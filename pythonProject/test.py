import time

import cv2
import subprocess

'''拉流url地址，指定 从哪拉流'''
video_capture = cv2.VideoCapture(0)  # 调用摄像头的rtsp协议流

'''推流url地址，指定 用opencv把各种处理后的流(视频帧) 推到 哪里'''
push_url = "rtsp://localhost:8554/vedio"

width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))  # Error setting option framerate to value 0.
print("width", width, "height", height, "fps：", fps)

command = ['C:\\Users\\yuyu\\Desktop\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg',  # linux不用指定
           '-y', '-an',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',  # 像素格式
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),  # 自己的摄像头的fps是0，若用自己的notebook摄像头，设置为15、20、25都可。
           '-i', '-',
           '-c:v', 'libx264',  # 视频编码方式
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'rtsp',  # flv rtsp
           '-rtsp_transport', 'tcp',  # 使用TCP推流，linux中一定要有这行
           push_url]  # rtsp rtmp
pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)


def frame_handler(frame):
    ...
    return frame


process_this_frame = True
while True:  # True or video_capture.isOpened():
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # handle the video capture frame
    start = time.time()

    frame = frame_handler(frame)

    # Display the resulting image. linux 需要注释该行代码
    # cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(delay=100) & 0xFF == ord('q'):  # delay=100ms为0.1s .若dealy时间太长，比如1000ms，则无法成功推流！
        break

    pipe.stdin.write(frame.tostring())
    # pipe.stdin.write(frame.tobytes())

video_capture.release()
cv2.destroyAllWindows()
pipe.terminate()