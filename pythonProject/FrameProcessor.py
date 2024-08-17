import cv2


class FrameProcessor:
    def __init__(self, video_path, fps, img_size):
        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,200)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[1])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[0])

    def get_frame(self, num=0):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, num)
        success, frame = self.cap.read()

        if not success:
            return None
        return frame

    def release(self):
        self.cap.release()
