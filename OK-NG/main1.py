import socket
import threading
import datetime
import time
import requests
import JSONGenerator
import json
import configparser
import concurrent.futures
import requests

# 开始录制接口
def start_record(barcode):
    url = "http://localhost:8001/start_record/"+barcode
    # data = {"条码": barcode
    response = requests.get(url)
    if response.status_code == 200:
        print("开始录制成功")
    else:
        print("开始录制失败", response.status_code, response.text)

# 结束录制接口
def end_record(result):
    url = "http://localhost:8001/end_record/"+result
    # data = {"检测结果": result}
    response = requests.get(url)
    if response.status_code == 200:
        print("结束录制成功")
    else:
        print("结束录制失败", response.status_code, response.text)

# 示例用法
# start_record("123456789") 
# end_record("OK")           # 或者 "NG"

def read_config_values(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    # Reading max_delay and cycle_num_max from the [YOLO] section
    max_delay = config.getint('YOLO', 'max_delay')
    cycle_num_max = config.getint('YOLO', 'cycle_num_max')
    
    return max_delay, cycle_num_max

def udp(host, port):
    print(f"时间：{datetime.datetime.now()}, udp接收已启动，地址{host}，端口{port}")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 44556))
    while True:
        recv_data, client_address = udp_socket.recvfrom(1024)
        print(f"时间：{datetime.datetime.now()}, 地址：{client_address}，数据：{recv_data.decode()}")


def tcp(host, port):
    print(f"时间：{datetime.datetime.now()}, tcp服务端已启动，地址{host}，端口{port}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((host, port))
    server_socket.listen(128)
    while True:
        client_socket, ip_port = server_socket.accept()
        t_client = threading.Thread(target=tcp_client_task, args=(client_socket, ip_port))
        t_client.start()
detect = False
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

def tcp_client_task(client_socket, ip_port):
    print(f'时间：{datetime.datetime.now()}, 客户端:{ip_port}加入连接')

    while True:
        try:
            data = client_socket.recv(1024).decode('gbk')
            start_record(data)
            if len(data) != 0:
                global detect 
                detect = False
                print(f'时间：{datetime.datetime.now()}, 客户端:{ip_port}, 数据:{data}') 
    
                # Check if there are active threads in the thread pool
                # if len(executor._threads) > 0:
                    # executor.shutdown_now()
                # time.sleep(0.01)

                executor.submit(count_ok_ng,True, data)

                
                # try:
                #     response = requests.get('http://127.0.0.1:5000/reset_cycle_num')
                #     requests.get('http://127.0.0.1:5000//reset_counters')
                #     response.raise_for_status()
                # except requests.RequestException as e:
                #     print(f"重置循环计数请求失败: {e}")
                #     continue
                
                # print(f'时间：{datetime.datetime.now()}, 客户端:{ip_port}, 数据:{data}') 
                # time1 = datetime.datetime.now().timestamp()
                # while True:
                #     time.sleep(0.01)
                #     total_result = determine_ng_ok()
                #     # time2= datetime.datetime.now()
                #     if (datetime.datetime.now().timestamp() - time1) > max_delay:
                #         total_result='NG'
                #         print('chaoshi')
                #         break
                #     if total_result!=[]:
                #         print('buguifan或ok')
                #         break
                    
                
                # generated_json = generate_and_update_json(data, total_result)
                # print(f'生成的JSON: {generated_json}')
                # target_url = 'http://127.0.0.1:46006/api/detect'
                # headers = {'Content-Type': 'application/json'}
                # try:
                #     response = requests.post(target_url, data=generated_json, headers=headers)
                #     response.raise_for_status()
                #     print("JSON data successfully sent to the target URL.")
                # except requests.RequestException as e:
                #         print(f"发送JSON数据失败: {e}")
            else:
                print(f'时间：{datetime.datetime.now()}, 客户端{ip_port}已经断开连接')
                break
        except requests.RequestException as e:
                print(f"while: {e}")
    client_socket.close()

def count_ok_ng(detect_new,data):
    global detect 
    detect= detect_new
    try:
        print("线程开始")
        response = requests.get('http://127.0.0.1:5000/reset_cycle_num')
        requests.get('http://127.0.0.1:5000//reset_counters')
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"重置循环计数请求失败: {e}")
        # continue
    
    time1 = datetime.datetime.now().timestamp()

    while detect:
        time.sleep(0.01)
        total_result = determine_ng_ok()
        # time2= datetime.datetime.now()
        if (datetime.datetime.now().timestamp() - time1) > max_delay:
            total_result='NG'
            print('chaoshi')
            break
        if total_result!=[]:
            print('buguifan或ok')
            break
    print("线程结束")    
    end_record(total_result) 
    generated_json = generate_and_update_json(data, total_result)
    print(f'生成的JSON: {generated_json}')
    target_url = 'http://127.0.0.1:46006/api/detect'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(target_url, data=generated_json, headers=headers)
        response.raise_for_status()
        print("JSON data successfully sent to the target URL.")
    except requests.RequestException as e:
            print(f"发送JSON数据失败: {e}")
 
def determine_ng_ok():

    try:
        
        counters = requests.get('http://127.0.0.1:5000/getcounters').json().get('counters', 0)
        # print(counters)
        # print(counters)
    except requests.RequestException as e:
        print(f"获取循环计数请求失败: {e}")
        return 'NG'  # Default to 'NG' on failure
    
    result = check_counters(counters)

    return result

def check_counters(counters):
    # 检查六个数的相互之间是否存在2的差值
    result =[]
    for i in range(len(counters)):
        for j in range(i+1, len(counters)):
            if abs(counters[i] - counters[j]) >= 2:
                
                result = 'NG'
                print('3333',result)
                break
    # 检查所有数是否都大于等于6
    if all(count >= cycle_num_max for count in counters):
        
        result = 'OK'
        print('2222',result)
    # else:
    #     print('1111',result)
    return result

def generate_and_update_json(barcode, total_result):
    image_name = []
    generator = JSONGenerator.JSONGenerator(barcode, total_result, image_name)
   
    # generated_json.update_total_result(total_result)
    try:
        frames_dirs = requests.get('http://127.0.0.1:5000/get_frame_dirs').json().get('frame_dirs', [])
    except requests.RequestException as e:
        print(f"获取帧目录请求失败: {e}")
        frames_dirs = []  # Default to empty list on failure
    
    generator.update_total_result(total_result)
    frames_dirs = generator.convert_image_paths_to_dict(frames_dirs)
    generator.update_images(frames_dirs)
    generated_json = generator.generate_json()
    print(generated_json)
    return generated_json


# Example usage




if __name__ == '__main__':
    config_file_path = 'E:\\AI\\7.3-code\\pythonProject\\conf.ini'
    max_delay, cycle_num_max = read_config_values(config_file_path)
    
    tcp('192.168.67.200', 5001)
    # udp("", 44556)
