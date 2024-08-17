import cv2
import datetime
from ConfigHandler import ConfigHandler
from flask import Flask, render_template, Response, jsonify
from Framesaver import FrameSaver
from FrameProcessor import FrameProcessor
from YOLODetection import YOLODetection
import time
import subprocess
import configparser
from flask import request

def save_rtsp_stream():
    print("start1")
    # config_handler = ConfigHandler(r'C:\\Users\\PC\\Documents\\7.3-code\\pythonProject\\conf.ini')

    # yolo_config = config_handler.get_yolo_config()
    # video_config = config_handler.get_video_config()
    # target_coords = config_handler.get_target_coords()

    # yolo_detection = YOLODetection(
    #     yolo_config['model_path'],
    #     target_coords,
    #     yolo_config['threshold'],
    #     yolo_config['detection_window'],
    #     yolo_config['required_detections'],
    #     yolo_config['cycle_num_max'],
    #     yolo_config['conf']
    # )
    
    cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")
    print("----------")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(fps)
    out = cv2.VideoWriter('E:\\saveMp4\\output_save.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    start = datetime.datetime.now()
    print(start)
    print("----------")
    count = 0
    while True:
        ret, frame = cap.read()
        #print(datetime.datetime.now())
        if not ret:
            break
        #start_time = time.perf_counter_ns()
        count = count + 1
        #time_difference_ns = time.perf_counter_ns()-start_time
        # annotated_frame, matches, cycle_num = yolo_detection.process_frame(frame)
        #cv2.imshow('RTSP Stream', frame)
        out.write(frame)
        #print(time_difference_ns/1000000)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break
        time_difference = datetime.datetime.now() - start
        milliseconds_difference = time_difference.total_seconds() * 1000
        if milliseconds_difference > 1000*10:
            break
    print("----------")
    time_difference = datetime.datetime.now() - start
    milliseconds_difference = time_difference.total_seconds()
    print(f"时长:{milliseconds_difference}")
    print(f"总帧数:{count}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("start")
    save_rtsp_stream()

