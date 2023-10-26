import os 

# print(pwd_3)

def back2pwd(pwd,level):
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd


print(back2pwd(__file__,3))