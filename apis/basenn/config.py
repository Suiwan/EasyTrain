
import os


def back2pwd(pwd,level):
    """
    返回上`level`数级目录的绝对路径
    """
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd


global_varibles = {
    "dataset":"hand_gray",
    "dataset_path": back2pwd(__file__,3) + "\\dataset\\hand_gray",
    "checkpoints_path": back2pwd(__file__,3) + "\\checkpoints", # save fold path
    "lr": 0.01,
    "epochs": 10,
    "network": [], # 网络结构，e.g.{"id":1, "name":'linear;,"size":(784,10),"activation":'relu'}
    "pretrained_path": None,
    "metrics": ["acc"], # options: acc mae mse
    "loss":"CrossEntropyLoss", # options: CrossEntropyLoss MSELoss L1Loss……
    "random_seed": 42,

}


def set_global_network(network):
    global_varibles["network"] = network

def set_dataset_path(dataset_path):
    global_varibles["dataset_path"] = dataset_path

def set_checkpoints_path(checkpoints_path):
    global_varibles["checkpoints_path"] = checkpoints_path

def set_lr(lr):
    global_varibles["lr"] = lr

def set_epochs(epochs):
    global_varibles["epochs"] = epochs


def set_metrics(metrics):
    global_varibles["metrics"] = metrics

def set_loss(loss):
    global_varibles["loss"] = loss

def set_random_seed(random_seed):
    global_varibles["random_seed"] = random_seed

def set_dataset(dataset):
    global_varibles["dataset"] = dataset

def update_global_varibles(**kwargs):
    for k,v in kwargs.items():
        global_varibles[k] = v
    print("global_varibles now ",global_varibles)
    return True

def update_pretrained_path(pretrained):
    pwd = back2pwd(__file__,3) 
    pretrained_path = pwd + "\\checkpoints\\" + global_varibles['dataset'] + "\\" + pretrained
    global_varibles['pretrained_path'] = pretrained_path

def update_dataset_path():
    global_varibles["dataset_path"] = back2pwd(__file__,3) + "\\dataset\\" + global_varibles["dataset"]