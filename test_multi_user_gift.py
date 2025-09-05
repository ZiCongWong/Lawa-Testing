#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多用户送礼功能的示例脚本
"""

import uuid
from api.user_api import login, enter_room, send_gifts
from common.yaml_handler import config_data

def test_multi_user_gift():
    """测试多用户送礼功能"""
    print("=== 测试多用户送礼功能 ===")
    
    # 获取配置中的用户信息
    users = config_data['users']
    room_id = config_data['roomId']
    gift_config = config_data['gift_config']
    
    if not users:
        print("!!! 配置文件中没有用户信息")
        return
    
    # 只测试前两个用户
    test_users = users[:2]
    user_sessions = []
    
    # 1. 登录所有测试用户
    print("\n1. 登录测试用户...")
    for user_config in test_users:
        print(f"\n--- 登录用户: {user_config['mobile']} ---")
        login_response = login(user_config['mobile'], user_config['password'], user_config['device'])
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            if login_data.get('code') == 200:
                user_data = login_data['data']
                user_sessions.append({
                    'mobile': user_config['mobile'],
                    'user_id': user_data['userId'],
                    'token': user_data['token'],
                    'device': user_config['device']
                })
                print(f"✓ 用户 {user_config['mobile']} 登录成功 (UserID: {user_data['userId']})")
            else:
                print(f"✗ 用户 {user_config['mobile']} 登录失败: {login_data}")
        else:
            print(f"✗ 用户 {user_config['mobile']} 登录失败: {login_response.status_code}")
    
    if not user_sessions:
        print("!!! 没有用户成功登录，测试终止")
        return
    
    # 2. 所有用户进入房间
    print(f"\n2. 所有用户进入房间 {room_id}...")
    for session in user_sessions:
        print(f"\n--- 用户 {session['user_id']} 进入房间 ---")
        enter_response = enter_room(session['token'], session['user_id'], session['device'])
        
        if enter_response.status_code == 200:
            enter_data = enter_response.json()
            if enter_data.get('success'):
                print(f"✓ 用户 {session['user_id']} 成功进入房间")
            else:
                print(f"✗ 用户 {session['user_id']} 进入房间失败: {enter_data}")
        else:
            print(f"✗ 用户 {session['user_id']} 进入房间失败: {enter_response.status_code}")
    
    # 3. 测试送礼功能
    print(f"\n3. 测试送礼功能...")
    
    # 第一个用户发送礼物给房间
    if user_sessions:
        sender = user_sessions[0]
        print(f"\n--- 用户 {sender['user_id']} 发送礼物给房间 ---")
        
        global_order_id = str(uuid.uuid4()).replace('-', '')
        gift_response = send_gifts(
            token=sender['token'],
            user_id=sender['user_id'],
            device=sender['device'],
            gift_id=gift_config['default_gift_id'],
            global_order_id=global_order_id,
            nums=1,
            room_id=int(room_id),
            send_type=gift_config['default_send_type'],
            source=gift_config['default_source'],
            to_user_id_list=[int(room_id)]
        )
        
        print(f"送礼响应状态码: {gift_response.status_code}")
        if gift_response.status_code == 200:
            try:
                gift_data = gift_response.json()
                print(f"✓ 送礼成功: {gift_data}")
            except:
                print(f"✓ 送礼成功: {gift_response.text}")
        else:
            print(f"✗ 送礼失败: {gift_response.text}")
    
    # 如果有第二个用户，测试用户间送礼
    if len(user_sessions) >= 2:
        sender = user_sessions[0]
        receiver = user_sessions[1]
        print(f"\n--- 用户 {sender['user_id']} 发送礼物给用户 {receiver['user_id']} ---")
        
        global_order_id = str(uuid.uuid4()).replace('-', '')
        gift_response = send_gifts(
            token=sender['token'],
            user_id=sender['user_id'],
            device=sender['device'],
            gift_id=gift_config['default_gift_id'],
            global_order_id=global_order_id,
            nums=2,  # 发送2个礼物
            room_id=int(room_id),
            send_type=gift_config['default_send_type'],
            source=gift_config['default_source'],
            to_user_id_list=[receiver['user_id']]
        )
        
        print(f"送礼响应状态码: {gift_response.status_code}")
        if gift_response.status_code == 200:
            try:
                gift_data = gift_response.json()
                print(f"✓ 用户间送礼成功: {gift_data}")
            except:
                print(f"✓ 用户间送礼成功: {gift_response.text}")
        else:
            print(f"✗ 用户间送礼失败: {gift_response.text}")
    
    print(f"\n=== 多用户送礼功能测试完成 ===")

if __name__ == "__main__":
    test_multi_user_gift()
