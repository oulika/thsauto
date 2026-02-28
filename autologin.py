import time
import pyautogui
from pywinauto import Application
from pywinauto.keyboard import send_keys
import win32gui
import win32con
import win32api


class FixedGFAutoLogin:
    def __init__(self):
        self.app = None
        self.main_window = None
        self.window_rect = None
        self.hwnd = None

    def connect_to_app(self):
        """连接到广发证券程序"""
        try:
            # 使用win32方式连接，更稳定
            self.app = Application(backend="win32").connect(title="广发证券至诚版")
            self.main_window = self.app.window(title="广发证券至诚版")
            self.main_window.wait('visible', timeout=10)

            # 获取窗口句柄
            self.hwnd = self.main_window.handle

            # 获取窗口位置和大小
            self.window_rect = self.main_window.rectangle()
            print(f"窗口位置: 左={self.window_rect.left}, 右={self.window_rect.right}, "
                  f"顶={self.window_rect.top}, 底={self.window_rect.bottom}")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def ensure_window_foreground(self):
        """确保窗口在前台并激活"""
        try:
            # 方法1：使用pywinauto
            self.main_window.set_focus()
            time.sleep(0.5)

            # 方法2：使用win32gui确保窗口激活
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.5)
        except:
            pass

    def click_and_input(self, x, y, text, input_method='multiple'):
        """
        点击并输入文本的多种方法
        """
        print(f"尝试在坐标({x}, {y})输入: {text}")

        # 确保窗口在前台
        self.ensure_window_foreground()

        # 方法1：直接点击然后输入
        try:
            pyautogui.click(x, y)
            time.sleep(0.5)
            pyautogui.write(text, interval=0.1)
            print(f"方法1成功: 已输入")
            return True
        except Exception as e:
            print(f"方法1失败: {e}")

        # 方法2：双击确保选中
        try:
            pyautogui.doubleClick(x, y)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')  # 全选
            time.sleep(0.2)
            pyautogui.press('delete')  # 删除
            time.sleep(0.2)
            pyautogui.write(text, interval=0.1)
            print(f"方法2成功: 已输入")
            return True
        except Exception as e:
            print(f"方法2失败: {e}")

        # 方法3：使用pywinauto的send_keys
        try:
            # 先点击
            pyautogui.click(x, y)
            time.sleep(0.5)
            # 使用send_keys
            send_keys(text)
            print(f"方法3成功: 已输入")
            return True
        except Exception as e:
            print(f"方法3失败: {e}")

        # 方法4：复制粘贴方式
        try:
            # 将文本复制到剪贴板
            import pyperclip
            pyperclip.copy(text)

            # 点击并粘贴
            pyautogui.click(x, y)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            print(f"方法4成功: 已粘贴")
            return True
        except Exception as e:
            print(f"方法4失败: {e}")

        # 方法5：逐个字符模拟键盘（最底层的方法）
        try:
            pyautogui.click(x, y)
            time.sleep(0.5)

            # 确保焦点在输入框
            pyautogui.click(x, y)
            time.sleep(0.3)

            # 逐个字符输入
            for char in text:
                pyautogui.write(char)
                time.sleep(0.1)
            print(f"方法5成功: 已逐个字符输入")
            return True
        except Exception as e:
            print(f"方法5失败: {e}")

        return False

    def calculate_coordinates(self):
        """计算坐标"""
        # 右边1/2区域的X坐标
        left_half = self.window_rect.left + (self.window_rect.width() // 2)

        # 选择右边区域的X坐标（稍微靠左一点，更接近中间）
        x_coord = left_half + (self.window_rect.width() // 4)

        # 垂直分成10份
        window_top = self.window_rect.top
        window_height = self.window_rect.height()
        segment_height = window_height / 10

        # 计算各行的Y坐标
        account_y = window_top + (segment_height * 2.5) + 10
        password_y = window_top + (segment_height * 3.5) + 10
        login_btn_y = window_top + (segment_height * 5.5) + 5

        return {
            'account': (int(x_coord), int(account_y)),
            'password': (int(x_coord), int(password_y)),
            'login_btn': (int(x_coord), int(login_btn_y))
        }

    def auto_login(self, account, password):
        """自动登录主函数"""
        if not self.connect_to_app():
            print("无法连接到程序")
            return False

        try:
            # 计算坐标
            coords = self.calculate_coordinates()
            print(f"计算得到的坐标:")
            print(f"  账号框: {coords['account']}")
            print(f"  密码框: {coords['password']}")
            print(f"  登录按钮: {coords['login_btn']}")

            # 确保窗口在最前面
            self.ensure_window_foreground()
            time.sleep(1)

            # 输入账号
            print("\n开始输入账号...")
            if not self.click_and_input(coords['account'][0], coords['account'][1], account):
                print("账号输入失败")
                return False

            time.sleep(1)

            # 输入密码
            print("\n开始输入密码...")
            if not self.click_and_input(coords['password'][0], coords['password'][1], password):
                print("密码输入失败")
                return False

            time.sleep(1)

            # 点击登录按钮
            print("\n点击登录按钮...")
            pyautogui.click(coords['login_btn'][0], coords['login_btn'][1])
            time.sleep(0.5)

            # 备用：如果点击没反应，尝试按回车
            pyautogui.press('enter')

            print("\n登录操作完成！")
            return True

        except Exception as e:
            print(f"登录过程出错: {e}")
            return False


# 更简单的版本，使用多种输入方式
def simple_fixed_login():
    """简单的修复版登录函数"""
    try:
        # 连接到程序
        app = Application(backend="win32").connect(title="广发证券至诚版")
        main_window = app.window(title="广发证券至诚版")

        # 激活窗口
        main_window.set_focus()
        time.sleep(1)

        # 获取窗口位置
        rect = main_window.rectangle()

        # 计算坐标
        x_coord = rect.left + (rect.width() * 3 // 4)
        window_height = rect.height()

        account_y = rect.top + int(window_height * 0.25)
        password_y = rect.top + int(window_height * 0.35)
        login_btn_y = rect.top + int(window_height * 0.55)

        account = "您的账号"
        password = "您的密码"

        print("开始登录过程...")

        # 输入账号 - 使用多种方法确保成功
        print("输入账号...")

        # 方法1：直接点击
        pyautogui.click(x_coord, account_y)
        time.sleep(0.5)

        # 方法2：确保选中
        pyautogui.doubleClick(x_coord, account_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)

        # 方法3：使用send_keys（有时比write更稳定）
        from pywinauto.keyboard import send_keys
        send_keys(account)
        time.sleep(0.5)

        # 按Tab键切换到密码框
        pyautogui.press('tab')
        time.sleep(0.5)

        # 输入密码
        print("输入密码...")
        send_keys(password)
        time.sleep(0.5)

        # 按回车登录
        print("登录...")
        pyautogui.press('enter')

        print("登录完成！")

    except Exception as e:
        print(f"错误: {e}")


# 终极修复版 - 使用最底层的方法
def ultimate_fix_login():
    """终极修复版，使用最稳定的方法"""
    import ctypes
    from ctypes import wintypes

    # 定义Windows消息常量
    WM_SETTEXT = 0x000C
    WM_GETTEXT = 0x000D
    EM_GETSEL = 0x00B0
    EM_SETSEL = 0x00B1
    WM_CHAR = 0x0102

    try:
        # 找到窗口
        hwnd = win32gui.FindWindow(None, "广发证券至诚版")
        if not hwnd:
            print("未找到窗口")
            return

        # 激活窗口
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)

        # 获取窗口位置
        rect = win32gui.GetWindowRect(hwnd)
        x_coord = rect[0] + ((rect[2] - rect[0]) * 3 // 4)

        # 计算点击位置
        account_y = rect[1] + int((rect[3] - rect[1]) * 0.25)
        password_y = rect[1] + int((rect[3] - rect[1]) * 0.35)

        account = "您的账号"
        password = "您的密码"

        # 点击账号框
        pyautogui.click(x_coord, account_y)
        time.sleep(0.5)

        # 清空并输入账号
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)

        # 逐个字符输入（最稳定）
        for char in account:
            ctypes.windll.user32.SendMessageW(hwnd, WM_CHAR, ord(char), 0)
            time.sleep(0.05)

        time.sleep(0.5)

        # 点击密码框
        pyautogui.click(x_coord, password_y)
        time.sleep(0.5)

        # 清空并输入密码
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)

        for char in password:
            ctypes.windll.user32.SendMessageW(hwnd, WM_CHAR, ord(char), 0)
            time.sleep(0.05)

        time.sleep(0.5)

        # 按回车登录
        pyautogui.press('enter')

        print("登录完成！")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    # 使用修复版
    login = FixedGFAutoLogin()
    login.auto_login("027001037171", "025183")

    # 如果还不行，试试简单版
    # simple_fixed_login()

    # 最后试试终极版
    # ultimate_fix_login()