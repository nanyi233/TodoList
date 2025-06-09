from flask import Flask, request, jsonify, send_from_directory
import os
from utils.file_handler import read_data, write_data, add_task
from datetime import datetime  # 补充缺失的导入

app = Flask(__name__)

# 确保数据目录存在
os.makedirs('data', exist_ok=True)

@app.route('/')
@app.route('/index.html')  # 添加新路由，使 /index.html 也指向主页
def index():
    """返回主页面"""
    return send_from_directory('templates', 'index.html')

@app.route('/todolist.html')
def todolist():
    """返回今日待办页面"""
    return send_from_directory('templates', 'todolist.html')

@app.route('/records.html')
def records():
    """返回记录表页面"""
    return send_from_directory('templates', 'records.html')

@app.route('/activityInventory.html')
def activity_inventory():
    """返回活动清单页面"""
    return send_from_directory('templates', 'activityInventory.html')

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    """任务列表API（GET获取所有任务，POST创建新任务）"""
    if request.method == 'GET':
        tasks = read_data('data/tasks.json')
        return jsonify(tasks)
    elif request.method == 'POST':
        new_task = request.json
        task = add_task(new_task)
        return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task_detail(task_id):
    """任务详情API（PUT更新任务，DELETE删除任务）"""
    tasks = read_data('data/tasks.json')
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'PUT':
        updated_task = request.json
        for key, value in updated_task.items():
            task[key] = value
        write_data(tasks, 'data/tasks.json')
        return jsonify(task)

    elif request.method == 'DELETE':
        tasks.remove(task)
        write_data(tasks, 'data/tasks.json')
        return jsonify({'success': True})

@app.route('/api/pomodoro', methods=['POST'])
def start_pomodoro():
    """开始番茄钟"""
    # 这里可以实现番茄钟的逻辑
    # 例如记录开始时间、任务ID等
    pomodoro_data = request.json
    # 保存到文件
    pomodoros = read_data('data/pomodoro.json')
    pomodoros.append({
        'id': len(pomodoros) + 1,
        'task_id': pomodoro_data.get('task_id'),
        'start_time': datetime.now().isoformat(),
        'duration': pomodoro_data.get('duration', 25)  # 默认为25分钟
    })
    write_data(pomodoros, 'data/pomodoro.json')
    return jsonify({'status': 'started'})

# 新增路由处理图片文件访问
@app.route('/Image/<path:filename>')
def serve_image(filename):
    return send_from_directory('Image', filename)

if __name__ == '__main__':
    app.run(debug=True)