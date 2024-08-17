import cv2
import time
import os


class FrameSaver:
    def __init__(self, save_path="E:\\saved_frames", max_save_count=10):
        self.save_path = save_path
        self.filename = None
        self.max_save_count = max_save_count
        self.previous_matches = None
        self.save_count = 0
        self.frame_dirs = []

        # 创建保存路径
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def check_and_save(self, annotated_frame, matches):
        # 检查matches是否发生变化
        if self.previous_matches is None or matches != self.previous_matches:
            self.save_frame_as_jpg(annotated_frame)
            self.save_count += 1
            
        self.previous_matches = matches

    def save_frame_as_jpg(self, annotated_frame):
        if self.save_count >= self.max_save_count:
            # print("Maximum save count reached.")
            return
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filename = os.path.join(self.save_path, f"frame_{timestamp}.jpg")
        cv2.imwrite(self.filename, annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        self.frame_dirs.append(self.filename)
        # print(f"Saved frame at {self.filename}")

    def get_frame_dirs(self):
        self.frame_dirs1 = self.frame_dirs
        self.frame_dirs = []
        self.save_count = 0 
        return self.frame_dirs1

    def reset(self):
        self.filename = None
        self.previous_matches = None
        self.save_count = 0
        self.frame_dirs = []
        # You can also add logic to clean up the save_path directory if needed
        # e.g., removing saved frames or resetting directory contents

# Example usage
if __name__ == "__main__":
    saver = FrameSaver()
    # Simulate saving frames
    frame = cv2.imread('test.jpg')  # Replace with actual frame
    saver.check_and_save(frame, matches=1)
    saver.check_and_save(frame, matches=2)
    print(saver.get_frame_dirs())
    
    # Reset the FrameSaver
    saver.reset()
    print(saver.get_frame_dirs())  # Should be an empty list after reset
