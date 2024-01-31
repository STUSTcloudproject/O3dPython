import tkinter as tk
from tkinter import ttk

class CollapsiblePane(tk.Frame):
    def __init__(self, parent, title="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # 建立標題區域框架
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)
        
        # 使用 Label 來模擬 button
        self.toggle_button = ttk.Label(self.title_frame, width=2, text='▶', cursor="hand2")
        self.toggle_button.pack(side="left")
        self.toggle_button.bind("<Button-1>", self.toggle)  # 綁定滑鼠左鍵點擊事件到 toggle 函數

        # 在標題區域中添加標題標籤
        self.title_label = ttk.Label(self.title_frame, text=title)
        self.title_label.pack(side="left", fill="x", expand=1)

        # 建立子框架用於放置折疊的內容
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self._is_collapsed = False  # 面板的初始狀態為摺疊
        self.toggle()  # 調用toggle函數來應用初始狀態

    def toggle(self, event=None):
        # 根據當前狀態切換面板的展開或摺疊
        if self._is_collapsed:
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='▼')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='▶')
        self._is_collapsed = not self._is_collapsed


class App(tk.Tk):
    def __init__(self):
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
        self.depth_stream = CollapsiblePane(self.left_panel, title="Depth Stream ")
        self.depth_stream.pack(fill="x", expand=0, padx=4, pady=4)  # 摺疊時不佔用額外空間
        self.add_stream_setting(self.depth_stream.sub_frame, ["320 x 240", "640 x 480", "1024 x 480", "1024 x 768"])

        self.infrared_stream = CollapsiblePane(self.left_panel, title="Infrared Stream ")
        self.infrared_stream.pack(fill="x", expand=0, padx=4, pady=4)
        self.add_stream_setting(self.infrared_stream.sub_frame, ["320 x 240", "640 x 480", "1024 x 480", "1024 x 768"])

        self.color_stream = CollapsiblePane(self.left_panel, title="Color Stream ")
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
        combo = ttk.Combobox(combo_frame, values=options)
        combo.pack(side="left", fill="x", expand=1)
        combo.current(0)  # 預設選擇第一個選項

        # 新增多個設置選項
        for i in range(1, 4):
            ttk.Checkbutton(parent, text=f"Setting Option {i}").pack(side="top", fill="x", expand=0)


if __name__ == '__main__':
    app = App()
    app.mainloop()