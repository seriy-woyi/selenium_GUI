import tkinter as tk
from tkinter import messagebox
from h import MainWindow

def raise_custom_exception():
    try:
        raise ("This is a custom exception.")
    except CustomException as e:
        # 在可视化界面中显示提示窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showerror("Custom Exception", str(e))
        root.destroy()

# 示例调用函数
raise_custom_exception()

# 示例调用函数
def show_token_length_error():
    pass


show_token_length_error()
