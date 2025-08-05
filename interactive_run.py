import time
import threading
from api import user_api
from common.yaml_handler import config_data


def heartbeat_worker(stop_event, token, user_id):
    """
    在后台线程中运行的心跳函数
    """
    print("\n>>> [心跳线程]: 已启动，每30秒发送一次心跳...")
    while not stop_event.is_set():
        user_api.room_heartbeat(token=token, user_id=user_id)
        # 等待30秒，或者如果 stop_event 被设置，则提前退出
        stop_event.wait(30)
    print("\n>>> [心跳线程]: 已停止")


def main():
    """
    主交互流程
    """
    # 1. 登录
    print("--- 步骤1: 正在登录... ---")
    mobile = config_data['user_credentials']['mobile']
    password = config_data['user_credentials']['password']
    login_response = user_api.login(mobile, password)

    if login_response.status_code != 200 or not login_response.json().get('success'):
        print("!!! 登录失败，程序退出。请检查配置或网络。")
        print(f"响应: {login_response.text}")
        return

    login_data = login_response.json()['data']
    token = login_data['token']
    user_id = login_data['userId']
    print(f"--- 登录成功! 用户ID: {user_id}, Token: {token[:10]}... ---")

    # 2. 进入房间
    print("\n--- 步骤2: 正在进入房间... ---")
    enter_room_response = user_api.enter_room(token=token, user_id=user_id)
    if enter_room_response.status_code != 200 or not enter_room_response.json().get('success'):
        print("!!! 进入房间失败，程序退出。")
        print(f"响应: {enter_room_response.text}")
        return
    print("--- 成功进入房间! ---")

    # 3. 启动后台心跳
    stop_heartbeat_event = threading.Event()
    heartbeat_thread = threading.Thread(
        target=heartbeat_worker,
        args=(stop_heartbeat_event, token, user_id),
        daemon=True
    )
    heartbeat_thread.start()

    # 4. 进入主操作循环
    while True:
        print("\n" + "=" * 40)
        print("请选择您要执行的操作:")
        print("  1. 上麦")
        # 您可以在这里继续添加更多操作...
        # print("  2. 下麦")
        # print("  3. 发送消息")
        print("  9. 退出房间 (结束程序)")
        print("=" * 40)

        choice = input("请输入选项编号: ")

        if choice == '1':
            print("\n--- 正在执行 [上麦] 操作... ---")
            user_api.on_mic(token=token, user_id=user_id)
        elif choice == '9':
            print("\n--- 正在执行 [退出房间] 操作... ---")
            user_api.exit_room(token=token, user_id=user_id)

            print("\n--- 正在停止后台心跳... ---")
            stop_heartbeat_event.set()
            heartbeat_thread.join(timeout=5)

            print("\n--- 程序已结束。感谢使用！ ---")
            break
        else:
            print("\n!!! 无效的选项，请重新输入。")


if __name__ == "__main__":
    main()