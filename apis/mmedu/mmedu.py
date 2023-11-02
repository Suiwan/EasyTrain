from . import mmedu_bp
from flask import render_template, request, jsonify
from .config import *
import json




def back2pwd(pwd,level):
    """
    返回上`level`数级目录的绝对路径
    """
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd




@mmedu_bp.route('/index')
def index():
    return render_template('mmeduPage.html',
                        task = global_varibles["task"],
                        model = global_varibles["model"],
                        lr = global_varibles["lr"],
                        epoch = global_varibles["epoch"],
                        batch_size = global_varibles["batch_size"],
                        dataset = global_varibles["dataset"])



@mmedu_bp.route('/select_task',methods=['POST'])
def select_task():
    if request.method == 'POST':
        task = request.json.get("task")
        print("task option",task)
        set_task(task=task)
        print("task now ",global_varibles["task"])
        response_data = {'message': '设置成功!', 'selected_option': task}
        return jsonify(response_data)
    

@mmedu_bp.route('/select_model',methods=['POST'])
def select_model():
    if request.method == 'POST':
        model = request.json.get("model")
        print("model option",model)
        set_model(model=model)
        print("model now ",global_varibles["model"])
        response_data = {'message': '设置成功!', 'selected_option': model}
        return jsonify(response_data)
    
@mmedu_bp.route('/select_dataset',methods=['POST'])
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


@mmedu_bp.route('/set_base_cfg',methods=['POST'])
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


@mmedu_bp.route('/set_advance_cfg',methods=['POST'])
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



@mmedu_bp.route('/get_local_dataset',methods=['GET'])
def get_local_dataset():
    if request.method == 'GET':
        print("getting_all_dataset")
        res = get_all_dataset()
        print(res)
        return jsonify(res)

@mmedu_bp.route('/get_local_pretrained_model',methods=['GET'])
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



@mmedu_bp.route('/get_epoch',methods=['GET'])
def get_epoch():
    global shared_data
    return jsonify({'epoch': global_varibles['epoch']})

@mmedu_bp.route('/get_checkpoints_path',methods=['GET'])
def get_checkpoints_path():
    global shared_data
    return jsonify({'checkpoints_path': global_varibles['checkpoints_path']})


