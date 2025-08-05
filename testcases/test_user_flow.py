import pytest
from api import user_api


class TestUserFlow:

    def test_enter_room_success(self, login_session):
        """
        测试获取用户信息成功场景
        :param login_token: pytest会自动将conftest.py中login_token的返回值注入到这里
        """
        # 直接使用从fixture中获取的token
        # 1. 从登录会话中提取所需信息
        token = login_session['token']
        user_id = login_session['userId']

        # 调用需要token的接口
        response = user_api.enter_room(token,user_id)
        data = response.json()

        # --- 断言 ---
        # 1. 检查HTTP状态码
        assert data['code'] == 200

        # 2. 检查响应体内容
        assert 'userId' in data['data']  # <--- 根据你的API实际返回结构修改

    def test_another_feature(self, login_token):
        """
        测试另一个需要登录才能访问的功能
        """
        # token = login_token
        # response = some_other_api.do_something(token, ...)
        # assert ...
        # (在此添加你的其他测试)
        pass  # 暂时跳过