from urllib3 import request

def __init__(self, url, data):
    self.url = url
    self.data = data
    self.data = self.get_data()

def post_api(self):
    header = {
        'url': self.url,
        'data': self.data
    }
    return request.post(header)
