import requests
import random

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

    def serverinfo(self):
        data = {
            "AllUser": "0",
            "BannedUser": "0",
            "AllApplication": "0",
            "NumberOfEvents": 0
        }

        try:
            server_info = requests.get(url=f"http://{self.ip}:{self.port}/api/zako/v2/server", headers=self.default_headers)
            return welcome_msg[random.randint(0, 2)], server_info.json()
        except:
            return "Server is Down", data

    def login(self, email, passwd):
        data = {
            "email": email,
            "pwd": passwd
        }

        try:
            login_data = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/login", headers=self.default_headers, json=data)
            if login_data.status_code == 200:
                return True, login_data.json()['token'], login_data.json()['message']
            else:
                return False, None, login_data.json()['message']
        except:
            return False, None, None
        
    def register(self, username, email, passwd):
        data = {
            "uname": username,
            "pwd": passwd,
            "e": email
        }
        try:
            register_data = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/register", headers=self.default_headers, json=data)
            if register_data.status_code == 200:
                return True, register_data.json()['message']
            else:
                return False, register_data.json()['message']
        except:
            return False, None
        
    def forgot(self, email):
        try:
            forgot_data = requests.get(f"http://{self.ip}:{self.port}/api/zako/v1/forgetpwd?email={email}", headers=self.default_headers)
            if forgot_data.status_code == 200:
                return True, forgot_data.json()['message']
            else:
                return False, forgot_data.json()['message']
        except:
            return False, None
        
    def resetpassword(self, email, code, passwd):
        data = {
            "email": email,
            "code": code,
            "password": passwd
        }
        try:
            repasswd = requests.post(f"http://{self.ip}:{self.port}/api/zako/v1/forgetpwd", headers=self.default_headers, json=data)
            if repasswd.status_code == 200:
                return True, repasswd.json()['message']
            else:
                return False, repasswd.json()['message']
        except:
            return False, None
        
    def verification(self, token):
        data = {
            "code": token
        }

        verification = requests.post(url=f"http://{self.ip}:{self.port}/api/zako/v1/verification", headers=self.default_headers, json=data)
        if verification.status_code == 200:
            return True
        return False

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
