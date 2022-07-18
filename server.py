# !/usr/bin/env python

from multiprocessing import Process

from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from infer.application import Application


def draw_plot():
    """
    draw QR code
    """
    # hide toolbar
    plt.rcParams['toolbar'] = 'None'
    # enbable Chinese
    plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签

    img = mpimg.imread('qrcode.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.title('请扫码')
    plt.ioff()
    plt.show()


serve = Flask(__name__)
CORS(serve)

app = Application()
print('模型已初始化。')
print(f'id is {id(app)}')


@serve.route("/api/", methods=["GET"])
def hello_world():
    action = request.args.get("action")
    if action == "start":
        # app.speaker = 1
        print('开始设置发音者')
        speaker = int(request.args.get("speaker"))
        print(speaker)
        if app.verify_speaker(speaker):
            app.speaker = speaker
        else:
            return {"status": 1, "message": "action error!"}
        print('成功设置发音者')
        print('开始录音')
        app.start()
        return {"status": 0, "message": "开始!"}
    elif action == "stop":
        # 停止接收 开始处理 播放
        print('停止录音')
        app.stop()
        print('开始推理')
        app.infer()
        print('结束推理\n')
        return {"status": 0, "message": "结束!"}
    else:
        return {"status": 1, "message": "action error!"}


@serve.route("/")
def index():
    return render_template("play.html")


if __name__ == '__main__':
    # draw qr code
    p = Process(target=draw_plot)
    p.start()
    serve.run(host="0.0.0.0", port=8000)
