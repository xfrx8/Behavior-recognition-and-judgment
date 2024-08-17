import cv2
from flask import Flask, render_template, Response, jsonify, request
import configparser
from Framesaver import FrameSaver
from FrameProcessor import FrameProcessor
from YOLODetection import YOLODetection
from BooleanVectorCounter import BooleanVectorCounter


class VideoStreamer:
    def __init__(self, config_handler):
        yolo_config = config_handler.get_yolo_config()
        video_config = config_handler.get_video_config()
        target_coords = config_handler.get_target_coords()
        self.start = True
        self.cycle_num = 0  # 初始化 cycle_num
        self.app = Flask(__name__)
        self.yolo_detection = YOLODetection(
            yolo_config['model_path'],
            target_coords,
            yolo_config['threshold'],
            yolo_config['detection_window'],
            yolo_config['required_detections'],
            yolo_config['cycle_num_max'],
            yolo_config['conf']
        )
        self.frame_processor = FrameProcessor(
            video_config['video_source'],
            fps=video_config['fps'],
            img_size=video_config['img_size']
        )
        self.frame_saver = FrameSaver(save_path='E:\\saved_frames', max_save_count=10)
        self.cycle_num_max = yolo_config['cycle_num_max']
        self.boolean_counter = BooleanVectorCounter(6)  # 初始化 BooleanVectorCounter

        @self.app.route('/set_cycle_num_max')
        def set_cycle_num():
            try:
                num = request.args.get('num')
                print('循环圈数:' + num)
                conf = configparser.ConfigParser()
                conf.read('E:\\AI\\7.3-code\\pythonProject\\conf.ini', encoding='utf-8')
                conf.set('YOLO', 'cycle_num_max', num)
                conf.write(open('E:\\AI\\7.3-code\\pythonProject\\conf.ini', 'w'))
                cn = conf.get('YOLO', 'cycle_num_max')
                
                return {"result": "success", "cycle_num_max": cn}

            except Exception as e:
                print(e)
                return {"result": "failed"}

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/get_cycle_num')
        def get_cycle_num():
            return jsonify({"cycle_num": self.cycle_num})

        @self.app.route('/reset_counts')
        def reset_counts():
            self.boolean_counter.reset()
            return jsonify({"status": "counts reset to zero"})
        @self.app.route('/getcounters')
        def get_counters():
            return jsonify({"counters": self.boolean_counter.get_counts()})

        @self.app.route('/reset_cycle_num')
        def reset_cycle_num():
            # self.cycle_num = 0
            self.yolo_detection.reset_cycle_num()
            self.frame_saver.reset()
            self.boolean_counter.reset_counts()
            self.yolo_detection.reset_mirror_list()
            return jsonify({"status": "cycle_num reset to zero"})

        @self.app.route('/get_cycle_num_max')
        def get_cycle_num_max():
            # 读取配置文件
            config = configparser.ConfigParser()
            config.read('E:\\AI\\7.3-code\\pythonProject\\conf.ini')
            self.cycle_num_max = config['YOLO'].getint('cycle_num_max')
            return jsonify({"cycle_num_max": self.cycle_num_max})

        # 获取截取帧的文件目录s
        @self.app.route('/get_frame_dirs')
        def get_frame_dir():
            return jsonify({"frame_dirs": self.frame_saver.get_frame_dirs()})

    def generate_frames(self):
        while True:
            frame = self.frame_processor.get_frame()
            if frame is None:
                break
            annotated_frame, matches, cycle_num = self.yolo_detection.process_frame(frame)

            self.frame_saver.check_and_save(annotated_frame, matches)
            self.cycle_num = cycle_num  # 更新 cycle_num
            self.boolean_counter.update_vector(matches)
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)


