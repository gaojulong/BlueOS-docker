#!/usr/bin/env python3
import os
from flask import Flask, request
import json
import configparser

base_dir = os.path.dirname(__file__)
app = Flask(__name__)
config_path = os.path.join(base_dir, 'configurations.ini') 
# path = r'configurations.ini'
# CREATE OBJECT
config = configparser.ConfigParser()
config.read(config_path)
config_video_url = config['ROVSettings']['config_video_url']
config_version = config['ROVSettings']['config_version']
config_machine_type = config['ROVSettings']['config_machine_type']


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    result = {}
    content = {}
    if request.method == 'GET':
        result['code'] = "ok"
        content["version"] = config_version
        content["video_url"] = config_video_url
        content["machine_type"] = config_machine_type
        result['content'] = content
        return json.dumps(result)
    else:
        result['code'] = "ok"
        json_data = request.json
        print(type(json_data))
        try:
            config.set("ROVSettings", "config_video_url", json_data["video_url"])
            config.set("ROVSettings", "config_version", json_data["version"])
            config.set("ROVSettings", "config_machine_type", json_data["machine_type"])
        except Exception as e:
            result['code'] = "error"
            return json.dumps(result)
        with open(r"configurations.ini", 'w') as configfileObj:
            config.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()
        return json.dumps(result)


# @app.route('/video_url', methods=['GET', 'POST'])
# @app.route('/video_url/', methods=['GET', 'POST'])
# def video_url():
#     result = {}
#     if request.method == 'GET':
#         result['code'] = "ok"
#         result['content'] = config_video_url
#         # return 'rtsp://192.168.2.3:8080/video'
#         print(result)
#         return json.dumps(result)
#     else:
#         content = request.form.get('content')
#         print(content)
#         config.set("ROVSettings", "config_video_url", content)
#         with open(r"configurations.ini", 'w') as configfileObj:
#             config.write(configfileObj)
#             configfileObj.flush()
#             configfileObj.close()
#         return "ok"
#
#
# @app.route('/version', methods=['GET', 'POST'])
# @app.route('/version/', methods=['GET', 'POST'])
# def version():
#     result = {}
#     if request.method == 'GET':
#         result['code'] = "ok"
#         result['content'] = config_version
#         print(result)
#         return json.dumps(result)
#     else:
#         result['code'] = "ok"
#         content = request.form.get('content')
#         config.set("ROVSettings", "config_version", content)
#         with open(r"configurations.ini", 'w') as configfileObj:
#             config.write(configfileObj)
#             configfileObj.flush()
#             configfileObj.close()
#         return json.dumps(result)
#
#
# @app.route('/machine_type', methods=['GET', 'POST'])
# @app.route('/machine_type/', methods=['GET', 'POST'])
# def machinetype():
#     result = {}
#     if request.method == 'GET':
#         result['code'] = "ok"
#         result['content'] = config_machine_type
#         # return 'rtsp://192.168.2.3:8080/video'
#         print(result)
#         return json.dumps(result)
#     else:
#         result['code'] = "ok"
#         content = request.form.get('content')
#         print(content)
#         config.set("ROVSettings", "config_machine_type", content)
#         with open(r"configurations.ini", 'w') as configfileObj:
#             config.write(configfileObj)
#             configfileObj.flush()
#             configfileObj.close()
#         return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10001)
