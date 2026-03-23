from flask import Flask, render_template, request, redirect, url_for
from parser_kitchen.together import Our_result
from flask_sqlalchemy import SQLAlchemy
import smtplib
import random
from email.message import EmailMessage
from parser_kitchen.login_linkedin import EMAIL, PASSWORD, NICK_POSTGRES, PASS_POSTGRES
from urllib.parse import quote_plus

app = Flask(__name__)


db_user = NICK_POSTGRES
db_pass = PASS_POSTGRES
db_name = "parser"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    nick = db.Column(db.String(50), nullable = False)
class EmailService:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_code(self, to_email, code):
        msg = EmailMessage()
        msg["Subject"] = "Verification Code"
        msg["From"] = self.email
        msg["To"] = to_email
        msg.set_content(f"Your verification code: {code}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.email, self.password)
            smtp.send_message(msg)

class UserManager:
    def __init__(self):
        self.pending_users = {}

    def create_user(self, email, password, nick):
        code = str(random.randint(100000, 999999))

        self.pending_users[email] = {
            "password": password,
            "nick": nick,
            "code": code
        }

        return code

    def verify_code(self, email, user_code):
        if email in self.pending_users:
            if self.pending_users[email]["code"] == user_code:
                user_data = self.pending_users[email]
                self.pending_users.pop(email)
                return True, user_data

        return False, None


email_service = EmailService(
    email=EMAIL,
    password= PASSWORD
)

user_manager = UserManager()


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/find', methods=["POST"])
def parse():
    job = str(request.form['job']).replace(" ", "-").lower()
    town = str(request.form['town']).replace(" ", "-").lower()

    data = Our_result(town, job).get_data()

    return render_template("out.html", vacancies=data)



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nick = request.form['nick']

        code = user_manager.create_user(email, password, nick)
        email_service.send_code(email, code)

        return redirect(url_for('verify', email=email))

    return render_template("sign_up.html")


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    email = request.args.get('email')

    if request.method == 'POST':
        user_code = request.form['code']

        success, user_data = user_manager.verify_code(email, user_code)

        if success:
            print("Registered:", user_data)
            return "Registration is successful!"

        return "Wrong code"

    return render_template("verify.html", email=email)


# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)