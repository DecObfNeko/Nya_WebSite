from flask import Flask, render_template, request
import requests
from lib import data

app = Flask(__name__)

ip = "127.0.0.1"    # NyanID服务器ip
port = "8080"   # NyanID服务器端口

apiserver = data.i_requests(ip, port)


@app.route("/")
def home():
    return render_template("/home.html", title="首页")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if request.form.get('remember') == "on":
            remember = True
        else:
            remember = False

        data = {
            "email": username,
            "pwd": password,
            "p": "127.0.0.1"
        }
        print(data)

        if apiserver.post_api("login", data=data)[0]:
            return render_template("/login.html", title=("登录成功"))
        return render_template("/login.html", title=("登录失败"))
        
    return render_template("/login.html", title=("登录"))

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        data = {
            "uname" : username,
            "pwd" : password,
            "e" :  email,
            "p" : "127.0.0.1"
        }
        if password == confirm_password:
            if apiserver.post_api("reg", data=data)[0]:
                return render_template("/login.html", title=("注册成功"))
            return render_template("login.html", title=("注册失败"))
        return render_template("login.html", title=("密码不匹配"))
        
    return render_template("/reg.html", title=("注册"))

@app.route("/contact")
def contact():
    return render_template("/contact.html", title=("联系"))


if __name__ == "__main__":
    app.run(debug=True)
