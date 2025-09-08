#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from datetime import datetime
from common.database_handler import DatabaseHandler
from common.logger import logger


def format_datetime(dt_str):
    """格式化日期时间字符串"""
    try:
        if isinstance(dt_str, str):
            # 尝试解析不同格式的日期时间
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']:
                try:
                    return datetime.strptime(dt_str, fmt).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
        return str(dt_str)
    except:
        return str(dt_str)


def display_records(records, limit=10):
    """显示记录"""
    if not records:
        print("没有找到符合条件的记录")
        return
    
    print(f"\n找到 {len(records)} 条记录")
    print("=" * 80)

def export_to_json(records, filename=None):
    """导出记录到JSON文件"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"user_asset_logs_{timestamp}.json"
    
    try:
        # 处理日期时间字段
        processed_records = []
        for record in records:
            processed_record = {}
            for key, value in record.items():
                if 'time' in key.lower() or 'date' in key.lower():
                    processed_record[key] = format_datetime(value)
                else:
                    processed_record[key] = value
            processed_records.append(processed_record)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(processed_records, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据已导出到文件: {filename}")
        return filename
    except Exception as e:
        print(f"导出文件失败: {e}")
        return None


def main():
    """主程序"""
    print("=" * 60)
    print("数据库数据读取程序")
    print("目标: 读取voice.t_user_asset_log_202509表中userId=1000120的记录")
    print("=" * 60)
    
    # 创建数据库处理器
    db_handler = DatabaseHandler()
    
    try:
        # 连接数据库
        print("\n正在连接数据库...")
        if not db_handler.connect():
            print("数据库连接失败，程序退出")
            return
        
        start_ts = input("请输入起始时间戳（秒）: ").strip()
        if not start_ts.isdigit():
            print("请输入有效的时间戳（数字，单位：秒）")
            return
        start_ts = int(start_ts)
        # 查询指定用户的记录
        target_user_id = 1000120
        print(f"\n正在查询用户ID为 {target_user_id} 的记录...")
        
        records = db_handler.get_user_asset_logs(target_user_id, start_ts=start_ts)
        
        if records:
            # 显示记录
            display_records(records, limit=5)
            count_num_occurrences(records)
            
            # 询问是否导出
            export_choice = input(f"\n是否导出所有 {len(records)} 条记录到JSON文件? (y/n): ")
            if export_choice.lower() in ['y', 'yes', '是']:
                export_to_json(records)
        else:
            print(f"未找到用户ID为 {target_user_id} 的记录")
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        print(f"程序执行出错: {e}")
    finally:
        # 关闭数据库连接
        db_handler.disconnect()
        print("\n程序结束")

# 分类统计num字段出现次数的函数
def count_num_occurrences(records):
    """
    对记录中的num字段进行分类统计，返回每种num出现的次数
    """
    from collections import Counter
    num_list = [record.get('num') for record in records if 'num' in record]
    num_counter = Counter(num_list)
    print("\n各num数值出现次数统计：")
    for num_value, count in num_counter.items():
        print(f"num = {num_value} 出现 {count} 次")
    return num_counter

# 在main函数中查询到records后，调用统计函数
# 你可以在显示记录后调用
# 例如：
# if records:
#     display_records(records, limit=5)
#     count_num_occurrences(records)
#     ...


if __name__ == "__main__":
    main()
