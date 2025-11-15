
from flask import render_template, request, url_for, redirect
from app.users import users_bp

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age", None)


    processed_name = name.upper()

    return render_template("users/hi.html",
                           name=processed_name,
                           age=age)

@users_bp.route("/admin")
def admin():

    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)