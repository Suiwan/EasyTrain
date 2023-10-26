from flask import Flask,render_template,Response,request,jsonify,Blueprint,redirect,url_for
from config import *
import json
from multiprocessing import Process,Queue,Event
import time
import os
import subprocess

from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__,static_url_path='/static')

from apis.mmedu import mmedu_bp

app.register_blueprint(mmedu_bp)



CORS(app)
socketio = SocketIO(app,cors_allowed_origins="*")

# @app.route('/')
# def index():
#     return render_template('train_page.html',
#                             task = global_varibles["task"],
#                             model = global_varibles["model"],
#                             lr = global_varibles["lr"],
#                             epoch = global_varibles["epoch"],
#                             batch_size = global_varibles["batch_size"],
#                             dataset = global_varibles["dataset"])

@app.route('/')
def index():
    return redirect(url_for('mmedu.index'))

@app.route('/basenn')
def basenn():
    return render_template('train_basenn.html')

@app.route('/get_local_dataset',methods=['GET'])
def get_local_dataset():
    if request.method == 'GET':
        print("getting_all_dataset")
        res = get_all_dataset()
        print(res)
        return jsonify(res)

@app.route('/get_local_pretrained_model',methods=['GET'])
def get_local_pretrained_model():
    if request.method == 'GET':
        print("getting_local_pretrained_model")
        pretrained_models = get_all_pretrained_model()
        if global_varibles['task'] == 'classification':
            res = pretrained_models['cls_model']
            # 根据dataset_path的最后一个文件夹名字，获取对应的预训练模型
            dataset_path = global_varibles['dataset_path']
            dataset_name = dataset_path.split('\\')[-1]
            model_list = res[dataset_name]
            print(model_list)
            return jsonify(model_list)
        elif global_varibles['task'] == 'detection':
            res = pretrained_models['det_model']
            # 根据dataset_path的最后一个文件夹名字，获取对应的预训练模型
            dataset_path = global_varibles['dataset_path']
            dataset_name = dataset_path.split('\\')[-1]
            model_list = res[dataset_name]  # note: 安装包中的dataset名字与预训练模型中的文件夹名字需要保持一致
            print(model_list)
            return jsonify(model_list)


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
    running_process = subprocess.Popen(["..\env\python.exe","generated_code.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    running_process.communicate()
    shared_data['IsRunning'] = False


def poll_log():
    global shared_data
    time_stamp = shared_data.get('time_stamp', '')
    last_line_num = 0
    print("log_task"+time_stamp)
    isRunning = shared_data.get('IsRunning', False)
    log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\checkpoints\\" + f"{time_stamp}"
    json_path = ""
    while True:
        json_files = [x for x in os.listdir(log_path) if x.endswith('.json')]
        if len(json_files) != shared_data['train_times']: # 防止多次训练时，没读取到最新的日志文件
            time.sleep(1)
        else:
            json_path = os.path.join(log_path, json_files[-1])
            break
    print("log_path",json_path)
    while isRunning:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > last_line_num:
                    for line in lines[last_line_num:]:
                        log = json.loads(line)
                        # to str
                        log = json.dumps(log)
                        shared_data['message'] = log
                        print(log)
                    last_line_num = len(lines)
            time.sleep(1)
    print("log_task end")

@socketio.on('log')
def poll_log_socket():
    global shared_data
    time_stamp = shared_data.get('time_stamp', '')
    last_line_num = 0
    print("log_task"+time_stamp)
    isRunning = shared_data.get('IsRunning', False)
    log_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\checkpoints\\" + f"{time_stamp}"
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


@app.route('/get_message',methods=['GET'])
def get_message():
    global shared_data
    log_data = shared_data['message']
    return jsonify(log_data)


@app.route('/start_thread',methods=['GET'])
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

@app.route('/stop_thread',methods=['GET'])
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

@app.route('/select_task',methods=['POST'])
def select_task():
    if request.method == 'POST':
        task = request.json.get("task")
        print("task option",task)
        set_task(task=task)
        print("task now ",global_varibles["task"])
        response_data = {'message': '设置成功!', 'selected_option': task}
        return jsonify(response_data)

@app.route('/select_model',methods=['POST'])
def select_model():
    if request.method == 'POST':
        model = request.json.get("model")
        print("model option",model)
        set_model(model=model)
        print("model now ",global_varibles["model"])
        response_data = {'message': '设置成功!', 'selected_option': model}
        return jsonify(response_data)
    
@app.route('/select_dataset',methods=['POST'])
def select_dataset():
    if request.method == 'POST':
        dataset = request.json.get("dataset")
        print("dataset option",dataset)
        set_dataset(dataset=dataset)
        print("dataset now ",global_varibles["dataset"])
        update_dataset_path()
        print("dataset_path now ",global_varibles["dataset_path"])
        response_data = {'message': '设置成功!', 'selected_option': dataset}
        return jsonify(response_data)



@app.route('/get_epoch',methods=['GET'])
def get_epoch():
    global shared_data
    return jsonify({'epoch': global_varibles['epoch']})

@app.route('/get_checkpoints_path',methods=['GET'])
def get_checkpoints_path():
    global shared_data
    return jsonify({'checkpoints_path': global_varibles['checkpoints_path']})


@app.route('/get_code',methods=['GET'])
def get_code():
    global shared_data
    print("get_code")
    # make dir for checkpoints
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    checkpoints_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\checkpoints\\" + t
    print("checkpoints_path: ",checkpoints_path)
    os.mkdir(checkpoints_path)
    set_checkpoints_path(checkpoints_path=checkpoints_path)
    shared_data['time_stamp'] = t
    print("time_stamp",shared_data['time_stamp'])
    print(shared_data['time_stamp'])
    full_code = generate_code()
    return jsonify(full_code)


@app.route('/set_base_cfg',methods=['POST'])
def set_base_config():
    # 从前端接收form表单数据
    lr = request.form['lr']
    batch_size = request.form['batch_size']
    epoch = request.form['epoch']
    random_seed = request.form['random_seed']
    set_lr(lr=lr)
    # set_batch_size(batch_size=batch_size)
    set_epoch(epoch=epoch)
    set_random_seed(random_seed=random_seed)
    print("set_config")
    print(global_varibles)
    response_data = {'message': '设置成功!'}
    return jsonify(response_data)


@app.route('/set_advance_cfg',methods=['POST'])
def set_advance_config():
    request_data = json.loads(request.data)
    optimizer = request_data['optimizer']
    weight_decay = request_data['weight_decay']
    class_num = request_data['class_num']
    device = request_data['device']
    pretrained_model = request_data['pretrained_model']
    if class_num != "":
        class_num = int(class_num)
        set_class_num(class_num=class_num)
    if weight_decay != "":
        weight_decay = float(weight_decay)
        set_weight_decay(weight_decay=weight_decay)
    set_optimizer(optimizer=optimizer)
    set_device(device=device)
    update_pretrained_path(pretrained_model=pretrained_model)
    print(global_varibles)
    return jsonify({'message': '设置成功!'})

if __name__ == '__main__':
    app.run(debug=True,port=5000)