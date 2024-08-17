import cv2
import datetime
from ConfigHandler import ConfigHandler
from flask import Flask, render_template, Response, jsonify
from Framesaver import FrameSaver
from FrameProcessor import FrameProcessor
from YOLODetection import YOLODetection
import subprocess
import configparser
from flask import request

# '''拉流url地址，指定 从哪拉流'''
# video_capture = cv2.VideoCapture(0)  # 调用摄像头的rtsp协议流
#
# '''推流url地址，指定 用opencv把各种处理后的流(视频帧) 推到 哪里'''
# push_url = "rtsp://localhost:8554/vedio"
#
# width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(video_capture.get(cv2.CAP_PROP_FPS))  # Error setting option framerate to value 0.
# print("width", width, "height", height, "fps：", fps)
#
# command = ['C:\\Users\\yuyu\\Desktop\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg',  # linux不用指定
#            '-y', '-an',
#            '-f', 'rawvideo',
#            '-vcodec', 'rawvideo',
#            '-pix_fmt', 'bgr24',  # 像素格式
#            '-s', "{}x{}".format(width, height),
#            '-r', str(fps),  # 自己的摄像头的fps是0，若用自己的notebook摄像头，设置为15、20、25都可。
#            '-i', '-',
#            '-c:v', 'libx264',  # 视频编码方式
#            '-pix_fmt', 'yuv420p',
#            '-preset', 'ultrafast',
#            '-f', 'rtsp',  # flv rtsp
#            '-rtsp_transport', 'tcp',  # 使用TCP推流，linux中一定要有这行
#            push_url]  # rtsp rtmp
# pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)
#
#
# def frame_handler(frame):
#     ...
#     return frame
#
#
# process_this_frame = True
# while True:  # True or video_capture.isOpened():
#     # Grab a single frame of video
#     ret, frame = video_capture.read()
#
#     # handle the video capture frame
#     start = time.time()
#
#     frame = frame_handler(frame)
#
#     # Display the resulting image. linux 需要注释该行代码
#     # cv2.imshow('Video', frame)
#
#     # Hit 'q' on the keyboard to quit!
#     if cv2.waitKey(delay=100) & 0xFF == ord('q'):  # delay=100ms为0.1s .若dealy时间太长，比如1000ms，则无法成功推流！
#         break
#
#     pipe.stdin.write(frame.tostring())
#     # pipe.stdin.write(frame.tobytes())
#
# video_capture.release()
# cv2.destroyAllWindows()
# pipe.terminate()

def save_rtsp_stream(url):
    config_handler = ConfigHandler(r'D:\\y\\pythonProject\\pythonProject\\conf.ini')

    yolo_config = config_handler.get_yolo_config()
    video_config = config_handler.get_video_config()
    target_coords = config_handler.get_target_coords()
    push_url = "rtsp://localhost:8554/video"

    width = int(2560)
    height = int(1440)
    fps = int(20)  # Error setting option framerate to value 0.
    print("width", width, "height", height, "fps：", fps)

    # command = ['D:\\y\\pythonProject\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg',  # linux不用指定
    #                 '-y', '-an',
    #                 '-f', 'rawvideo',
    #                 '-vcodec', 'rawvideo',
    #                 '-pix_fmt', 'bgr24',  # 像素格式
    #                 '-s', "{}x{}".format(width, height),
    #                 '-r', str(fps),  # 自己的摄像头的fps是0，若用自己的notebook摄像头，设置为15、20、25都可。
    #                 '-i', '-',
    #                 '-c:v', 'libx264',  # 视频编码方式
    #                 '-pix_fmt', 'yuv420p',
    #                 '-preset', 'ultrafast',
    #                 '-f', 'rtsp',  # flv rtsp
    #                 '-rtsp_transport', 'tcp',  # 使用TCP推流，linux中一定要有这行
    #                 push_url]  # rtsp rtmp
    # pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)
    # start = True
    # cycle_num = 0  # 初始化 cycle_num
    # app = Flask(__name__)
    yolo_detection = YOLODetection(
        yolo_config['model_path'],
        target_coords,
        yolo_config['threshold'],
        yolo_config['detection_window'],
        yolo_config['required_detections'],
        yolo_config['cycle_num_max'],
        yolo_config['conf']
    )
    frame_processor = FrameProcessor(
        video_config['video_source'],
        fps=video_config['fps'],
        img_size=video_config['img_size']
    )
    
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    print(fps)
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    start = datetime.datetime.now()
    print(start)
    print("----------")
    count = 0
    while True:
        ret, frame = cap.read()
        print(datetime.datetime.now())
        if not ret:
            break

        # 处理每一帧数据
        # 在这里可以对每一帧进行一些操作

        # start = datetime.datetime.now()
        count = count + 1
        # out.write(frame)
        time_difference = datetime.datetime.now()-start
        milliseconds_difference = time_difference.total_seconds() * 1000
        annotated_frame, matches, cycle_num = yolo_detection.process_frame(frame)
        # print(milliseconds_difference)
        # cv2.imshow('RTSP Stream', frame)
        cv2.imshow('RTSP Stream', annotated_frame)
        out.write(annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if milliseconds_difference > 1000*10:
            break
    print("----------")
    print(datetime.datetime.now())
    time_difference = datetime.datetime.now() - start
    milliseconds_difference = time_difference.total_seconds() * 1000
    print(milliseconds_difference)
    print(count)
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # RTSP地址，需要替换成实际的海康摄像头RTSP地址
    # rtsp_url = 'rtsp://admin:isen123456@192.168.10.10:554/Streaming/Channels/1'
    # ip_str = '192.168.10.10'
    # rtsp_port = '554'
    #
    # url = "rtsp://admin:isen123456@" + ip_str + ":" + rtsp_port + "/Streaming/Channels/2"
    # print(url)
    # cap = cv2.VideoCapture(url)
    # ret, frame = cap.read()
    # while ret:
    #     ret, frame = cap.read()
    #     cv2.imshow("frame", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # cv2.destroyAllWindows()
    # cap.release()

    # 摄像头IP地址
    ip = '192.168.10.10'
    # 摄像头登录用户名及密码
    user = 'admin'
    password = 'isen123456'
    # url = "rtsp://" + user + ":" + password + "@" + ip + ":554/h264/ch1/main/av_stream"
    # url = "rtsp://" + user + ":" + password + "@" + ip + ":554//Streaming/Channels/1"
    url = "rtsp://admin:isen123456@192.168.10.64:554/h264/ch1/main/av_stream"
    print(url)
    save_rtsp_stream(url)
    # cap = cv2.VideoCapture(url)
    #
    # # 打开RTSP流
    # # 检查是否成功打开流
    # if not cap.isOpened():
    #     print("无法打开RTSP流")
    #     exit()
    #
    # try:
    #     while True:
    #         # 读取帧
    #         ret, frame = cap.read()
    #         # 如果读取成功，显示帧
    #         if ret:
    #             cv2.imshow('RTSP Stream', frame)
    #         else:
    #             print("无法读取帧")
    #             break
    #         # 按'q'退出循环
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    # finally:
    #     # 释放资源
    #     cap.release()
    #     cv2.destroyAllWindows()
