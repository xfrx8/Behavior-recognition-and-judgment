import cv2


class PixelMatcher:
    def __init__(self, target_pixels, threshold=10):
        """
        初始化 PixelMatcher 类
        :param target_pixels: 目标像素点列表，格式为 [(x1, y1), (x2, y2), ...]
        :param threshold: 框的边长的一半
        """
        self.target_pixels = target_pixels
        self.threshold = threshold

    def match_and_draw(self, frame):
        """
        在给定的帧上绘制匹配的像素区域
        :param frame: 输入帧 (numpy array)
        :return: 带有绘制区域的帧
        """
        output_frame = frame.copy()

        for (x, y) in self.target_pixels:
            # 确保坐标是整数
            x, y = int(x), int(y)

            # 在以目标像素点为中心，阈值为边长一半的区域内绘制矩形框
            top_left = (x - self.threshold, y - self.threshold)
            bottom_right = (x + self.threshold, y + self.threshold)

            # 确保 top_left 和 bottom_right 是整数元组
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

            # 绘制矩形框
            cv2.rectangle(output_frame, top_left, bottom_right, (255, 0, 0), 1)

        return output_frame


# 示例使用
# if __name__ == "__main__":
#     # 定义目标像素点
#     target_pixels = [(50, 50), (100, 100)]
#
#     # 初始化 PixelMatcher 类并设置阈值
#     pixel_matcher = PixelMatcher(target_pixels, threshold=30)
#
#     # 创建一个测试帧 (空白图像)
#     frame = np.zeros((200, 200, 3), dtype=np.uint8)
#
#     # 设置目标像素点的颜色为白色，以便区分
#     for (x, y) in target_pixels:
#         frame[y, x] = [255, 255, 255]
#
#     # 匹配并绘制匹配区域
#     output_frame = pixel_matcher.match_and_draw(frame)
#
#     # 显示结果
#     cv2.imshow("Matched Frame", output_frame)
#     cv2.waitKey(
