# !/usr/bin/env python

from xmlrpc.client import FastMarshaller
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template

from infer.application import Application

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
    serve.run(host="0.0.0.0", port=8000)
