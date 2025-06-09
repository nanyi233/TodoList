import json
import os
from datetime import datetime

def read_data(file_path):
    """读取JSON数据文件"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data, file_path):
    """写入JSON数据文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_task(task_data, tasks_file='data/tasks.json'):
    """添加新任务"""
    tasks = read_data(tasks_file)
    # 为新任务添加ID和时间戳
    new_id = max([task.get('id', 0) for task in tasks], default=0) + 1
    task_data.update({
        'id': new_id,
        'created_at': datetime.now().isoformat(),
        'status': 'pending'  # pending, in_progress, completed
    })
    tasks.append(task_data)
    write_data(tasks, tasks_file)
    return task_data
