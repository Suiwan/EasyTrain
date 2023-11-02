from . import basenn_bp
from flask import render_template, jsonify,request
from .config import *
import json


@basenn_bp.route('/test')
def test():
    return jsonify({'message': 'test success!'})


@basenn_bp.route('/dataset',methods=['GET'])
def dataset():
    return render_template('dataset.html')


@basenn_bp.route('/set_network',methods=['POST'])
def set_network():
    if request.method == 'POST':
        networks = request.json.get("network")
        print("network option",networks)
        # 处理一下网络结构
        network = {}
        network_list = []
        for n in networks:
            network["id"] = n["id"]
            network["type"] = n["type"]
            network["activation"] = n["activation"]
            inputSize = int(n["inputSize"])
            outputSize = int(n["outputSize"])
            network["size"] = (inputSize,outputSize)
            network_list.append(network)
        set_global_network(network=network_list)
        print("network now ",global_varibles["network"])
        # set_network(network=network)
        # print("network now ",global_varibles["network"])
        response_data = {'message': '设置成功!', 'success': True}
        return jsonify(response_data)
    


@basenn_bp.route('/set_base_cfg',methods=['POST'])
def set_base_cfg():
    if request.method == 'POST':
        lr = request.form['lr']
        epochs = request.form['epochs']
        random_seed = request.form['random_seed']
        if update_global_varibles(lr=lr,epochs=epochs,random_seed=random_seed):
            response_data = {'message': '设置成功!', 'success': True}
        else:
            response_data = {'message': '设置失败!', 'success': False}
        return jsonify(response_data)
    

@basenn_bp.route('/set_advance_cfg',methods=['POST'])
def set_advance_cfg():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        loss = request_data["loss"]
        metrics = request_data["metrics"]
        pretrained = request_data["pretrained"]
        set_loss(loss=loss)
        set_metrics(metrics=metrics)
        if pretrained != "None":
            update_pretrained_path(pretrained=pretrained)
        print("global_varibles now ",global_varibles)
    
    return jsonify({'message': '设置成功!', 'success': True})