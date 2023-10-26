from . import mmedu_bp
from flask import render_template, request, jsonify
from config import *


@mmedu_bp.route('/test')
def test():
    return 'mmedu test'



@mmedu_bp.route('/')
def index():
    return render_template('train_page.html',
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

