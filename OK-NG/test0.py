import socket
import threading
import datetime
import time
import requests
import configparser
import JSONGenerator
import json
def determine_ng_ok():
    # time.sleep(20)
    cycle_num_max = requests.get('http://127.0.0.1:5000/get_cycle_num_max').json().get('cycle_num_max', 0)
    cycle_num = requests.get('http://127.0.0.1:5000/get_cycle_num').json().get('cycle_num', 0)
    print(f'时间：{datetime.datetime.now()}, cycle_num:{cycle_num}')

    if cycle_num < cycle_num_max:
        print('NG')
        total_result = 'NG'
    else:
        print('OK')
        total_result = 'OK'

    return total_result


def generate_and_update_json(barcode, total_result):
    image_name = []
    generator = JSONGenerator.JSONGenerator(barcode, total_result, image_name)
   
    # generated_json.update_total_result(total_result)
    frames_dirs = requests.get('http://127.0.0.1:5000/get_frame_dirs').json().get('frame_dirs', [])
    generator.update_total_result(total_result)
    frames_dirs = generator.convert_image_paths_to_dict(frames_dirs)
    generator.update_images(frames_dirs)
    generated_json = generator.generate_json()
    print(generated_json)
    return generated_json


response = requests.get('http://127.0.0.1:5000//reset_cycle_num')
# print(f'时间：{datetime.datetime.now()}, 客户端:{ip_port}, 数据:{data}')
data='0'
total_result = determine_ng_ok()
result_json = generate_and_update_json(data, total_result)
print(f'生成的JSON: {result_json}')
target_url = 'http://127.0.0.1:50000/api/detect'
headers = {'Content-Type': 'application/json'}
response = requests.post(target_url, data=json.dumps(result_json), headers=headers)
# Check the response
if response.status_code == 200:
    print("JSON data successfully sent to the target URL.")
else:
    print(f"Failed to send JSON data. Status code: {response.status_code}")


 

