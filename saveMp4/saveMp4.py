import cv2
from flask import Flask
import time
import os
import datetime
import threading
import concurrent.futures

app = Flask(__name__)

isRead = False
detectionResult = ""

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


@app.route('/start_record/<bar_code>')
def start_record(bar_code):
    # threading.Thread(target=record_thread, args=(bar_code))
    # thread_pool = threading.BoundedSemaphore(1)
    global isRead
    if isRead:
        return "正在录制视频，请稍后"
    else:
        executor.submit(record_thread, bar_code)
    return "True"


def record_thread(bar_code):
    # 创建保存路径
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    data_str = time.strftime("%Y%m%d")
    save_path = "E:\\saveMp4\\" + data_str
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = os.path.join(save_path, f"{bar_code}_{timestamp}.mp4")

    cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")
    #cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))
    print("fps:：", 20, "width:", width, "height:", height)

    global isRead
    global detectionResult
    isRead = True
    detectionResult = ""
    start = datetime.datetime.now()
    print(f"开始录制,条码：{bar_code},时间：{start}")
    print(f"录制标识:{isRead}")
    count = 0
    while isRead:
        ret, frame = cap.read()
        if not ret:
            break
        count = count+1
        out.write(frame)
    cap.release()
    out.release()
    end = datetime.datetime.now()
    time_difference = datetime.datetime.now() - start
    milliseconds_difference = time_difference.total_seconds()
    print(f"总帧数:{count}")
    print(f"时长:{milliseconds_difference}")
    filename_new = os.path.join(save_path, f"{bar_code}_{timestamp}_{detectionResult}.mp4")
    os.rename(filename, filename_new)
    print(f"检测结果:{detectionResult}，时间：{end}")
    print(f"视频路径:{filename_new}")
    detectionResult = ""


@app.route('/end_record/<detection_result>')
def end_record(detection_result):
    global isRead
    global detectionResult
    print(f"结束录制 前, 录制标识:{isRead}")
    print(f"结束录制 前, 检测结果:{detection_result}")
    isRead = False
    detectionResult = detection_result
    print(f"结束录制 后, 录制标识:{isRead}")
    print(f"结束录制 后, 检测结果:{detection_result}")
    return "True"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
