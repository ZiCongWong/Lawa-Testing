import pytest
from api import user_api
from common.yaml_handler import config_data


@pytest.fixture(scope="session")
def login_session():
    """
    执行登录操作，并返回Token。
    """
    print("\n--- 开始执行登录操作 ---")
    mobile = config_data['user_credentials']['mobile']
    password = config_data['user_credentials']['password']  # 这里获取的是原始密码

    # 调用更新后的登录接口
    response = user_api.login(mobile, password)
    data = response.json()

    assert data["code"] == 200,f"登录失败，响应内容: {response.text}"

    try:
        # 请根据你API的实际返回结构修改这里的路径
        login_data = data['data']
        print(f"--- 登录成功，获取会话数据: {login_data} ---")
        return login_data
    except (KeyError, TypeError) as e:
        pytest.fail(f"无法从登录响应中提取会话数据。错误: {e}，响应内容: {response.text}")


