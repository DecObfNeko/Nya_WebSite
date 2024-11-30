import base64
import ssl
from ssl import *
import requests
from Crypto.Random import random
from flask import *
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

api = 'http://nyanid.cn:8080'


@app.errorhandler(404)
def server_error(error):
    return render_template('assets/ErrPage/404.html')


@app.route('/prypoy')
def privacy_policy():
    return render_template('assets/ServiceAgreement/PrivacyPolicy.html')


@app.route('/mc')
def mcserver():
    return render_template('publichtml/server.html')

    #  fhkos = '''
    #    <li class="dropdown"><a href="#"><span>My Account</span> <i class="bi bi-chevron-down"></i></a>
    #  <ul>
    # <li><a href="/user">我的档案</a></li>
    #  <li><a href="javascript:logout()">Logout</a></li>
    #  </ul>
    #   </li>
    #    '''        fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    #   request.cookies.get("MiaoWu")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.cookies.get("MiaoWu") == None:
        fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
    else:
        try:
            cookie = request.cookies.get("MiaoWu")
            decoded_bytes = base64.b64decode(cookie)
            Dcookie = decoded_bytes.decode('utf-8')
            headers = {
                "Authorization": "Bearer " + Dcookie,
                "Event": "Gi"
            }
            data = requests.get(url=api + '/api/zako/v1/userinfo', headers=headers)
            rdata = data.json()
            username = rdata['username']
            fhkos = '''
                   <li class="dropdown"><a href="#"><span>''' + username + '''</span> <i class="bi bi-chevron-down"></i></a>
                 <ul>
                <li><a href="/user">我的档案</a></li>
                 <li><a href="javascript:logout()">Logout</a></li>
                 </ul>
                  </li>
                   '''
        except:
            fhkos = '<li><a class="getstarted scrollto" href="login?page=client">Login</a></li>'
        finally:
            pass

    stat = ''
    try:
        data = requests.get(api + "/api/zako/v2/server")
        serverjson = data.json()
    except requests.exceptions.InvalidURL:
        stat = 'Server is Down'
        serverjson = {"AllUser": "0", "BannedUser": "0", "AllApplication": "0", "NumberOfEvents": 0}
    randomimg = random.randint(1, 31)
    return render_template('index.html', stat=stat, fhkos=fhkos, randomimg=randomimg, bans=serverjson['BannedUser'],
                           reg=serverjson['AllUser'], regapp=serverjson['AllApplication'],
                           event=serverjson['NumberOfEvents'])






@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('account/login.html', )


@app.route('/register', methods=['GET', 'POST'])
def reg():
    return render_template('account/register.html', )


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('account/forgot.html', )


@app.route('/user/<uid>', methods=['GET'])
def user(uid):
    return uid


if __name__ == '__main__':
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('mc.nyacat.cloud_bundle.crt', 'mc.nyacat.cloud.key')
    socketio.run(app, host='0.0.0.0', port=2096, allow_unsafe_werkzeug=True, debug=True, ssl_context=ssl_context)
