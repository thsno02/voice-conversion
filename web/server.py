# !/usr/bin/env python

from flask import Flask
from flask_cors import CORS
from flask import request
app = Flask(__name__)
CORS(app)


@app.route("/api/", methods=["GET"])
def hello_world():
  action = request.args.get("action")
  if action == "start":
    # 开启接收语音
    # pass
    speaker = request.args.get("speaker")
    
    return {"status":0,"message":"success!"}
  elif action == "stop":
    # 停止接收 开始处理 播放
    return {"status": 0, "message": "success!"}
  else:
    return {"status": 1, "message": "action error!"}


if __name__ == '__main__':
  app.run(port=8000,debug=True)
