import time


class YoloCoordinateMatcher:
    def __init__(self, threshold=10, detection_window=0.5, required_detections=2):
        self.threshold = threshold
        self.detection_window = detection_window
        self.required_detections = required_detections
        self.match_timestamps = {}
        self.matched_timestamps = {}

    def match_coordinates(self, yolo_coord, target_coords):
        current_time = time.time()
        results = []
        for coord in target_coords:
            if self._is_match(yolo_coord, coord):
                if coord not in self.match_timestamps:
                    self.match_timestamps[coord] = []
                self.match_timestamps[coord].append(current_time)
                # 保留在检测窗口内的时间戳
                self.match_timestamps[coord] = [t for t in self.match_timestamps[coord] if current_time - t <= self.detection_window]
                if len(self.match_timestamps[coord]) >= self.required_detections:
                    results.append(True)
                    self.matched_timestamps[coord] = current_time  # 记录匹配成功的坐标和时间戳
                else:
                    results.append(False)
            else:
                if coord in self.match_timestamps:
                    self.match_timestamps[coord] = [t for t in self.match_timestamps[coord] if current_time - t <= self.detection_window]
                results.append(False)
        return results

    def _is_match(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) <= self.threshold and abs(coord1[1] - coord2[1]) <= self.threshold

    def get_matched_timestamps(self):
        return self.matched_timestamps
