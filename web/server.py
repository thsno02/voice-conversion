# !/usr/bin/env python

from time import sleep
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template
app = Flask(__name__)
CORS(app)


@app.route("/api/", methods=["GET"])
def hello_world():
  action = request.args.get("action")
  # speaker = request.form.get("speaker")
  # print("speaker is "+speaker)

  if action == "start":
    # 开启接收语音
    # pass
    speaker = request.args.get("speaker")
    print("speaker is "+speaker)
    sleep(1)
    
    return {"status":0,"message":"success!"}
  elif action == "stop":
    # 停止接收 开始处理 播放
    return {"status": 0, "message": "success!"}
  else:
    return {"status": 1, "message": "action error!"}

@app.route('/')
def index():
  return render_template('play.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8000,debug=True)
