
from datetime import datetime
from JSONGenerator import JSONGenerator
import requests

data_received = False
cycle_num = 0
barcode = "0"
total_result = 'NG'
image_name = []


generator = JSONGenerator(barcode, total_result, image_name)
barcode = "data"
generated_json = generator.generate_json()
# generated_json.update_barcode(barcode)  # 更新JSONGenerator的barcode
# print(f'时间：{datetime.datetime.now()},数据:{barcode}')
response = requests.get('http://192.168.3.159:5000/reset_cycle_num')
while True:
    cycle_num = requests.get('http://192.168.3.159:5000/get_cycle_num').json().get('cycle_num', 0)
    print(f'时间：{datetime.now()},cycle_num:{cycle_num}')
    if cycle_num >= 6:
        frames_dirs = requests.get('http://192.168.3.159:5000/get_frame_dirs').json().get('frame_dirs', [])
        generator.update_total_result('OK')
        frames_dirs = generator.convert_image_paths_to_dict(frames_dirs)
        generator.update_images(frames_dirs)
        updated_json = generator.generate_json()

        print("\n更新后的JSON数据：")
        print(updated_json)

        break
