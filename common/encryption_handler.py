import hashlib
import time
import json
from common.yaml_handler import config_data

# 从配置文件获取salt/secret
API_SALT = config_data['api_salt']


def get_password_md5(password):
    """计算密码的MD5值"""
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def get_current_timestamp_s():
    """获取当前的10位秒级时间戳"""
    return int(time.time())


def generate_signature(params: dict = None, body: dict = None):

    param_str = ""
    if params:
        sorted_params = sorted(params.items())
        param_str = "".join([f"{k}={v}" for k, v in sorted_params])


    body_str = ""
    if body:
        # ★★★ 修复点: 移除 separators 参数，生成带标准空格的JSON字符串
        body_str = json.dumps(body)
    timestamp_s = str(get_current_timestamp_s())
    string_to_sign = f"{param_str}{body_str}{timestamp_s}"
    final_string_for_md5 = f"{API_SALT}{string_to_sign}{API_SALT}"
    sign_header_value = hashlib.md5(final_string_for_md5.encode('utf-8')).hexdigest()
    dynamic_headers = {
        'time': timestamp_s,
        'sign': sign_header_value
    }

    return dynamic_headers

