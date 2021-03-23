# Imports for needed packages
import csv
import math
import struct
import time
import wave
import pyaudio
import speech_recognition as sr
from datetime import datetime

r = sr.Recognizer()  # Creating speech_recognition object

# now = datetime.now()  # Creating datetime object
# dateTime = now.strftime("%m%d%Y%H%M%S")  # Creating formatting for filename
# filename = dateTime + ".wav"  # Creating filename
# outTime = now.strftime("%m/%d/%Y, %H:%M:%S")  # Creating formatting for output file

Threshold = 10  # Sets sound threshold to start recording

# Audio parameters
SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
INPUT = 1

TIMEOUT_LENGTH = 5  # Time to timeout from silence


class Recorder:

    # Calculates average size of numbers regardless of positive or negative; Used to detect current sound volume
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        form = "%dh" % count
        shorts = struct.unpack(form, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    # Initializes pyAudio objects
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk,
                                  input_device_index=INPUT)

    # Records sound when called
    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    # Writes recorded sound to file using filename
    def write(self, recording):
        now = datetime.now()  # Creating datetime object
        dateTime = now.strftime("%m%d%Y%H%M%S")  # Creating formatting for filename
        filename = dateTime + ".wav"  # Creating filename
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')
        self.convertspeech(filename)

    # Listens for an RMS above threshold
    def listen(self):
        print('Listening beginning')
        while True:
            sound = self.stream.read(chunk)
            rms_val = self.rms(sound)
            if rms_val > Threshold:
                self.record()

    # Converts recorded sound into text and outputs into txt file
    @staticmethod
    def convertspeech(namefile):
        now = datetime.now()  # Creating datetime object
        outTime = now.strftime("%m/%d/%Y, %H:%M:%S")  # Creating formatting for output file
        with sr.WavFile(namefile) as source:
            print('Processing')
            audio = r.record(source)

            try:
                text = r.recognize_google(audio)
            except sr.UnknownValueError:
                text = "-----Audio Could Not Be Converted To Text-----"

            print("You said : {}".format(text))
            writecsv(outTime, text, namefile)


# Function to write the text output from a call to the csv file
def writecsv(date, text, ref):
    with open(r'callOutput.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Date", "Text", "Audio Ref"])
        # Uncomment the next line when running program for first time
        # writer.writeheader()
        writer.writerow({"Date": date, "Text": text, "Audio Ref": ref})


a = Recorder()

a.listen()
