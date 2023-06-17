from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vibehouse.cmr@gmail.com'
app.config['MAIL_PASSWORD'] = 'qfqlbxvrxodkzzvj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


class User_d(db.Model):
    Username = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    DOB = db.Column(db.String(250), nullable=False)


class User_msg(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)


class UserLandlord(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/index.html')
def home_page1():
    return render_template("index.html")


@app.route('/about.html')
def about_page():
    return render_template("about.html")


@app.route("/blog.html")
def blog_page():
    return render_template("blog.html")


@app.route("/blog-single.html")
def blog_single_page():
    return render_template("blog-single.html")


@app.route("/submit-msg", methods=["POST", "GET"])
def contact_s():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        new_post = User_msg(name=name, email=email, subject=subject, message=message)
        db.session.add(new_post)
        db.session.commit()

        msg = Message(subject+" by "+email, sender=email, recipients=["vibehouse.cmr@gmail.com"])
        msg.body = message
        mail.send(msg)
        return render_template("contact.html")


@app.route("/contact.html")
def contact_page():
    return render_template("contact.html")


@app.route("/msg-landlord", methods=["POST", "GET"])
def landlord_s():
    if request.method == "POST":
        l_name = request.form.get('l_name')
        l_email = request.form.get('l_email')
        l_subject = request.form.get('l_subject')
        l_message = request.form.get('l_message')
        l_new_post = UserLandlord(name=l_name, email=l_email, subject=l_subject, message=l_message)
        db.session.add(l_new_post)
        db.session.commit()

        msg = Message(l_subject + " by " + l_email, sender=l_email, recipients=["vibehouse.cmr@gmail.com"])
        msg.body = l_message
        mail.send(msg)
        return render_template("Landlord.html")


@app.route("/Landlord.html")
def landlord():
    return render_template("Landlord.html")


@app.route("/property.html")
def property_page():
    return render_template("property.html")


@app.route("/index2.html")
def after_login():
    return render_template("index2.html")


@app.route("/property-single.html")
def property_single():
    return render_template("property-single.html")


@app.route("/ok.html")
def login_page():
    return render_template("ok.html")


@app.route("/register1.html")
def register_page():
    return render_template("register1.html")


@app.route("/submit-data", methods=["POST", "GET"])
def register_s():
    if request.method == "POST":
        name = request.form.get('firstname')
        email = request.form.get('email')
        username = request.form.get('u_name')
        password = request.form.get('password')
        dob = request.form.get('date_ob')
        phone_no = request.form.get('ph_no')
        new_post1 = User_d(Username=username, name=name, password=password, DOB=dob,  phone_no= phone_no,email=email,)
        db.session.add(new_post1)
        db.session.commit()
        return render_template("index.html")


@app.route("/login-user", methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        data = User_d.query.filter_by(Username=username, password=password).first_or_404(description='There is no data with {}'.format(username))
        return render_template("index2.html", data=[data.name])


@app.route('/form', methods=["POST", "GET"])
def form():
    email = request.form.get("email")

    msg = Message("Thank You", sender="vibehouse.cmr@gmail.com", recipients=[email])
    msg.body = "You have been subscribed to our Newsletter."
    mail.send(msg)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
