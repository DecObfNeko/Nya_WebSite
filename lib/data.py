import requests

class i_requests:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def post_api(self, api, headers=None, data=None):
        url = f"http://{self.ip}:{self.port}/api/zako/v1/{api}"
        default_headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.42.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        if headers:
            default_headers.update(headers)

        response = requests.post(url, headers=default_headers, json=data)

        if response.status_code == 200:
            return True, response.json()
        else:
            return response.status_code, response.json()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = "8080"
    api = "login"
    headers = {}
    data = {
        "e": "1787522500@qq.com",
        "pwd": "114514",
        "uap": True
    }
    apiserver = i_requests(ip, port, api, headers, data)