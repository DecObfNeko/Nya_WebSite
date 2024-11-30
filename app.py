# 导入必要的库
import base64
import ssl
import requests  # 用于发起HTTP请求

from lib import data
from ssl import *  # 导入ssl模块的所有内容
from Crypto.Random import random  # 从Crypto库中导入random，用于生成随机数
from flask import *  # 从flask库中导入所有内容
from flask_socketio import SocketIO  # 导入Flask-SocketIO，用于实现WebSocket通信

ip = "192.168.0.106"
port = 8080

apiserver = data.i_requests(ip, port)

# 初始化Flask应用
app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'  # 设置Flask应用的密钥，用于会话加密等
socketio = SocketIO(app)  # 初始化SocketIO对象，绑定到Flask应用



# 定义404错误处理函数
@app.errorhandler(404)
def server_error(error):
    return render_template('assets/ErrPage/404.html')  # 渲染404错误页面

# 定义隐私政策页面路由
@app.route('/prypoy')
def privacy_policy():
    return render_template('assets/ServiceAgreement/PrivacyPolicy.html')  # 渲染隐私政策页面

# 定义Minecraft服务器页面路由
@app.route('/mc')
def mcserver():
    return render_template('publichtml/server.html')  # 渲染Minecraft服务器页面

# 定义首页路由及逻辑
@app.route('/', methods=['GET', 'POST'])
def home():
    # 根据用户是否登录，显示不同的导航菜单项
    if request.cookies.get("MiaoWu") == None:
        fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    else:
        try:
            # 解码用户认证cookie，获取用户信息
            cookie = request.cookies.get("MiaoWu")
            decoded_bytes = base64.b64decode(cookie)
            Dcookie = decoded_bytes.decode('utf-8')
            headers = {
                "Authorization": "Bearer " + Dcookie,
                "Event": "Gi"
            }
            data = data = apiserver.post_api("v1", "userinfo", headers)[1]
            username = data['username']
            fhkos = f'''
            <li class="dropdown"><a href="#"><span>{username}</span> <i class="bi bi-chevron-down"></i></a>
            <ul>
            <li><a href="/user">我的档案</a></li>
            <li><a href="javascript:logout()">Logout</a></li>
            </ul>
            </li>
            '''
        except:
            fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    
    # 查询服务器状态
    stat, data = apiserver.userinfo()

    # 生成随机图片编号
    randomimg = random.randint(1, 31)
    
    # 渲染首页，传递相关变量
    return render_template('index.html', stat=stat, fhkos=fhkos, randomimg=randomimg, bans=data['BannedUser'],
                           reg=data['AllUser'], regapp=data['AllApplication'],
                           event=data['NumberOfEvents'])

# 定义登录页面路由
@app.route('/login', methods=['GET', 'POST'])
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
        }
        print(data)

        if apiserver.post_api("v1", "login", data=data)[0] == True:
            print(apiserver.post_api("v1", "login", data=data))
            return render_template('account/login.html', title=("登录成功"))
        return render_template('account/login.html', title=("登录失败"))

# 定义注册页面路由
@app.route('/register', methods=['GET', 'POST'])
def reg():
    return render_template('account/register.html')  # 渲染注册页面

# 定义忘记密码页面路由
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('account/forgot.html')  # 渲染忘记密码页面

# 定义用户信息页面路由
@app.route('/user/<uid>', methods=['GET'])
def user(uid):
    return uid  # 返回用户ID（此处仅为示例，实际应用中应返回用户信息）

# 主程序入口
if __name__ == '__main__':
    # 加载SSL证书和密钥
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('mc.nyacat.cloud_bundle.crt', 'mc.nyacat.cloud.key')
    
    # 运行Flask应用，启用WebSocket通信，使用HTTPS，允许不安全的Werkzeug调试器，并启用调试模式
    socketio.run(app, host='0.0.0.0', port=2096, allow_unsafe_werkzeug=True, debug=True, ssl_context=ssl_context)