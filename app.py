from flask import Flask, render_template, request

from lib import i_data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("/home.html", title="首页")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get('remember', False)
        data = {
            "e": username,
            "pwd": password,
            "uap": remember
        }
        if i_data.post_api("http://127.0.0.1:11451/api/zako/v1/ddu/bca/lue", data):
            return "114514"
    return render_template("/login.html", title=("登录"))

@app.route("/reg", methods=["GET", "POST"])
def reg():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("/reg.html", title=("注册"))

@app.route("/contact")
def contact():
    return render_template("/contact.html", title=("联系"))


if __name__ == "__main__":
    app.run(debug=True)
