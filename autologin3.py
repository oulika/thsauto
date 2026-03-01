import pyautogui
import time
import subprocess
import psutil
import os
from pywinauto import Application

from autologin2 import auto_login_calculated_coordinates

# 配置参数
EXE_PATH = r"C:\广发证券至诚版\xiadan.exe"
PASSWORD = "你的密码"  # 请替换为实际密码


def kill_process(process_name):
    """杀掉指定名称的进程"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                proc.kill()
                print(f"已杀死进程: {process_name}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    print(f"未找到进程: {process_name}")
    return False


def open_application():
    """打开应用程序"""
    try:
        subprocess.Popen(EXE_PATH)
        print("已启动应用程序")
        return True
    except Exception as e:
        print(f"启动应用程序失败: {e}")
        return False


def move_to_center_and_login():
    """移动鼠标到屏幕中心并输入密码登录"""
    # 等待应用程序完全启动
    time.sleep(5)

    # 获取屏幕尺寸并计算中心点
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    print(f"屏幕尺寸: {screen_width}x{screen_height}")
    print(f"屏幕中心点: ({center_x}, {center_y})")

    # 移动鼠标到屏幕中心并点击
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    pyautogui.click()

    # 等待焦点切换
    time.sleep(1)

    # 输入密码
    print("正在输入密码...")
    pyautogui.write(PASSWORD)

    # 按回车键登录
    print("按回车键登录...")
    pyautogui.press('enter')

    print("登录操作完成")


def main():
    print("开始执行操作...")

    # 1. 杀死现有进程
    print("步骤1: 杀掉xiadan.exe进程")
    kill_process("xiadan.exe")
    time.sleep(2)

    # 2. 重新打开应用
    print("步骤2: 重新打开应用程序")
    open_application()
    time.sleep(5)


    # 3. 移动到屏幕中心并登录
    print("步骤3: 准备登录操作")
    # move_to_center_and_login()

    auto_login_calculated_coordinates('027001037171','025183')

    print("所有操作完成！")


if __name__ == "__main__":
    main()