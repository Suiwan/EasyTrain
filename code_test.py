import os

pwd = os.path.abspath(os.path.dirname(__file__))
print(pwd)
# 上一级
pwd = os.path.abspath(os.path.dirname(pwd))
print(pwd)

# checkpoints文件夹
checkpoints_path = pwd + "\\checkpoints"
print(checkpoints_path)

checkpoints_list = os.listdir(checkpoints_path)
# 过滤掉非文件夹
checkpoints_list = [x for x in checkpoints_list if os.path.isdir(checkpoints_path + "\\" + x)]
print(checkpoints_list)

res = {}
for x in checkpoints_list:
    # 获取checkpoints文件夹下的所有文件夹
    checkpoints_path = pwd + "\\checkpoints\\" + x
    checkpoints_list = os.listdir(checkpoints_path)
    temp = {}
    for y in checkpoints_list:
        # 获取checkpoints文件夹下的所有文件夹
        checkpoints_path = pwd + "\\checkpoints\\" + x + "\\" + y
        checkpoints_list = os.listdir(checkpoints_path)
        # 仅保留.pth文件
        checkpoints_list = [x for x in checkpoints_list if x.endswith('.pth')]
        temp[y] = checkpoints_list
    res[x] = temp

print(res)