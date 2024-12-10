# 导入必要的库
import ssl

from lib import data
from ssl import *  # 导入ssl模块的所有内容
from Crypto.Random import random  # 从Crypto库中导入random，用于生成随机数
from flask import *  # 从flask库中导入所有内容
from flask_socketio import SocketIO  # 导入Flask-SocketIO，用于实现WebSocket通信

ip = "127.0.0.1"
port = 1145

api = data.i_requests(ip, port)

# 初始化Flask应用
app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'  # 设置Flask应用的密钥，用于会话加密等
socketio = SocketIO(app)  # 初始化SocketIO对象，绑定到Flask应用


# 彩蛋
@app.route('/XikMkd-IINC')
def egg():
    return "10,这个数字代表的是什么呢？"

@app.route('/NyaCat-YYDS')
def checkegg():
    return "这里是彩蛋哦！" # 还没想好彩蛋页面放什么呢QAQ
# 彩蛋END


# 定义404错误处理函数
@app.errorhandler(404)
def server_error(error):
    if random.randint(1, 100) == 50: # 1% 的概率进入彩蛋页面
        return render_template('publichtml/egghunt.html')
    return render_template('assets/ErrPage/404.html')  # 渲染404错误页面

@app.route('/repasswdErr')
def repasswdErr():
    return render_template('assets/ErrPage/repasswdErr.html')

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
    userip = request.remote_addr # 获取用户ip
    session['re_email'] = False # 恢复参数

    # 根据用户是否登录，显示不同的导航菜单项
    if request.cookies.get("MiaoWu") == None:
        fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    else:
        try:
            # 解码用户认证cookie，获取用户信息
            cookie = request.cookies.get("MiaoWu")
            stat, username = api.checkLogin(userip, cookie)
            if stat:
                fhkos = f'''
            <li class="dropdown"><a href="#"><span>{username}</span> <i class="bi bi-chevron-down"></i></a>
            <ul>
            <li><a href="/user">我的档案</a></li>
            <li><a href="javascript:logout()">Logout</a></li>
            </ul>
            </li>
            '''
            else:
                fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
        except:
            fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    
    # 查询服务器状态
    stat, server_data = api.serverinfo(userip)

    # 生成随机图片编号
    randomimg = random.randint(1, 31)
    
    # 渲染首页，传递相关变量
    return render_template('index.html', stat=stat, fhkos=fhkos, randomimg=randomimg, bans=server_data['BannedUser'],
                           reg=server_data['AllUser'], regapp=server_data['AllApplication'],
                           event=server_data['NumberOfEvents'])

# 定义登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    userip = request.remote_addr # 获取用户ip

    if request.cookies.get("MiaoWu") != None:
        return redirect(url_for('home'), code=301)
    if request.method == 'POST':
        email = request.form.get("email")
        passwd = request.form.get("password")
        stat, data, message = api.login(userip, email, passwd)
        print(stat, data, message)
        if stat:
            response = make_response(redirect(url_for('home'), code=301))
            response.set_cookie('MiaoWu', data, httponly=True)
            return response
        else:
            return render_template('account/login.html', msg=message)
    return render_template('account/login.html')

# 定义注册页面路由
@app.route('/register', methods=['GET', 'POST'])
def reg():
    userip = request.remote_addr # 获取用户ip

    if request.cookies.get("MiaoWu") != None:
        return redirect(url_for('home'), code=301)
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        passwd = request.form.get("password")
        stat, message = api.register(userip, username, email, passwd)
        if stat:
            return render_template('account/register.html', msg=message)
        else:
            return render_template('account/register.html', msg=message)
    return render_template('account/register.html')  # 渲染注册页面

@app.route('/verification/<token>')
def verification(token):
    userip = request.remote_addr # 获取用户ip

    if api.verification(userip, token):
        return redirect(url_for('login'), code=301)
    return redirect(url_for('reg'), code=301)

# 定义忘记密码页面路由
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    userip = request.remote_addr # 获取用户ip

    if request.method == 'POST':
        email = request.form.get("email")
        session["re_email"] = email
        stat, message = api.forgot(userip, email)
        if stat:
            return redirect(url_for('repasswd'), code=301)
        else:
            return render_template('account/forgot.html', msg=message)
    return render_template('account/forgot.html')  # 渲染忘记密码页面

@app.route('/resetpassword', methods=['GET', 'POST'])
def repasswd():
    userip = request.remote_addr # 获取用户ip

    email = session.get("re_email")
    if email == False:
        return redirect(url_for('repasswdErr'))
    if request.method == 'POST':
        code = request.form.get("verification_code")
        passwd = request.form.get("New_password")
        stat, message = api.resetpassword(userip, email, code, passwd)
        if stat:
            return render_template('account/resetpassword.html', account=email, msg=message)
        else:
            return render_template('account/resetpassword.html', account=email, msg=message)
    return render_template('account/resetpassword.html', account=email)

# 定义用户信息页面路由
@app.route('/user/<uid>', methods=['GET'])
def user(uid):
    return uid

# 主程序入口
if __name__ == '__main__':
    # 加载SSL证书和密钥
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('mc.nyacat.cloud_bundle.crt', 'mc.nyacat.cloud.key')
    
    # 运行Flask应用，启用WebSocket通信，使用HTTPS，允许不安全的Werkzeug调试器，并启用调试模式
    socketio.run(app, host='0.0.0.0', port=2096, allow_unsafe_werkzeug=True, debug=True, ssl_context=ssl_context)