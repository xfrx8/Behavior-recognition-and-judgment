import socket
import threading
import datetime
import time
import requests
import JSONGenerator
import json
import configparser
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(
    filename='E:\\AI\\7.3-code\\pythonProject\\app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 开始录制接口
def start_record(barcode):
    url = "http://localhost:8001/start_record/" + barcode
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("开始录制成功")
    else:
        logging.error("开始录制失败 %s %s", response.status_code, response.text)

# 结束录制接口
def end_record(result):
    url = "http://localhost:8001/end_record/" + result
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("结束录制成功")
    else:
        logging.error("结束录制失败 %s %s", response.status_code, response.text)

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
    logging.info(f"udp接收已启动，地址{host}，端口{port}")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 44556))
    while True:
        recv_data, client_address = udp_socket.recvfrom(1024)
        logging.info(f"地址：{client_address}，数据：{recv_data.decode()}")

def tcp(host, port):
    logging.info(f"tcp服务端已启动，地址{host}，端口{port}")
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
    logging.info(f'客户端:{ip_port}加入连接')

    while True:
        try:
            data = client_socket.recv(1024).decode('gbk')
            start_record(data)
            if len(data) != 0:
                global detect 
                detect = False
                logging.info(f'客户端:{ip_port}, 数据:{data}') 

                executor.submit(count_ok_ng, True, data)
            else:
                logging.info(f'客户端{ip_port}已经断开连接')
                break
        except requests.RequestException as e:
            logging.error(f"while: {e}")
    client_socket.close()

def count_ok_ng(detect_new, data):
    global detect 
    detect = detect_new
    try:
        logging.info("线程开始")
        response = requests.get('http://127.0.0.1:5000/reset_cycle_num')
        requests.get('http://127.0.0.1:5000//reset_counters')
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"重置循环计数请求失败: {e}")
    
    time1 = datetime.datetime.now().timestamp()
    
    while detect:
        time.sleep(0.01)
        total_result = determine_ng_ok()
        if (datetime.datetime.now().timestamp() - time1) > max_delay:
            total_result = 'NG'
            logging.warning('超时')
            break
        if total_result != []:
            logging.info('不规范或OK')
            break
    if total_result == []:
        total_result='NG'
    logging.info("线程结束")    
    end_record(total_result) 
    generated_json = generate_and_update_json(data, total_result)
    logging.info(f'生成的JSON: {generated_json}')
    target_url = 'http://127.0.0.1:46006/api/detect'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(target_url, data=generated_json, headers=headers)
        response.raise_for_status()
        logging.info("JSON data successfully sent to the target URL.")
    except requests.RequestException as e:
        logging.error(f"发送JSON数据失败: {e}")
    
def determine_ng_ok():
    try:
        counters = requests.get('http://127.0.0.1:5000/getcounters').json().get('counters', 0)
    except requests.RequestException as e:
        logging.error(f"获取循环计数请求失败: {e}")
        return 'NG'  # Default to 'NG' on failure
    
    result = check_counters(counters)
    return result

def check_counters(counters):
    result = []
    for i in range(len(counters)):
        for j in range(i+1, len(counters)):
            if abs(counters[i] - counters[j]) >= 2:
                result = 'NG'
                logging.info('检测结果: NG')
                break
    if all(count >= cycle_num_max for count in counters):
        result = 'OK'
        logging.info('检测结果: OK')
    return result

def generate_and_update_json(barcode, total_result):
    image_name = []
    generator = JSONGenerator.JSONGenerator(barcode, total_result, image_name)
    try:
        frames_dirs = requests.get('http://127.0.0.1:5000/get_frame_dirs').json().get('frame_dirs', [])
    except requests.RequestException as e:
        logging.error(f"获取帧目录请求失败: {e}")
        frames_dirs = []  # Default to empty list on failure
    
    generator.update_total_result(total_result)
    frames_dirs = generator.convert_image_paths_to_dict(frames_dirs)
    generator.update_images(frames_dirs)
    generated_json = generator.generate_json()
    logging.info(generated_json)
    return generated_json

if __name__ == '__main__':
    config_file_path = 'E:\\AI\\7.3-code\\pythonProject\\conf.ini'
    max_delay, cycle_num_max = read_config_values(config_file_path)
    tcp('192.168.67.200', 5001)
