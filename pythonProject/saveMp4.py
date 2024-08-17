import cv2
import datetime
import numpy as np
import requests
from io import BytesIO
from PIL import Image


def save_rtsp_stream():
    # 视频流的URL
    global bytes
    stream_url = "http://127.0.0.1:5000/video_feed"

    # response = requests.get(stream_url, stream=True)
    # start = datetime.datetime.now()
    # print(start)
 
    # # 打开文件以二进制写入模式
    # with open('output_video.mp4', 'wb') as output_file:
    #     for chunk in response.iter_content(chunk_size=1024):
    #         if chunk:
    #             output_file.write(chunk)
    #             time_difference = datetime.datetime.now() - start
    #             milliseconds_difference = time_difference.total_seconds() * 1000
    #             if milliseconds_difference > 1000*10:
    #                 break
    
    # print("视频保存完成。")

    # response = requests.get(stream_url, stream=True)
    # start = datetime.datetime.now()
    # print(start)
    # out = cv2.VideoWriter('output_new.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20,(int(2560),int(1440)))
    # imageBytes = bytes()
    # count = 0
    # for data in response.iter_content():
    #     count = count + 1
    #     # 输出data 查看每一张图片的开始与结尾，查找图片的头与尾截取jpg。并把剩余部分imageBytes做保存
    #     imageBytes += data
    #     a = imageBytes.find(b'\xff\xd8')
    #     b = imageBytes.find(b'\xff\xd9')
    #     if a != -1 and b != -1:
    #         print(datetime.datetime.now())
    #         jpg = imageBytes[a:b + 2]
    #         imageBytes = imageBytes[b + 2:]

    #         bytes_stream = BytesIO(jpg)
    #         img = Image.open(bytes_stream)
    #         img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    #         cv2.imshow('img', img)
    #         out.write(img)
    #         if cv2.waitKey(10) & 0XFF == ord('q'):
    #             break

    # cv2.destroyAllWindows()
    # print("jieshu")


    response = requests.get(stream_url, stream=True)
    # 确保请求成功
    if response.status_code == 200:
        for frame in response.iter_content():
            if frame:
                # 使用PIL读取单帧图像
                print(datetime.datetime.now())
                img = Image.open(BytesIO(frame))
                # 转换成OpenCV格式
                #img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
                # 在这里处理img_cv
                # ...
    
                # 显示图像
                #cv2.imshow('Video Stream', img_cv)
    
                # time_difference = datetime.datetime.now() - start
                # milliseconds_difference = time_difference.total_seconds() * 1000
                # if milliseconds_difference > 1000 * 10:
                #     break
                # 按 'q' 退出循环
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    save_rtsp_stream()
    # save_rtsp_stream()
