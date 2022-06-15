# !/usr/bin/env python

from xmlrpc.client import FastMarshaller
from flask import Flask
from flask_cors import CORS
from flask import request
from ..infer.application import Application
app = Flask(__name__)
CORS(app)

start = False

@app.route("/api/", methods=["GET"])
def hello_world():
  action = request.args.get("action")
  if action == "start":
    # 开启接收语音
    speaker = request.args.get("speaker")
    app.
  elif action == "stop":
    # 停止接收 开始处理 播放
    infer(audio)
    return {"status": 0, "message": "success!"}
  else:
    return {"status": 1, "message": "action error!"}


if __name__ == '__main__':
  app.run(port=8000,debug=True)
