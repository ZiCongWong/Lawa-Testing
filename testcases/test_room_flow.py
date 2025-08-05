import pytest
import time
import threading
from api import user_api


def heartbeat_worker(stop_event, token, user_id):
    """
    在后台线程中运行的心跳函数
    :param stop_event: 用于通知线程停止的事件
    :param token: 用户 token
    :param user_id: 用户 ID
    """
    print("\n>>> [心跳线程]: 已启动")
    while not stop_event.is_set():
        user_api.room_heartbeat(token=token, user_id=user_id)
        # 等待30秒，或者如果 stop_event 被设置，则提前退出
        stop_event.wait(30)
    print("\n>>> [心跳线程]: 已停止")


def test_full_room_lifecycle(login_session):
    """
    测试完整的 "登录 -> 进房 -> 后台心跳 -> 房间操作 -> 退房 -> 停止心跳" 的生命周期
    """
    # 1. 准备会话信息和停止信号
    token = login_session['token']
    user_id = login_session['userId']
    stop_heartbeat_event = threading.Event()

    # 2. 进入房间
    enter_room_response = user_api.enter_room(token=token, user_id=user_id)
    assert enter_room_response.json()['code'] == 200
    print("\n--- [主流程]: 成功进入房间 ---")

    # 3. 启动后台心跳线程
    heartbeat_thread = threading.Thread(
        target=heartbeat_worker,
        args=(stop_heartbeat_event, token, user_id),
        daemon=True  # 设置为守护线程，主线程退出时它也会退出
    )
    heartbeat_thread.start()
    time.sleep(1)  # 短暂等待，确保心跳线程已运行

    # 4. 执行房间内的其他操作
    print("\n--- [主流程]: 执行房间内操作 (上麦)... ---")
    on_mic_response = user_api.on_mic(token=token, user_id=user_id)
    assert on_mic_response.status_code == 200
    assert on_mic_response.json()['code'] == 200

    # 5. 模拟用户在房间内停留一段时间
    print("\n--- [主流程]: 模拟用户在房间停留5秒... ---")
    time.sleep(5)

    # 6. 退出房间
    print("\n--- [主流程]: 准备退出房间... ---")
    exit_room_response = user_api.exit_room(token=token, user_id=user_id)
    assert exit_room_response.status_code == 200
    assert exit_room_response.json()['code'] == 200

    # 7. 停止心跳线程
    print("\n--- [主流程]: 发送停止信号给心跳线程... ---")
    stop_heartbeat_event.set()
    heartbeat_thread.join(timeout=5)  # 等待心跳线程结束，设置超时以防万一

    print("\n--- [主流程]: 测试完成 ---")
