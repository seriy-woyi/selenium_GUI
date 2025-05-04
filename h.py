import time
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from core import Type, Click


def get_step_text(step):
    return f"{step['location_type']}, {step['value']}, {step['operation_type']}, {step['keys']}, {step['wait_time']}"


class MainWindow:
    def __init__(self, master):
        master.title("Serial's自动化测试")
        try:
            image_file = "Macbook (1).png"
            bg_image = PhotoImage(file=image_file)
            bg_label = Label(master, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except TclError:
            print("图片加载失败，请检查图片路径。")

        # 解析 language.xml 文件
        tree = ET.parse("language.xml")
        root = tree.getroot()
        # 获取中文翻译
        self.zh_title_texts = [text_elem.text for text_elem in root.findall(".//lang[@name='中文']/title/*")]
        self.zh_btn_texts = [text_elem.text for text_elem in root.findall(".//lang[@name='中文']/button/*")]
        self.language = 'zh'
        self.language_combobox = ttk.Combobox(values=['中文', 'English', '日本語'])
        self.language_combobox.current(0)
        self.language_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)

        # 定义主框架
        self.frame_main = ttk.Frame(master, padding=20)
        self.frame_main.grid(column=0, row=0, sticky=(N, W, E, S))
        self.frame_main.columnconfigure(0, weight=1)
        master.geometry("550x400")

        # 定义URL输入框
        self.label_url = ttk.Label(self.frame_main, text=self.zh_title_texts[0])
        self.label_url.grid(column=0, row=0, sticky=(W, E))
        self.url_input = ttk.Entry(self.frame_main, width=40)
        self.url_input.insert(0, "https://www.baidu.com")
        self.url_input.grid(column=1, row=0, sticky=(W, E))

        # 定义元素步骤
        self.steps = []

        # 定义定位方式下拉框
        self.label_location_type = ttk.Label(self.frame_main, text=self.zh_title_texts[1])
        self.label_location_type.grid(column=0, row=1, sticky=(W, E))
        self.location_type_combobox = ttk.Combobox(self.frame_main, state="readonly", values=[
            "LINK_TEXT", "CLASS_NAME", "CSS_SELECTOR", "PARTIAL_LINK_TEXT",
            "XPATH", "TAG_NAME", "ID", "NAME"
        ])
        self.location_type_combobox.current(0)
        self.location_type_combobox.grid(column=1, row=1, sticky=(W, E))

        # 定义元素值输入框
        self.label_value = ttk.Label(self.frame_main, text=self.zh_title_texts[2])
        self.label_value.grid(column=0, row=2, sticky=(W, E))
        self.value_input = ttk.Entry(self.frame_main, width=40)
        self.value_input.grid(column=1, row=2, sticky=(W, E))

        # 定义操作类型下拉框
        self.label_operation_type = ttk.Label(self.frame_main, text=self.zh_title_texts[3])
        self.label_operation_type.grid(column=0, row=3, sticky=(W, E))
        self.operation_type_combobox = ttk.Combobox(self.frame_main, state="readonly", values=[
            self.zh_title_texts[5], self.zh_title_texts[6]
        ])
        self.operation_type_combobox.current(0)
        self.operation_type_combobox.grid(column=1, row=3, sticky=(W, E))
        self.operation_type_combobox.bind("<<ComboboxSelected>>", self.on_operation_type_changed)

        # 定义输入文本输入框（初始状态为隐藏）
        self.operation_type_button = ttk.Label(self.frame_main, text=self.zh_title_texts[4])
        self.operation_type_button.grid(column=0, row=4, sticky=(W, E))
        self.operation_type_button.grid_remove()
        self.keys_input = ttk.Entry(self.frame_main, width=40)
        self.keys_input.grid(column=1, row=4, sticky=(W, E))
        self.keys_input.grid_remove()

        # 定义添加步骤按钮
        self.add_step_button = ttk.Button(self.frame_main, text=self.zh_btn_texts[0], command=self.add_step)
        self.add_step_button.grid(column=0, row=6, columnspan=2)

        # 定义等待时间输入框
        self.label_operation_type = ttk.Label(self.frame_main, text=self.zh_title_texts[7])
        self.label_operation_type.grid(column=0, row=5, sticky=(W, E))
        self.wait_input = ttk.Entry(self.frame_main, width=40)
        self.wait_input.grid(column=1, row=5, sticky=(W, E))

        # 定义执行按钮
        self.execute_button = ttk.Button(self.frame_main, text=self.zh_btn_texts[1], command=self.execute)
        self.execute_button.grid(column=0, row=7, columnspan=2)

        # 定义步骤列表
        self.steps_list_box = Listbox(self.frame_main, width=60)
        self.steps_list_box.grid(column=0, row=8, columnspan=2)
        self.steps_list_box.bind("<<ListboxSelect>>", self.on_step_selected)

        # 定义删除步骤按钮
        self.delete_step_button = ttk.Button(self.frame_main, text=self.zh_btn_texts[3], command=self.delete_step)
        self.delete_step_button.grid(column=2, row=9)

        self.frame_main.place(relx=0.5, rely=0.5, anchor=CENTER)

    def change_language(self, event):
        # 设置当前语言
        if self.language_combobox.get() == '中文':
            self.language = 'zh'
        elif self.language_combobox.get() == 'English':
            self.language = 'en'
        else:
            self.language = 'jp'

        # 重新加载语言文本
        self.load_texts()

    def load_texts(self):
        tree = ET.parse("language.xml")
        root = tree.getroot()

        lang = '中文' if self.language == 'zh' else 'English' if self.language == 'en' else '日本語'
        title_texts = [text_elem.text for text_elem in root.findall(f".//lang[@name='{lang}']/title/*")]
        button_texts = [text_elem.text for text_elem in root.findall(f".//lang[@name='{lang}']/button/*")]

        # 更新标签文本
        self.label_url.config(text=title_texts[0])
        self.label_location_type.config(text=title_texts[1])
        self.label_value.config(text=title_texts[2])
        self.label_operation_type.config(text=title_texts[3])
        self.operation_type_button.config(text=title_texts[4])
        self.add_step_button.config(text=button_texts[0])
        self.execute_button.config(text=button_texts[1])
        self.delete_step_button.config(text=button_texts[3])

        self.zh_title_texts = title_texts
        self.zh_btn_texts = button_texts

        # 更新操作类型下拉框的值
        self.operation_type_combobox['values'] = [title_texts[5], title_texts[6]]

    def delete_step(self):
        # 获取选中项的索引
        index = self.steps_list_box.curselection()
        if len(index) == 0:
            return
        index = index[0]

        # 删除选中的步骤
        self.steps.pop(index)
        self.steps_list_box.delete(index)

    def on_step_selected(self, event):
        # 获取选中项的索引
        index = self.steps_list_box.curselection()
        if len(index) == 0:
            return
        index = index[0]

        # 获取选中项的内容
        step = self.steps[index]
        self.location_type_combobox.set(step["location_type"])
        self.value_input.delete(0, END)
        self.value_input.insert(0, step["value"])
        self.operation_type_combobox.set(step["operation_type"])
        if step["operation_type"] == self.zh_title_texts[6]:
            self.keys_input.delete(0, END)
            self.keys_input.insert(0, step["keys"])
            self.keys_input.grid()
        else:
            self.keys_input.delete(0, END)
            self.keys_input.grid_remove()
        self.wait_input.delete(0, END)
        self.wait_input.insert(0, step["wait_time"])

        def update_step():
            # 获取输入值
            location_type = self.location_type_combobox.get()
            value = self.value_input.get()
            operation_type = self.operation_type_combobox.get()

            # 如果未选择定位方式和操作类型，则不修改步骤
            if not location_type or not operation_type:
                return

            # 获取等待时间
            wait_time = self.wait_input.get()

            # 获取文本框的内容
            keys = self.keys_input.get()

            # 构造新步骤
            new_step = {
                "location_type": location_type,
                "value": value,
                "operation_type": operation_type,
                "keys": keys,
                "wait_time": wait_time,
            }

            # 更新步骤列表
            self.steps[index] = new_step
            self.steps_list_box.delete(index)
            self.steps_list_box.insert(index, get_step_text(new_step))

        # 定义一个“修改步骤”按钮，点击后弹出对话框，用于修改步骤
        update_button = ttk.Button(self.frame_main, text=self.zh_btn_texts[2], command=update_step)
        update_button.grid(column=2, row=8)

    def on_operation_type_changed(self, event):
        if self.operation_type_combobox.get() == self.zh_title_texts[6]:
            self.operation_type_button.grid()
            self.keys_input.grid()
        else:
            self.operation_type_button.grid_remove()
            self.keys_input.grid_remove()

    def add_step(self):
        # 获取输入值
        location_type = self.location_type_combobox.get()
        value = self.value_input.get()
        operation_type = self.operation_type_combobox.get()

        # 如果未选择定位方式和操作类型，则不添加步骤
        if not location_type or not operation_type:
            return

        # 获取等待时间
        wait_time = self.wait_input.get()

        # 获取文本框的内容
        keys = self.keys_input.get()

        # 添加到步骤列表中
        step = {
            "location_type": location_type,
            "value": value,
            "operation_type": operation_type,
            "keys": keys,
            "wait_time": wait_time,
        }

        # 如果当前选中了某个条目，则替换该条目所对应的步骤
        index = self.steps_list_box.curselection()
        if len(index) > 0:
            index = index[0]
            self.steps[index] = step
            self.steps_list_box.delete(index)
            self.steps_list_box.insert(index, get_step_text(step))
        else:
            self.steps.append(step)
            self.steps_list_box.insert(END, get_step_text(step))

        # 清空输入框
        self.location_type_combobox.current(0)
        self.value_input.delete(0, END)
        self.operation_type_combobox.current(0)
        self.keys_input.delete(0, END)
        self.keys_input.grid_remove()
        self.wait_input.delete(0, END)

    def execute(self):
        url = self.url_input.get()

        try:
            # 打开浏览器
            driver = webdriver.Edge()
            driver.get(url)
            # 实例化操作类
            type_obj = Type(driver)
            click_obj = Click(driver)

            for step in self.steps:
                location_type = step["location_type"]
                value = step["value"]
                operation_type = step["operation_type"]
                keys = step["keys"]
                wait_time = step["wait_time"]

                try:
                    by = getattr(By, location_type)
                    if operation_type == self.zh_title_texts[6]:
                        click_obj.click(by, value)
                    elif operation_type == self.zh_title_texts[5]:
                        type_obj.send_keys(by, value, keys)

                    # 执行等待操作
                    try:
                        wait_time = float(wait_time)
                        time.sleep(wait_time)
                    except ValueError:
                        pass  # 如果转换失败，则无需执行时间等待操作。
                except NoSuchElementException:
                    showerror("错误", f"未找到元素：{location_type}={value}")
                    break

            # 关闭浏览器
            driver.quit()

            # 任务执行完成后弹出提示框
            showinfo("提示", "操作已完成！")
        except Exception as e:
            showerror("错误", f"执行过程中出现错误：{str(e)}")


if __name__ == '__main__':
    root = Tk()
    main_window = MainWindow(root)
    root.mainloop()