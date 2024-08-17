import configparser


class ConfigHandler:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config.read_file(f)

    def get_yolo_config(self):
        yolo_config = {
            'model_path': self.config['YOLO']['model_path'],
            'threshold': self.config.getfloat('YOLO', 'threshold'),
            'detection_window': self.config.getfloat('YOLO', 'detection_window'),
            'required_detections': self.config.getint('YOLO', 'required_detections'),
            'conf': self.config.getfloat('YOLO', 'conf'),
            'cycle_num_max': self.config.getint('YOLO', 'cycle_num_max')
        }
        return yolo_config

    def get_video_config(self):
        video_config = {
            'video_source': self.config.getint('VIDEO', 'video_source'),
            'fps': self.config.getint('VIDEO', 'fps'),
            'img_size': (self.config.getint('VIDEO', 'img_width'), self.config.getint('VIDEO', 'img_height'))
        }
        return video_config

    def get_target_coords(self):
        target_coords_str = self.config['TARGET_COORDS']['coords']
        target_coords = [tuple(map(int, coord.split(','))) for coord in target_coords_str.split(';')]
        return target_coords
