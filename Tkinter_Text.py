import tkinter as tk
from tkinter import ttk

class CollapsiblePane(tk.Frame):
    def __init__(self, parent, title="", toggle_callback=None):
        super().__init__(parent)

        # 建立標題區域框架
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)
        
        # 使用 Label 來模擬 button
        self.details_button = ttk.Label(self.title_frame, width=2, text='▶', cursor="hand2")
        self.details_button.pack(side="left")
        self.details_button.bind("<Button-1>", self.toggle)  # 綁定滑鼠左鍵點擊事件到 toggle 函數

        # 在標題區域中添加標題標籤
        self.title_label = ttk.Label(self.title_frame, text=title)
        self.title_label.pack(side="left", fill="x", expand=1)

        self.toggle_switch = ToggleSwitch(self.title_frame, pane=self, callback=toggle_callback)
        self.toggle_switch.pack(side="right")

        # 建立子框架用於放置折疊的內容
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self._is_collapsed = False  # 面板的初始狀態為摺疊
        self.toggle()  # 調用toggle函數來應用初始狀態

    def toggle(self, event=None):
        # 根據當前狀態切換面板的展開或摺疊
        if self._is_collapsed:
            self.sub_frame.pack(fill="x", expand=1)
            self.details_button.configure(text='▼')
        else:
            self.sub_frame.forget()
            self.details_button.configure(text='▶')
        self._is_collapsed = not self._is_collapsed

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, pane, callback=None):
        super().__init__(parent, width=40, height=20, bg='red')  # 明确指定所有参数，不使用*args和**kwargs
        self.pane = pane
        self.callback = callback  # 保存回调函数
        self.is_on = False
        self.bind("<Button-1>", self.toggle)
        self.create_oval(2, 2, 22, 22, fill="white", outline="", tag="slider")

    def toggle(self, event):
        self.is_on = not self.is_on
        if self.is_on:
            self.move("slider", 20, 0)
            self['bg'] = 'green'
        else:
            self.move("slider", -20, 0)
            self['bg'] = 'red'
        if self.callback:  # 检查回调函数是否存在
            self.callback(self.is_on, self.pane)  # 调用回调函数，并传递开关的当前状态

class App(tk.Tk):
    def __init__(self, toggle_callback=None):
        super().__init__()
        # 設定應用視窗的標題和大小
        self.title('Intel RealSense Viewer')
        self.geometry('800x600')

        # 建立一個可分隔視窗pane
        self.pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=1)

        # 在pane中添加左側和右側的面板
        self.left_panel = tk.Frame(self.pane, width=200)
        self.right_panel = tk.Label(self.pane, text="This is an alternative to the 3D visualization area", bg='gray', fg='white')
        self.right_panel.pack(fill="both", expand=True)
        self.pane.add(self.left_panel, weight=1)
        self.pane.add(self.right_panel, weight=3)

        # 添加可摺疊面板並設置其內容
        self.depth_stream = CollapsiblePane(self.left_panel, title="Depth Stream ", toggle_callback=toggle_callback)
        self.depth_stream.pack(fill="x", expand=0, padx=4, pady=4)  # 摺疊時不佔用額外空間
        self.add_stream_setting(self.depth_stream.sub_frame, ["320 x 240", "640 x 480", "1024 x 768"])

        self.infrared_stream = CollapsiblePane(self.left_panel, title="Infrared Stream ", toggle_callback=toggle_callback)
        self.infrared_stream.pack(fill="x", expand=0, padx=4, pady=4)
        self.add_stream_setting(self.infrared_stream.sub_frame, ["320 x 240", "640 x 480", "1024 x 768"])

        self.color_stream = CollapsiblePane(self.left_panel, title="Color Stream ", toggle_callback=toggle_callback)
        self.color_stream.pack(fill="x", expand=0, padx=4, pady=4)
        self.add_stream_setting(self.color_stream.sub_frame, ["640 x 360", "640 x 480", "960 x 540", "1280 x 720", "1920 x 1080"])

    # 在每個摺疊面板中添加設定選項
    def add_stream_setting(self, parent, options):
        # 添加詳細設定的標題
        ttk.Label(parent, text="Detailed Settings").pack(side="top", fill="x", expand=0)
        
        # 建立框架以組織下拉框和其標籤
        combo_frame = ttk.Frame(parent)
        combo_frame.pack(side="top", fill="x", expand=0)

        # 在下拉框旁添加標籤說明
        ttk.Label(combo_frame, text="Resolution : ").pack(side="left")

        # 建立下拉框
        parent.combo = ttk.Combobox(combo_frame, values=options)
        parent.combo.pack(side="left", fill="x", expand=1)
        parent.combo.current(0)  # 預設選擇第一個選項

        # 新增多個設置選項
        for i in range(1, 4):
            ttk.Checkbutton(parent, text=f"Setting Option {i}").pack(side="top", fill="x", expand=0)

    def set_right_panel_text(self, text):
        self.right_panel.config(text=text)  # 更新 right_panel 的 text 属性

    
if __name__ == '__main__':
    app = App()
    app.mainloop()