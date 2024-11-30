import requests

class i_requests:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def post_api(self, version, api_path, headers=None, data=None):
        url = f"http://{self.ip}:{self.port}/api/zako/{version}/{api_path}"
        default_headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.42.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        if headers is not None:
            default_headers.update(headers)
 
        try:
            response = requests.post(url, headers=default_headers, json=data)
            response.raise_for_status()  # 这将引发HTTPError异常，如果响应状态码表示错误
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
    
    def userinfo(self):
        try:
            user_info = self.post_api("v1", "userinfo")
            if user_info is False:
                return "Server is Down", {"AllUser": "0", "BannedUser": "0", "AllApplication": "0", "NumberOfEvents": 0}
            return "Welcome to NyaCat！", user_info
        except Exception as e:
            return "Error processing user info", {"error": str(e)}


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = "8080"
    api = "reg"
    headers = {}
    data = {
        "uname" : "icelly",
        "pwd" : "icelly_QAQ2007",
        "e" : "icelly_QAQ@foxmail.com",
        "p" : "127.0.0.1"
    }
    apiserver = i_requests(ip, port)
    print(apiserver.post_api(api, data))
