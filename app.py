from flask import Flask, render_template, request
from lib import data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("/home.html", title="首页")


@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("/login.html", title=("登录"))

@app.route("/reg", methods=["GET", "POST"])
def reg():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("/reg.html", title=("注册"))

@app.route("/contact")
def lx():
    return render_template("/contact.html", title=("联系"))


if __name__ == "__main__":
    app.run(debug=True)
