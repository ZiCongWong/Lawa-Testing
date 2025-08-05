# /run.py

import pytest
import os
from datetime import datetime

if __name__ == '__main__':
    # 定义报告文件名，包含时间戳
    report_name = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path = os.path.join('reports', report_name)

    # 确保reports目录存在
    if not os.path.exists('reports'):
        os.makedirs('reports')

    print(f"测试开始，报告将生成在: {report_path}")

    # 运行pytest主函数
    # --html=... : 指定pytest-html插件生成报告的路径
    # -v : 输出更详细的日志
    # -s : 显示测试函数中的print输出
    # testcases/ : 指定要运行的测试用例目录
    pytest.main([
        f"--html={report_path}",
        "-v",
        "-s",
        "testcases/"
    ])

    print(f"测试完成，请查看报告: {report_path}")