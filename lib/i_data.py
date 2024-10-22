from urllib3 import request
import json


def post_api(url, data):
    response = request.post(url, json=data)
    
    if response.status_code == 201:
        return True