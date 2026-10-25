from flask import Blueprint, render_template, request, redirect, url_for
from .database import get_db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    return render_template("index.html", users=users)

@main.route("/add-user", methods=["POST"])
def add_user():
    username = request.form.get("username")
    email = request.form.get("email")

    if username and email:
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        db.commit()

    return redirect(url_for("main.index"))