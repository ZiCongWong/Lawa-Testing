#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试送礼接口的示例脚本
"""

import uuid
from api.user_api import login, enter_room, send_gifts
from common.yaml_handler import config_data

def generate_global_order_id():
    """生成全局订单ID"""
    return str(uuid.uuid4()).replace('-', '')

def test_gift_sending():
    """测试送礼功能"""
    # 从配置文件获取用户信息
    user_creds = config_data['user_credentials']
    mobile = user_creds['mobile']
    password = user_creds['password']
    device = config_data['users'][0]['device']  # 使用第一个用户的设备ID
    room_id = config_data['roomId']
    
    print("=== 测试送礼接口 ===")
    
    # 1. 登录
    print("\n1. 用户登录...")
    login_response = login(mobile, password, device)
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.status_code}")
        return
    
    login_data = login_response.json()
    if login_data.get('code') != 0:
        print(f"登录失败: {login_data}")
        return
    
    token = login_data['data']['token']
    user_id = login_data['data']['userId']
    print(f"登录成功 - 用户ID: {user_id}, Token: {token[:20]}...")
    
    # 2. 进入房间
    print("\n2. 进入房间...")
    enter_response = enter_room(token, user_id, device)
    if enter_response.status_code != 200:
        print(f"进入房间失败: {enter_response.status_code}")
        return
    
    enter_data = enter_response.json()
    if enter_data.get('code') != 0:
        print(f"进入房间失败: {enter_data}")
        return
    
    print("进入房间成功")
    
    # 3. 发送礼物
    print("\n3. 发送礼物...")
    gift_config = config_data['gift_config']
    
    # 使用配置中的默认值，也可以自定义
    gift_id = gift_config['default_gift_id']
    global_order_id = generate_global_order_id()  # 生成新的订单ID
    nums = 1  # 礼物数量
    send_type = gift_config['default_send_type']
    source = gift_config['default_source']
    to_user_id_list = [int(room_id)]  # 发送给房间
    
    print(f"礼物参数:")
    print(f"  - 礼物ID: {gift_id}")
    print(f"  - 全局订单ID: {global_order_id}")
    print(f"  - 数量: {nums}")
    print(f"  - 房间ID: {room_id}")
    print(f"  - 发送类型: {send_type}")
    print(f"  - 来源: {source}")
    print(f"  - 接收用户列表: {to_user_id_list}")
    
    gift_response = send_gifts(
        token=token,
        user_id=user_id,
        device=device,
        gift_id=gift_id,
        global_order_id=global_order_id,
        nums=nums,
        room_id=int(room_id),
        send_type=send_type,
        source=source,
        to_user_id_list=to_user_id_list
    )
    
    print(f"\n送礼响应状态码: {gift_response.status_code}")
    if gift_response.status_code == 200:
        try:
            gift_data = gift_response.json()
            print(f"送礼响应数据: {gift_data}")
        except Exception as e:
            print(f"解析响应数据失败: {e}")
            print(f"原始响应: {gift_response.text}")
    else:
        print(f"送礼失败: {gift_response.text}")

if __name__ == "__main__":
    test_gift_sending()
