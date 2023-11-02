from flask import Flask,render_template,jsonify,redirect,url_for

import json
from multiprocessing import Process
import time
import os
import subprocess
from apis.mmedu.config import *
from extensions import app,socketio





@app.route('/')
def index():
    return redirect(url_for('mmedu.index'),code=301)

@app.route('/basenn/')
def basenn():
    return render_template('basennPage.html')







# 离线轮询
# def poll_log():
#     global shared_data
#     time_stamp = shared_data.get('time_stamp', '')
#     last_line_num = 0
#     print("log_task"+time_stamp)
#     isRunning = shared_data.get('IsRunning', False)
#     log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\checkpoints\\" + f"{time_stamp}"
#     json_path = ""
#     while True:
#         json_files = [x for x in os.listdir(log_path) if x.endswith('.json')]
#         if len(json_files) != shared_data['train_times']: # 防止多次训练时，没读取到最新的日志文件
#             time.sleep(1)
#         else:
#             json_path = os.path.join(log_path, json_files[-1])
#             break
#     print("log_path",json_path)
#     while isRunning:
#         if os.path.exists(json_path):
#             with open(json_path, 'r') as f:
#                 lines = f.readlines()
#                 if len(lines) > last_line_num:
#                     for line in lines[last_line_num:]:
#                         log = json.loads(line)
#                         # to str
#                         log = json.dumps(log)
#                         shared_data['message'] = log
#                         print(log)
#                     last_line_num = len(lines)
#             time.sleep(1)
#     print("log_task end")


# 离线轮询
# @app.route('/get_message',methods=['GET'])
# def get_message():

#     global shared_data
#     log_data = shared_data['message']
#     return jsonify(log_data)
shared_data = {
    'message':None,
    'IsRunning':False,
    'time_stamp':'',
    'train_times':0
}

running_process = None

def train_task():
    global shared_data
    global running_process
    print("training_thread")
    shared_data['message'] = "正在训练 ……"
    running_process = subprocess.Popen(["..\env\python.exe","mmedu_code.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    running_process.communicate()
    shared_data['IsRunning'] = False


@socketio.on('log')
def poll_log_socket():
    global shared_data
    time_stamp = shared_data.get('time_stamp', '')
    last_line_num = 0
    print("log_task"+time_stamp)
    isRunning = shared_data.get('IsRunning', False)
    log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\checkpoints\\" +"mmedu_" +f"{time_stamp}"
    while True:
        json_files = [x for x in os.listdir(log_path) if x.endswith('.json')]
        if len(json_files) != shared_data['train_times']: # 防止多次训练时，没读取到最新的日志文件
            time.sleep(1)
        else:
            log_path = os.path.join(log_path, json_files[-1])
            break
    print("log_path",log_path)
    isRunning = shared_data['IsRunning']
    print("poll log is running?",isRunning)
    while isRunning:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > last_line_num:
                    for line in lines[last_line_num:]:
                        log = json.loads(line)
                        # to str
                        log = json.dumps(log)
                        shared_data['message'] = log
                        socketio.emit('log',log)
                        print(log)
                    last_line_num = len(lines)
            time.sleep(1)
        else:
            print("log_path not exist")
    print("log_task end")


@app.route('/mmedu/start_thread',methods=['GET'])
def start_thread():
    global shared_data
    shared_data['train_times'] += 1
    global running_process
    if running_process: #and running_process.poll() is None:
        return jsonify({'message': '已经有一个模型在训练'})
    else:
        shared_data['IsRunning'] = True
        if shared_data['IsRunning']:
            print("start_thread")
        running_process= Process(target=train_task)
        running_process.start()
        poll_log_socket()
        return jsonify({'message': '结束训练'})


@app.route('/mmedu/stop_thread',methods=['GET'])
def stop_thread():
    global shared_data
    shared_data['IsRunning'] = False
    global running_process
    if running_process: #and running_process.poll() is None:
        print("stop_thread")
        running_process.terminate()
        running_process = None
        shared_data['IsRunning']  = False
        if shared_data['IsRunning'] is False:
            print("stop_thread")
        return jsonify({'message': '已结束训练'})
    else:
        return jsonify({'message': '没有正在训练的模型'})


@app.route('/mmedu/get_code',methods=['GET'])
def get_code():
    global shared_data
    print("get_code")
    # make dir for checkpoints
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    checkpoints_path = back2pwd(__file__,1) + "\\EasyDL2.0\\checkpoints\\" + "mmedu_"+t
    print("checkpoints_path: ",checkpoints_path)
    os.mkdir(checkpoints_path)
    set_checkpoints_path(checkpoints_path=checkpoints_path)
    shared_data['time_stamp'] = t
    print("time_stamp",shared_data['time_stamp'])
    print(shared_data['time_stamp'])
    full_code = generate_code()
    return jsonify(full_code)



if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True,port=5000)