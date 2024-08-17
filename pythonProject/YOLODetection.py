from ultralytics import YOLO
import cv2
from YoloCoordinateMatcher import YoloCoordinateMatcher
from BooleanListChecker import BooleanListChecker
from BooleanListChecker import BooleanMirror
from PixelMatcher import PixelMatcher


class YOLODetection:
    def __init__(self, model_path, target_coords, threshold=0.7, detection_window=0.5, required_detections=2, cycle_num_max=6, conf=0.7):
        self.model = YOLO(model_path)
        self.target_coords = target_coords
        self.conf = conf
        self.threshold = threshold
        self.required_detections = required_detections
        self.detection_window = detection_window
        self.cycle_num_max = cycle_num_max
        self.matcher = YoloCoordinateMatcher(threshold=60, detection_window=self.detection_window, required_detections=self.required_detections)  # 初始化坐标匹配器
        self.bm = BooleanMirror([False] * len(self.target_coords), [False] * len(self.target_coords))
        self.cycle_num = 0
        self.false_position = 23
        self.pixel_matcher = PixelMatcher(self.target_coords, threshold=self.threshold)

    def process_frame(self, frame):
        results = self.model.predict(frame, conf=self.conf, verbose=False)
        annotated_frame = results[0].plot()

        if results[0].boxes.xywh.numel() == 0:
            for coord in self.target_coords:
                frame = cv2.circle(frame, (int(coord[0]), int(coord[1])), 5, (0, 255, 255), -1)
                frame = self.pixel_matcher.match_and_draw(frame)
            return frame, [False] * len(self.target_coords), self.cycle_num

        if BooleanListChecker(self.bm.mirror_list).check_all_true():
            self.cycle_num += 1
            self.bm.mirror_list = [False] * len(self.target_coords)

        matches = []
        leftmost_detection = None

        for r in results:
            for detection in r.boxes.xyxy:
                x2 = int(detection[2].item())

                # y2 = int(detection[3].item())

                # 选择最左边的检测结果
                if leftmost_detection is None or x2 < leftmost_detection[2]:
                    leftmost_detection = detection

        if leftmost_detection is not None:
            x2 = int(((leftmost_detection[2].item()+leftmost_detection[0].item())/2)+90)
            y2 = int(leftmost_detection[3].item())
            cv2.circle(annotated_frame, (x2, y2), radius=5, color=(0, 255, 0), thickness=-1)
            matches = self.matcher.match_coordinates((x2, y2), self.target_coords)

            # for i, match in enumerate(matches):
                # if match:
                    # print(f"目标坐标 {self.target_coords[i]} 匹配成功")

        self.bm.source_list = matches
        if True in matches:
            x = matches.index(True)
            if sum(self.bm.mirror_list) == 0 and x != self.false_position:
                self.bm.update()
            elif sum(self.bm.mirror_list) != 0:
                self.bm.update()

        for i, coord in enumerate(self.target_coords):
            color = (0, 255, 0) if self.bm.mirror_list[i] else (0, 0, 255)
            cv2.circle(annotated_frame, (int(coord[0]), int(coord[1])), 5, color, -1)
        cv2.putText(annotated_frame, f"Cycle Num: {self.cycle_num}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, cv2.LINE_AA)
        annotated_frame = self.pixel_matcher.match_and_draw(annotated_frame)
        if self.bm.mirror_list.count(False) == 1:
            self.false_position = self.bm.mirror_list.index(False)

        return annotated_frame, matches, self.cycle_num

    def reset_cycle_num(self):
        self.cycle_num = 0
        print("Cycle number has been reset to zero.")
    def reset_mirror_list(self):
        self.bm.mirror_list = [False] * len(self.target_coords)
        print("bm.mirror_list has been reset to all False.")
