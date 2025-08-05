import time
import threading
from api import user_api
from common.yaml_handler import config_data


class UserSession:
    """封装单个用户的状态和行为"""

    def __init__(self, user_config):
        self.mobile = user_config['mobile']
        self.password = user_config['password']
        self.device = user_config['device']
        self.token = None
        self.user_id = None
        self.heartbeat_thread = None
        self.stop_event = threading.Event()

    def login(self):
        """为该用户执行登录"""
        print(f"--- 正在为用户 {self.mobile} 登录... ---")
        response = user_api.login(self.mobile, self.password, self.device)
        if response.status_code == 200 and response.json().get('success'):
            data = response.json()['data']
            self.token = data['token']
            self.user_id = data['userId']
            print(f"--- 用户 {self.mobile} 登录成功! (UserID: {self.user_id}) ---")
            return True
        print(f"!!! 用户 {self.mobile} 登录失败: {response.text}")
        return False

    def enter_room(self):
        """进入房间"""
        print(f"--- 用户 {self.user_id} 正在进入房间... ---")
        response = user_api.enter_room(self.token, self.user_id, self.device)
        return response.status_code == 200 and response.json().get('success')

    def start_heartbeat(self):
        """启动该用户的后台心跳"""
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker,
            daemon=True
        )
        self.heartbeat_thread.start()

    def _heartbeat_worker(self):
        print(f"\n>>> [心跳线程-{self.user_id}]: 已启动")
        while not self.stop_event.is_set():
            user_api.room_heartbeat(self.token, self.user_id, self.device)
            user_api.mic_heartbeat(self.token, self.user_id, self.device)
            self.stop_event.wait(30)
        print(f"\n>>> [心跳线程-{self.user_id}]: 已停止")

    def stop_heartbeat(self):
        """停止心跳"""
        self.stop_event.set()
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)

    def on_mic(self, seat_index):
        # ★★★ 已按你的要求更新 ★★★
        user_api.on_mic(self.token, self.user_id, self.device, seat_index)

    def exit_room(self):
        user_api.exit_room(self.token, self.user_id, self.device)
        self.stop_heartbeat()


def main():
    """主交互流程"""
    active_sessions = []

    # 1. 初始化并登录所有用户
    print("=" * 50)
    print("程序启动，正在初始化所有用户...")
    for user_config in config_data['users']:
        session = UserSession(user_config)
        if session.login() and session.enter_room():
            session.start_heartbeat()
            active_sessions.append(session)
        else:
            print(f"!!! 初始化用户 {user_config['mobile']} 失败，已跳过。")

    if not active_sessions:
        print("!!! 没有任何用户成功初始化，程序退出。")
        return

    # 2. 进入主操作循环
    while True:
        print("\n" + "=" * 50)
        print("当前在线用户:")
        for i, session in enumerate(active_sessions):
            print(f"  {i + 1}. 用户ID: {session.user_id} (手机号: {session.mobile})")
        print("  q. 退出所有用户并结束程序")
        print("-" * 50)

        user_choice = input("请选择要操作的用户编号 (或输入'q'退出): ")

        if user_choice.lower() == 'q':
            break

        try:
            user_index = int(user_choice) - 1
            if not 0 <= user_index < len(active_sessions):
                raise ValueError
            selected_session = active_sessions[user_index]
        except ValueError:
            print("\n!!! 无效的用户编号，请重新输入。")
            continue

        # 3. 针对选定用户的操作菜单
        while True:
            print("\n" + "-" * 50)
            print(f"当前操作用户: {selected_session.user_id}")
            print("  1. 上麦")
            print("  9. 退出房间")
            print("  b. 返回用户选择菜单")
            print("-" * 50)

            action_choice = input("请输入操作编号: ")

            if action_choice == '1':
                # ★★★ 已按你的要求更新 ★★★
                while True:
                    try:
                        seat_input = input("请输入要上的麦位号 (例如: 2): ")
                        seat_index = int(seat_input)
                        selected_session.on_mic(seat_index)
                        break
                    except ValueError:
                        print("!!! 输入无效，请输入一个数字。")

            elif action_choice == '9':
                selected_session.exit_room()
                active_sessions.pop(user_index)
                print(f"--- 用户 {selected_session.user_id} 已退出房间并离线。 ---")
                if not active_sessions:
                    print("--- 所有用户均已离线。 ---")
                break  # 返回用户选择菜单
            elif action_choice.lower() == 'b':
                break  # 返回用户选择菜单
            else:
                print("\n!!! 无效的操作编号，请重新输入。")

        if not active_sessions:
            break  # 如果所有用户都退出了，结束主循环

    # 4. 结束程序
    print("\n--- 正在清理所有剩余会话并退出程序... ---")
    for session in active_sessions:
        session.exit_room()
    print("--- 程序已安全退出。 ---")


if __name__ == "__main__":
    main()
