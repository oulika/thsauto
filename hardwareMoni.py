import ctypes
from ctypes import wintypes
import time
import random


class HardwareKeyboardSimulator:
    """
    使用硬件级API模拟键盘输入
    """

    # Windows API constants
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYDOWN = 0x0000
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_SCANCODE = 0x0008

    def __init__(self):
        self.user32 = ctypes.windll.user32

        # 定义INPUT结构体
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
            ]

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
            ]

        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = [
                ("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD)
            ]

        class INPUT_UNION(ctypes.Union):
            _fields_ = [
                ("ki", KEYBDINPUT),
                ("mi", MOUSEINPUT),
                ("hi", HARDWAREINPUT)
            ]

        class INPUT(ctypes.Structure):
            _anonymous_ = ("ui",)
            _fields_ = [
                ("type", wintypes.DWORD),
                ("ui", INPUT_UNION)
            ]

        self.INPUT = INPUT
        self.KEYBDINPUT = KEYBDINPUT

    def send_key(self, key_code, scan_code=0):
        """
        发送硬件级键盘事件
        """
        # 使用扫描码而不是虚拟键码，更难被检测
        if scan_code == 0:
            scan_code = self.user32.MapVirtualKeyA(key_code, 0)

        # 按键按下
        key_down = self.INPUT(
            type=self.INPUT_KEYBOARD,
            ki=self.KEYBDINPUT(
                wVk=key_code,
                wScan=scan_code,
                dwFlags=self.KEYEVENTF_SCANCODE,  # 使用扫描码
                time=0,
                dwExtraInfo=None
            )
        )

        # 按键释放
        key_up = self.INPUT(
            type=self.INPUT_KEYBOARD,
            ki=self.KEYBDINPUT(
                wVk=key_code,
                wScan=scan_code,
                dwFlags=self.KEYEVENTF_SCANCODE | self.KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=None
            )
        )

        # 发送按下事件
        self.user32.SendInput(1, ctypes.byref(key_down), ctypes.sizeof(self.INPUT))

        # 随机按键时长
        time.sleep(random.uniform(0.05, 0.15))

        # 发送释放事件
        self.user32.SendInput(1, ctypes.byref(key_up), ctypes.sizeof(self.INPUT))

        # 随机按键间隔
        time.sleep(random.uniform(0.08, 0.25))

    def type_string(self, text):
        """
        模拟打字字符串
        """
        # 虚拟键码映射（简化版）
        vk_map = {
            'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
            'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
            'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
            'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
            'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
            '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
            '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        }

        for char in text:
            if char.isupper():
                # 按下Shift
                self.send_key(0x10)  # VK_SHIFT
                time.sleep(random.uniform(0.02, 0.08))

                # 输入大写字母
                self.send_key(vk_map[char.lower()])

                # 释放Shift
                time.sleep(random.uniform(0.02, 0.08))
                self.send_key(0x10)  # 再次发送Shift会释放
            else:
                # 输入小写字母或数字
                if char in vk_map:
                    self.send_key(vk_map[char])
                else:
                    # 处理特殊字符
                    self._send_special_char(char)

            # 随机长停顿（模拟思考）
            if random.random() < 0.15:
                time.sleep(random.uniform(0.5, 1.8))

    def _send_special_char(self, char):
        """处理特殊字符"""
        special_map = {
            '.': 0xBE,  # VK_OEM_PERIOD
            '@': 0x32,  # 需要Shift+2
        }
        # 简化处理...


# 使用示例
hw_sim = HardwareKeyboardSimulator()

# 先聚焦到输入框
# pyautogui.click(center_x, account_y)
time.sleep(random.uniform(0.3, 0.8))

# 使用硬件级模拟输入123456
# hw_sim.type_string('123456')