import requests
from common.yaml_handler import config_data
from common.encryption_handler import generate_signature, get_password_md5

BASE_URL = config_data['base_url']
room_id = config_data['roomId']


def _send_request(url, payload, headers, description):
    """封装通用的请求逻辑"""
    if (description != "发送心跳"):
        print(f"\n[请求] {description} (用户: {headers.get('userId', 'N/A')}): {url}")
        print(f"[请求] Body: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    try:
        data = response.json()
        if(description != "发送心跳"):
            print(f"[响应] {description}响应: {data}")
    except requests.exceptions.JSONDecodeError:
        if (description != "发送心跳"):
            print(f"[响应] {description}响应: {response.text}")
    return response

def _get_headers(token, user_id, device):
    """为每个请求动态构建请求头"""
    headers = config_data['base_headers'].copy()
    headers['token'] = token
    headers['userId'] = str(user_id)
    headers['device'] = device
    return headers

def login(mobile, password, device):
    """发起登录请求"""
    login_payload = {"authType": "4", "phonePasswordParam": {"phone": mobile, "password": get_password_md5(password)}}
    headers = _get_headers('', '0', device) # 登录时 userId 为 0, token 为空
    dynamic_headers = generate_signature(body=login_payload)
    headers.update(dynamic_headers)
    login_url = f"{BASE_URL}/voice/user/login"
    return _send_request(login_url, login_payload, headers, "登录")


def enter_room(token, user_id, device):
    """发起进入房间的请求"""
    payload = {"pwd": "", "roomId": room_id}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/room/enterRoom"
    return _send_request(url, payload, headers, "进入房间")


def room_heartbeat(token, user_id, device):
    """发送房间心跳包"""
    payload = {"inRoom": 1, "roomId": room_id}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/room/heartbeat"
    return _send_request(url, payload, headers, "发送心跳")

def mic_heartbeat(token, user_id, device):
    """发送MIC心跳包"""
    payload = {"onMic": 1, "onPush":0,"roomId": room_id}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/mic/heartbeat"
    return _send_request(url, payload, headers, "发送心跳")

def on_mic(token, user_id, device, seat_index):
    """上麦操作示例"""
    # ★★★ 已按你的要求更新 ★★★
    payload = {"event": 1, "seat": seat_index, "roomId": room_id}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/mic/event"
    return _send_request(url, payload, headers, f"上麦到座位 {seat_index}")

def exit_room(token, user_id, device):
    """退出房间"""
    payload = {"roomId": room_id}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/room/quitRoom"
    return _send_request(url, payload, headers, "退出房间")

def red_pack(token, user_id, device):
    redPacketId = config_data['redPacketID']
    payload = {"roomId": room_id, "redPacketId": redPacketId}
    headers = _get_headers(token, user_id, device)
    dynamic_headers = generate_signature(body=payload)
    headers.update(dynamic_headers)
    url = f"{BASE_URL}/voice/room/grabRedPacket"
    return _send_request(url, payload, headers, "抢红包")




