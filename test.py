
import os


def back2pwd(pwd,level):
    """
    返回上`level`数级目录的绝对路径
    """
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd

def get_all_dataset():
    dataset_list = []
    pwd = back2pwd(__file__,1) + "\\dataset\\basenn"
    dirs = os.listdir(pwd)
    # print(dirs)
    for dir in dirs:
        for file in os.listdir(os.path.join(pwd,dir)):
            # print(os.path.join(pwd,dir,file))
            if os.path.isfile(os.path.join(pwd,dir,file)):
                dataset_list.append(os.path.join(dir,file))
    print(dataset_list)




get_all_dataset()