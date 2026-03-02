from pywinauto import Application
import time
import pywinauto.keyboard as keyboard


def login_tdx(account, password, exe_path=None):
  """
  自动登录通达信金融终端

  Args:
      account: 账号
      password: 密码
      exe_path: 通达信可执行文件路径（如果不指定，则连接到已打开的窗口）
  """

  # 如果没有指定exe路径，则连接到已运行的进程
  if exe_path:
    # 启动通达信
    app = Application().start(exe_path)
    print("正在启动通达信...")
  else:
    # 连接到已打开的窗口
    app = Application().connect(class_name="#32770", title="通达信金融终端V7.72")
    print("已连接到通达信窗口")

  # 等待窗口加载
  time.sleep(3)

  try:
    # 获取登录窗口
    dlg = app.window(class_name="#32770", title="通达信金融终端V7.72")

    # 方法1：通过controlID查找登录按钮并点击
    login_btn = dlg.child_window(control_id=0x00000001)
    print("找到登录按钮")

    # 方法2：通过类名和文本查找输入框（账号和密码）
    # 通常账号和密码输入框是Edit类型
    edit_controls = dlg.children(class_name="Edit")

    if len(edit_controls) >= 2:
      # 第一个Edit通常是账号输入框
      account_edit = edit_controls[0]
      account_edit.set_text(account)
      print(f"已输入账号: {account}")

      time.sleep(0.5)

      # 第二个Edit通常是密码输入框
      password_edit = edit_controls[1]
      password_edit.set_text(password)
      print("已输入密码")

      time.sleep(0.5)

      # 点击登录按钮
      login_btn.click()
      print("点击登录按钮")

    else:
      print("未找到输入框，尝试其他方法...")
      # 备用方法：使用键盘操作
      login_dlg_set_focus(dlg, account, password)

  except Exception as e:
    print(f"出现错误: {e}")
    # 尝试备用方法
    login_dlg_set_focus(dlg, account, password)


def login_dlg_set_focus(dlg, account, password):
  """备用方法：设置焦点后使用键盘输入"""
  try:
    # 确保窗口在最前
    dlg.set_focus()

    # 使用键盘输入
    time.sleep(1)
    keyboard.send_keys(account)
    time.sleep(0.5)
    keyboard.send_keys('{TAB}')  # 切换到密码框
    time.sleep(0.5)
    keyboard.send_keys(password)
    time.sleep(0.5)
    keyboard.send_keys('{ENTER}')  # 回车登录

    print("使用键盘输入完成")

  except Exception as e:
    print(f"备用方法也失败了: {e}")


def find_all_windows():
  """查找所有通达信窗口，用于调试"""
  from pywinauto.findwindows import find_windows

  windows = find_windows(class_name="#32770")
  for i, hwnd in enumerate(windows):
    from pywinauto import win32functions
    title = win32functions.GetWindowText(hwnd)
    print(f"窗口{i}: {title} - {hex(hwnd)}")

    # 获取详细信息
    try:
      app = Application().connect(handle=hwnd)
      dlg = app.window(handle=hwnd)
      print(f"  控件信息:")
      for ctrl in dlg.children():
        print(f"    类名: {ctrl.class_name()}, 控件ID: {ctrl.control_id()}, 文本: {ctrl.window_text()}")
    except:
      pass


def enhanced_login_tdx(account, password):
  """增强版登录：包含窗口查找和多种尝试"""

  # 先查找所有窗口
  find_all_windows()

  try:
    # 尝试连接到已打开的窗口
    app = Application().connect(class_name="#32770", title="通达信金融终端V7.72")
    dlg = app.window(class_name="#32770", title="通达信金融终端V7.72")

    print(f"窗口句柄: {dlg.handle}")
    print(f"窗口文本: {dlg.window_text()}")

    # 打印所有子控件
    print("所有控件:")
    for ctrl in dlg.children():
      print(f"  类名: {ctrl.class_name()}, 控件ID: {ctrl.control_id()}, 文本: {ctrl.window_text()}")

    # 尝试多种方式查找输入框
    # 方式1: 通过类名查找
    edit_boxes = dlg.children(class_name="Edit")
    if edit_boxes:
      edit_boxes[0].set_text(account)
      edit_boxes[1].set_text(password)

    # 方式2: 通过控件ID查找（需要知道具体ID）
    # 账号框控件ID通常是某个值，可以通过上面打印的信息获取

    # 查找登录按钮
    login_btn = None
    # 通过控件ID查找
    login_btn = dlg.child_window(control_id=1)
    if login_btn.exists():
      login_btn.click()
    else:
      # 通过文本查找
      login_btn = dlg.child_window(title="登录", class_name="Button")
      if login_btn.exists():
        login_btn.click()

    print("登录操作完成")

  except Exception as e:
    print(f"增强版登录出错: {e}")


if __name__ == "__main__":
  # 配置您的账号密码
  account = "15001868406"
  password = "wang521wei"

  # 可选：指定通达信可执行文件路径
  # tdx_path = r"C:\new_tdx\TdxW.exe"

  # 方法1：如果通达信已打开，直接连接
  print("尝试登录...")
  login_tdx(account, password)

  # 方法2：如果需要启动通达信，使用下面这行
  # login_tdx(account, password, exe_path=tdx_path)

  # 方法3：使用增强版（推荐先运行一次查看控件信息）
  # enhanced_login_tdx(account, password)

  print("脚本执行完成")
