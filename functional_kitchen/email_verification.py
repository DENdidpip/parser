import smtplib
import random
from email.message import EmailMessage
from werkzeug.security import generate_password_hash

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
        hashed_password = generate_password_hash(password)

        self.pending_users[email] = {
            "password_hash": hashed_password,
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