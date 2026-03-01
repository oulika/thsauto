import pyautogui
import random
import math
import time


def human_like_mouse_move(target_x, target_y, chaos=2):
    """
    模拟人类的鼠标移动轨迹

    Args:
        target_x: 目标X坐标
        target_y: 目标Y坐标
        chaos: 混乱度参数，越大路径越曲折
    """
    # 获取当前位置
    current_x, current_y = pyautogui.position()

    # 计算距离
    distance = math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2)

    # 根据距离决定步数
    steps = max(20, min(int(distance / 5), 100))

    # 生成曲线路径点
    points = []
    for i in range(steps + 1):
        t = i / steps
        # 使用三次贝塞尔曲线，中间控制点加入随机偏移
        mid_x1 = current_x + (target_x - current_x) * 0.3 + random.uniform(-chaos * 30, chaos * 30)
        mid_y1 = current_y + (target_y - current_y) * 0.3 + random.uniform(-chaos * 30, chaos * 30)
        mid_x2 = current_x + (target_x - current_x) * 0.7 + random.uniform(-chaos * 30, chaos * 30)
        mid_y2 = current_y + (target_y - current_y) * 0.7 + random.uniform(-chaos * 30, chaos * 30)

        # 贝塞尔曲线插值
        x = (1 - t) ** 3 * current_x + 3 * (1 - t) ** 2 * t * mid_x1 + 3 * (1 - t) * t ** 2 * mid_x2 + t ** 3 * target_x
        y = (1 - t) ** 3 * current_y + 3 * (1 - t) ** 2 * t * mid_y1 + 3 * (1 - t) * t ** 2 * mid_y2 + t ** 3 * target_y

        points.append((int(x), int(y)))

    # 移动到每个路径点
    for x, y in points:
        pyautogui.moveTo(x, y, duration=random.uniform(0.01, 0.03))
        # 添加微小的随机停顿
        time.sleep(random.uniform(0.001, 0.005))


# 使用示例
# human_like_mouse_move(800, 600, chaos=2)