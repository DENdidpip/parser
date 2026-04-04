from flask import Blueprint, render_template, request, redirect, url_for, current_app
from parser_kitchen.together import Our_result
from .user import db, User
from .email_verification import EmailService, UserManager

main_bp = Blueprint("main", __name__)

email_service = None
user_manager = UserManager()


@main_bp.before_app_request
def setup_services():
    global email_service
    if email_service is None:
        email_service = EmailService(
            email=current_app.config["EMAIL_USER"],
            password=current_app.config["EMAIL_PASS"]
        )


@main_bp.route("/")
def main():
    return render_template("index.html")


@main_bp.route("/find", methods=["POST"])
def parse():
    job = str(request.form["job"]).replace(" ", "-").lower()
    town = str(request.form["town"]).replace(" ", "-").lower()

    data = Our_result(town, job).get_data()

    return render_template("out.html", vacancies=data)


@main_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        nick = request.form["nick"]

        already_registered = User.query.filter_by(email=email).first()
        if already_registered:
            return "User with this email already exists"

        code = user_manager.create_user(email, password, nick)
        email_service.send_code(email, code)

        return redirect(url_for("main.verify", email=email))

    return render_template("sign_up.html")


@main_bp.route("/verify", methods=["GET", "POST"])
def verify():
    email = request.args.get("email")

    if request.method == "POST":
        user_code = request.form["code"]

        success, user_data = user_manager.verify_code(email, user_code)

        if success:
            new_user = User(
                email=email,
                password_hash=user_data["password_hash"],
                nick=user_data["nick"]
            )
            db.session.add(new_user)
            db.session.commit()

            return "Registration is successful!"

        return "Wrong code"

    return render_template("verify.html", email=email)