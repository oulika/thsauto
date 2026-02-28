import pywinauto
from pywinauto import Application, Desktop
import time


def auto_login_calculated_coordinates(username, password):
    """
    基于垂直7等分和水平居中的坐标计算自动登录
    """

    print("正在查找登录窗口...")

    # 方法1：尝试连接到现有窗口
    try:
        app = Application().connect(title="用户登录", class_name="#32770")
        dlg = app.window(title="用户登录")
        print("成功连接到登录窗口")
    except:
        # 方法2：等待窗口出现
        print("等待窗口出现...")
        time.sleep(2)
        windows = Desktop(backend="uia").windows()
        login_window = None

        for win in windows:
            if win.window_text() == "用户登录" or "登录" in win.window_text():
                login_window = win
                break

        if not login_window:
            print("未找到登录窗口")
            return False

        app = Application().connect(handle=login_window.handle)
        dlg = app.window(handle=login_window.handle)

    # 激活窗口
    dlg.set_focus()
    time.sleep(1)

    # 获取窗口位置和大小
    rect = dlg.rectangle()
    window_left = rect.left
    window_top = rect.top
    window_width = rect.width()
    window_height = rect.height()

    print(f"窗口位置: left={window_left}, top={window_top}")
    print(f"窗口大小: width={window_width}, height={window_height}")

    # 计算垂直7等分的高度
    segment_height = window_height / 7

    # 计算水平居中X坐标
    center_x = window_left + window_width // 2

    # 根据7等分计算各元素的Y坐标
    # 第4行（账号）: 3.5份的偏移（取中间值）
    account_y = window_top + int(segment_height * 3.5)

    # 第5行（密码）: 4.5份的偏移
    password_y = window_top + int(segment_height * 4.5)

    # 第7行（登录）: 6.5份的偏移
    login_y = window_top + int(segment_height * 6.5)

    print(f"垂直7等分高度: {segment_height:.1f}px")
    print(f"账号位置: ({center_x}, {account_y})")
    print(f"密码位置: ({center_x}, {password_y})")
    print(f"登录位置: ({center_x}, {login_y})")

    try:
        # 导入pyautogui用于鼠标操作
        import pyautogui

        # 1. 点击账号输入框
        print("输入账号...")
        pyautogui.click(center_x, account_y)
        time.sleep(0.5)

        # 清空可能存在的旧内容
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(0.3)

        # 输入账号
        pyautogui.write(username)
        time.sleep(0.5)

        # 2. 点击密码输入框
        print("输入密码...")
        pyautogui.click(center_x, password_y)
        time.sleep(0.5)

        # 清空可能存在的旧内容
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(0.3)

        # 输入密码
        pyautogui.write(password)
        time.sleep(0.5)

        # 3. 点击登录按钮
        print("点击登录...")
        pyautogui.click(center_x, login_y)

        # 或者尝试按回车键
        # pyautogui.press('enter')

        print("登录操作完成")
        return True

    except Exception as e:
        print(f"操作失败: {e}")
        return False


# 增强版：包含偏移量调整功能
def auto_login_adjustable(username, password, x_offset=0, y_offset_account=0, y_offset_password=0, y_offset_login=0):
    """
    可调整偏移量的版本
    :param x_offset: 水平偏移量（正数向右，负数向左）
    :param y_offset_account: 账号垂直偏移量
    :param y_offset_password: 密码垂直偏移量
    :param y_offset_login: 登录按钮垂直偏移量
    """

    try:
        app = Application().connect(title="用户登录", class_name="#32770")
        dlg = app.window(title="用户登录")
        dlg.set_focus()
        time.sleep(1)

        rect = dlg.rectangle()
        window_width = rect.width()
        window_height = rect.height()

        # 计算基础坐标
        base_center_x = rect.left + window_width // 2
        segment_height = window_height / 7

        # 应用偏移量
        center_x = base_center_x + x_offset
        account_y = rect.top + int(segment_height * 3.5) + y_offset_account
        password_y = rect.top + int(segment_height * 4.5) + y_offset_password
        login_y = rect.top + int(segment_height * 6.5) + y_offset_login

        import pyautogui

        print("开始自动登录...")

        # 账号输入
        pyautogui.click(center_x, account_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.write(username)
        time.sleep(0.5)

        # 密码输入
        pyautogui.click(center_x, password_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.write(password)
        time.sleep(0.5)

        # 点击登录
        pyautogui.click(center_x, login_y)

        print("登录完成")
        return True

    except Exception as e:
        print(f"错误: {e}")
        return False


# 调试版本：显示点击位置并等待确认
def auto_login_debug_mode(username, password):
    """
    调试模式：显示将要点击的位置，等待用户确认
    """

    app = Application().connect(title="用户登录", class_name="#32770")
    dlg = app.window(title="用户登录")
    dlg.set_focus()
    time.sleep(1)

    rect = dlg.rectangle()
    window_width = rect.width()
    window_height = rect.height()

    center_x = rect.left + window_width // 2
    segment_height = window_height / 7

    account_y = rect.top + int(segment_height * 3.5)
    password_y = rect.top + int(segment_height * 4.5)
    login_y = rect.top + int(segment_height * 6.5)

    print("=== 调试信息 ===")
    print(f"窗口区域: L={rect.left}, T={rect.top}, W={window_width}, H={window_height}")
    print(f"水平中心: {center_x}")
    print(f"垂直分段高度: {segment_height:.2f}")
    print(f"账号位置: ({center_x}, {account_y})")
    print(f"密码位置: ({center_x}, {password_y})")
    print(f"登录位置: ({center_x}, {login_y})")
    print("=" * 40)

    # 显示鼠标移动轨迹但不点击
    import pyautogui
    pyautogui.moveTo(center_x, account_y, duration=1)
    print("鼠标移动到账号位置")
    input("按Enter继续...")

    pyautogui.moveTo(center_x, password_y, duration=1)
    print("鼠标移动到密码位置")
    input("按Enter继续...")

    pyautogui.moveTo(center_x, login_y, duration=1)
    print("鼠标移动到登录位置")
    input("按Enter确认执行自动登录...")

    # 执行实际登录
    pyautogui.click(center_x, account_y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pyautogui.write(username)
    time.sleep(0.5)

    pyautogui.click(center_x, password_y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pyautogui.write(password)
    time.sleep(0.5)

    pyautogui.click(center_x, login_y)
    print("登录执行完成")


# 使用示例
if __name__ == "__main__":
    # 设置你的账号密码
    USERNAME = "your_username"
    PASSWORD = "your_password"

    # 首次运行建议使用调试模式
    print("首次运行请使用调试模式确认坐标")
    choice = input("选择模式: 1-标准模式, 2-调试模式, 3-可调模式: ")

    if choice == "1":
        success = auto_login_calculated_coordinates(USERNAME, PASSWORD)
        print("成功" if success else "失败")

    elif choice == "2":
        auto_login_debug_mode(USERNAME, PASSWORD)

    elif choice == "3":
        # 如果坐标不准，可以调整偏移量
        x_off = int(input("水平偏移量(默认0): ") or "0")
        y_off_acc = int(input("账号垂直偏移(默认0): ") or "0")
        y_off_pwd = int(input("密码垂直偏移(默认0): ") or "0")
        y_off_login = int(input("登录垂直偏移(默认0): ") or "0")

        success = auto_login_adjustable(USERNAME, PASSWORD, x_off, y_off_acc, y_off_pwd, y_off_login)
        print("成功" if success else "失败")