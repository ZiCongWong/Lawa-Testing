# /common/yaml_handler.py

import yaml
import os

def read_yaml(file_path):
    """读取YAML文件"""
    # 获取当前脚本所在文件的绝对路径
    current_path = os.path.abspath(os.path.dirname(__file__))
    # 拼接完整的文件路径
    full_path = os.path.join(current_path, '..', file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

# 读取主配置文件
config_data = read_yaml('config/config.yml')