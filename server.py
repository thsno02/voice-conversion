# !/usr/bin/env python

from multiprocessing import Process
import socket

import pyqrcode
from PIL import Image
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from infer.application import Application


def draw_plot():
    # find the server address
    ip = socket.gethostbyname_ex(socket.gethostname())[-1][1]
    server_address = 'http://' + ip + ':8000'
    # draw qr code with highest error tolerance
    url = pyqrcode.QRCode(server_address, error='H')
    url.png('./src/qr_code.png', scale=10)
    im = Image.open('./src/qr_code.png')
    im = im.convert("RGBA")
    logo = Image.open('./src/mlogo.png')
    box = (135, 135, 235, 235)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    im.paste(region, box)
    im.show(title='QR Code')


serve = Flask(__name__)
CORS(serve)

app = Application()
print('Model has been initialized.')
print(f'id is {id(app)}')


@serve.route("/api/", methods=["GET"])
def hello_world():
    action = request.args.get("action")
    if action == "start":
        # app.speaker = 1
        # print('开始设置发音者')
        speaker = int(request.args.get("speaker"))
        # print(speaker)
        if app.verify_speaker(speaker):
            app.speaker = speaker
        else:
            return {"status": 1, "message": "action error!"}
        # print('成功设置发音者')
        # print('开始录音')
        app.start()
        return {"status": 0, "message": "开始!"}
    elif action == "stop":
        # 停止接收 开始处理 播放
        # print('停止录音')
        app.stop()
        # print('开始推理')
        app.infer()
        # print('结束推理\n')
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
