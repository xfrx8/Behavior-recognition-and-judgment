import subprocess
import ffmpeg

# 配置视频流的URL和RTSP服务器的URL
video_stream_url = 'http://192.168.3.159:5000/video_feed'
rtsp_server_url = 'rtsp://localhost:8554/mystream'

# 使用FFmpeg将视频流传输到RTSP服务器
def stream_to_rtsp(video_url, rtsp_url):
    # 使用ffmpeg-python构建FFmpeg命令
    (
        ffmpeg
        .input(video_url)
        .output(rtsp_url, format='rtsp', vcodec='copy')
        .run()
    )

# 调用函数开始流传输
if __name__ == '__main__':
    stream_to_rtsp(video_stream_url, rtsp_server_url)
