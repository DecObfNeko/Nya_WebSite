from flask import Flask, render_template, request
import requests
from lib import data

app = Flask(__name__)

ip = "127.0.0.1"    # 登录验证服务器ip
port = "8080"   # 登录验证服务器端口

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
            "e": username,
            "pwd": password,
            "uap": remember
        }
        print(data)

        if apiserver.post_api("login", data=data)[0] == True:
            return render_template("/login.html", title=("登录成功"))
        return render_template("/login.html", title=("登录失败"))
        
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
