import requests
import random
import base64

welcome_msg = [
    "Welcome to NyaCat!",
    "Here is NyaCat!",
    "MiaoWu~~~"
]

class i_requests:
    default_headers = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.42.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def serverinfo(self, userip):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        data = {
            "AllUser": "0",
            "BannedUser": "0",
            "AllApplication": "0",
            "NumberOfEvents": 0
        }

        try:
            server_info = requests.get(url=f"http://{self.ip}:{self.port}/api/zako/v2/server", headers=headers)
            return welcome_msg[random.randint(0, 2)], server_info.json()
        except:
            return "Server is Down", data

    def login(self, userip, email, passwd):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        data = {
            "email": email,
            "pwd": passwd
        }

        try:
            login_data = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/login", headers=headers, json=data)
            if login_data.status_code == 200:
                print("ok")
                return True, login_data.json()['data'], None
            else:
                print("no")
                return False, None, login_data.json()['message']
        except:
            print("f")
            return False, None, None
        
    def register(self, userip, username, email, passwd):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        data = {
            "uname": username,
            "pwd": passwd,
            "e": email
        }
        try:
            register_data = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/register", headers=headers, json=data)
            if register_data.status_code == 200:
                return True, register_data.json()['message']
            else:
                return False, register_data.json()['message']
        except:
            return False, None
        
    def forgot(self, userip, email):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        try:
            forgot_data = requests.get(f"http://{self.ip}:{self.port}/api/zako/v1/forgetpwd?email={email}", headers=headers)
            if forgot_data.status_code == 200:
                return True, forgot_data.json()['message']
            else:
                return False, forgot_data.json()['message']
        except:
            return False, None
        
    def resetpassword(self, userip, email, code, passwd):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        data = {
            "email": email,
            "code": code,
            "password": passwd
        }
        try:
            repasswd = requests.post(f"http://{self.ip}:{self.port}/api/zako/v1/forgetpwd", headers=headers, json=data)
            if repasswd.status_code == 200:
                return True, repasswd.json()['message']
            else:
                return False, repasswd.json()['message']
        except:
            return False, None
        
    def verification(self, userip, token):
        headers = {
            "UserIP": userip
        }

        headers.update(self.default_headers)

        data = {
            "code": token
        }

        verification = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/verification", headers=headers, json=data)
        if verification.status_code == 200:
            return True
        return False

    def checkLogin(self, userip, cookie):
        try:
            decoded_bytes = base64.b64decode(cookie)
            Dcookie = decoded_bytes.decode('utf-8')
            headers = {
                "UserIP": userip,
                "Authorization": "Bearer " + Dcookie,
                "Event": "Gi"
            }
            checkLogin = requests.get(f"http://{self.ip}:{self.port}/api/zako/v1/userinfo", headers=headers)
            if checkLogin.status_code == 200:
                return True, checkLogin.json()['username']
            else:
                return False, None
        except:
            return False, None
        
    # 对邮箱进行base64编码的函数
    def encode_email(self, email):
        encoded_email = base64.b64encode(email).decode('utf-8')
        return encoded_email
 
    # 对base64编码的邮箱进行解码的函数
    def decode_email(slef, encoded_email):
        email_bytes = base64.b64decode(encoded_email)
        email = email_bytes.decode('utf-8')
        return email


if __name__ == "__main__":
    api = i_requests("127.0.0.1", 1145)
    api.forgot("1787522500@qq.com")


'''
 *                    _ooOoo_
 *                   o8888888o
 *                   88" . "88
 *                   (| -_- |)
 *                    O\ = /O
 *                ____/`---'\____
 *              .   ' \\| |// `.
 *               / \\||| : |||// \
 *             / _||||| -:- |||||- \
 *               | | \\\ - /// | |
 *             | \_| ''\---/'' | |
 *              \ .-\__ `-` ___/-. /
 *           ___`. .' /--.--\ `. . __
 *        ."" '< `.___\_<|>_/___.' >'"".
 *       | | : `- \`.;`\ _ /`;.`/ - ` : | |
 *         \ \ `-. \_ __\ /__ _/ .-` / /
 * ======`-.____`-.___\_____/___.-`____.-'======
 *                    `=---='
 *
 * .............................................
 *          佛祖保佑             永无BUG
'''
