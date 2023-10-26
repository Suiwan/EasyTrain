from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import os

app = Flask(__name__,static_url_path='/static')

from apis.mmedu import mmedu_bp

CORS(app)

socketio = SocketIO(app,cors_allowed_origins="*")

app.register_blueprint(mmedu_bp)


def back2pwd(pwd,level):
    """
    返回上`level`数级目录的绝对路径
    """
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd