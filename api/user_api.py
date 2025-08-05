import requests
from common.yaml_handler import config_data
from common.encryption_handler import generate_signature, get_password_md5

BASE_URL = config_data['base_url']


def login(mobile, raw_password):

    login_payload = {
        "authType": "4",
        "phonePasswordParam": {
            "phone": mobile,
            "password": get_password_md5(raw_password)
        }
    }


    dynamic_headers = generate_signature(body=login_payload)


    headers = config_data['login_headers'].copy()
    headers.update(dynamic_headers)

    login_url = f"{BASE_URL}/voice/user/login"

    print(f"\n[请求]: {login_url}")
    print(f"[请求]Headers: {headers}")
    print(f"[请求]Body: {login_payload}")

    response = requests.post(login_url, json=login_payload, headers=headers)
    data = response.json()

    try:
        print(f"[响应]: {data['code']}, 内容: {data}")
    except requests.exceptions.JSONDecodeError:
        print(f"[响应]: {data['code']}, 内容: {data}")

    return response


def enter_room(token,user_id):
    enter_room_payload = {"pwd":"","roomId":1000153}
    dynamic_headers = generate_signature(body=enter_room_payload)
    headers = config_data['login_headers'].copy()
    # ★★★ 关键点: 更新 header 中的 token 和 userId
    headers['token'] = token
    headers['userId'] = str(user_id) # userId 必须是字符串
    headers.update(dynamic_headers)


    enter_room_url = f"{BASE_URL}/voice/room/enterRoom"

    print(f"\n[请求] 进入房间接口: {enter_room_url}")
    print(f"[请求] Headers: {headers}")
    print(f"[请求] Body: {enter_room_payload}")

    response = requests.post(enter_room_url, json=enter_room_payload, headers=headers)
    data = response.json()

    try:
        print(f"[响应]: {data['code']}, 内容: {data}")
    except requests.exceptions.JSONDecodeError:
        print(f"[响应]: {data['code']}, 内容: {data}")

    return response



