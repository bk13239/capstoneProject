from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from contactForm import ContactForm
from flask_mail import Message, Mail
import pandas

mail = Mail()

app = Flask(__name__)

app.secret_key = "asdfghjklpoiuytrewq"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "dispatchLoggeramin@gmail.com"
app.config["MAIL_PASSWORD"] = "Suzieq319"

mail.init_app(app)


# Created NOT Done
@app.route("/home")
@app.route("/index")
@app.route("/")
def home():
    filename = 'callOutput.csv'
    data = pandas.read_csv(filename, header=0)
    callList = reversed(list(data.values))
    return render_template("index.html", callList=callList)


@app.route("/subscribe")
def subscribe():
    return render_template("subscribe.html")


@app.route("/archive")
def archive():
    return render_template("archive.html")


# Done
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if not form.validate():
            flash("All fields are required!")
            return render_template("contact.html", form=form)
        else:
            msg = Message(form.subject.data, sender="contact@dispatchlogger.com", recipients=['bk13239@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template("contact.html", success=True)
    elif request.method == "GET":
        return render_template("contact.html", form=form)


app.run(debug=True)
