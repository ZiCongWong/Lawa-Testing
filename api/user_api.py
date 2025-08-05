import requests
from common.yaml_handler import config_data
from common.encryption_handler import generate_signature, get_password_md5

BASE_URL = config_data['base_url']
room_id = config_data['roomId']


def _send_request(url, payload, token, user_id, description,method):
    """封装通用的请求逻辑"""
    dynamic_headers = generate_signature(body=payload)
    headers = config_data['login_headers'].copy()
    headers['token'] = token
    headers['userId'] = str(user_id)
    headers.update(dynamic_headers)

    print(f"\n[请求] {description}: {url}")
    print(f"[请求] Body: {payload}")

    response = requests.request(method=method,url=url, json=payload, headers=headers)

    try:
        data = response.json()
        print(f"[响应] {description}响应: {data}")
    except requests.exceptions.JSONDecodeError:
        print(f"[响应] {description}响应: {response.text}")

    return response

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
    enter_room_payload = {"pwd":"","roomId":room_id}
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


def room_heartbeat(token, user_id):
    """
    发送房间心跳包
    :param token: 登录后获取的 token
    :param user_id: 登录后获取的 userId
    :param room_id: 进入房间后获取的 roomId
    :return: requests的response对象
    """
    # 1. 构建心跳接口的请求体
    heartbeat_payload = {"inRoom": 1, "roomId": room_id}

    # 2. 调用通用签名函数
    dynamic_headers = generate_signature(body=heartbeat_payload)

    # 3. 组合完整的请求头
    headers = config_data['login_headers'].copy()
    headers['token'] = token
    headers['userId'] = str(user_id)
    headers.update(dynamic_headers)

    # 4. 发送请求
    heartbeat_url = f"{BASE_URL}/voice/room/heartbeat"
    print(f"\n[请求] 发送心跳: {heartbeat_url}")
    print(f"[请求] Body: {heartbeat_payload}")
    response = requests.post(heartbeat_url, json=heartbeat_payload, headers=headers)

    try:
        data = response.json()
        print(f"[响应] 心跳响应: {data}")
    except requests.exceptions.JSONDecodeError:
        print(f"[响应] 心跳响应: {response.text}")

    return response

def on_mic(token, user_id):
    """上麦操作示例"""
    payload = {"event": 1, "seat": 2, "roomId": room_id}
    url = f"{BASE_URL}/voice/mic/event"
    return _send_request(url, payload, token, user_id, "上麦",method="POST")

def exit_room(token, user_id):
    """退出房间"""
    payload = {"roomId": room_id}
    url = f"{BASE_URL}/voice/room/quitRoom"
    return _send_request(url, payload, token, user_id, "退出房间",method="POST")




