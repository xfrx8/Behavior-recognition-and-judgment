# 这是一个示例 Python 脚本。

from VideoStreamer import VideoStreamer as Vs
from ConfigHandler import ConfigHandler

# target_coords = [(975, 805), (1176, 896), (1400, 806), (1391, 651), (1010, 654), (1186, 584)]
# model_path =  "best.pt"
# threshold=60
# required_frames = 7
# conf = 0.7
# cycle_num_max = 6
# video_source = "videos/视频5.mp4"

config_handler = ConfigHandler(r'E:\\AI\\7.3-code\\pythonProject\\conf.ini')
streamer = Vs(config_handler)
streamer.run()
