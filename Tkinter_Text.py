import tkinter as tk
from tkinter import ttk

class CollapsiblePane(tk.Frame):
    def __init__(self, parent, title="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # 建立標題區域框架
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        # 在標題區域中添加標題標籤
        self.title_label = ttk.Label(self.title_frame, text=title)
        self.title_label.pack(side="left", fill="x", expand=1)

        # 添加一個切換按鈕，用於展開或折疊面板
        self.toggle_button = ttk.Button(self.title_frame, width=2, text='+', command=self.toggle)
        self.toggle_button.pack(side="right")

        # 建立子框架用於放置折疊的內容
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self._is_collapsed = True  # 面板的初始狀態為摺疊
        self.toggle()  # 調用toggle函數來應用初始狀態

    def toggle(self):
        # 根據當前狀態切換面板的展開或摺疊
        if self._is_collapsed:  # 如果面板目前是摺疊的
            self.sub_frame.pack(fill="x", expand=1)  # 展開內容區域
            self.toggle_button.configure(text='-')  # 切換按鈕顯示為“-”
        else:  # 如果面板目前是展開的
            self.sub_frame.forget()  # 摺疊內容區域
            self.toggle_button.configure(text='+')  # 切換按鈕顯示為“+”
        self._is_collapsed = not self._is_collapsed  # 更新摺疊狀態

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
        self.depth_stream = CollapsiblePane(self.left_panel, title="Depth Stream")
        self.depth_stream.pack(fill="x", expand=0)  # 摺疊時不佔用額外空間
        self.add_stream_setting(self.depth_stream.sub_frame, ["Option 1", "Option 2", "Option 3"])

        self.infrared_stream = CollapsiblePane(self.left_panel, title="Infrared Stream")
        self.infrared_stream.pack(fill="x", expand=0)
        self.add_stream_setting(self.infrared_stream.sub_frame, ["Option A", "Option B"])

        self.color_stream = CollapsiblePane(self.left_panel, title="Color Stream")
        self.color_stream.pack(fill="x", expand=0)
        self.add_stream_setting(self.color_stream.sub_frame, ["Option X", "Option Y", "Option Z"])

    # 在每個摺疊面板中添加設定選項
    def add_stream_setting(self, parent, options):
        # 為每個子面板添加詳細設定標籤和組合框以供選擇
        ttk.Label(parent, text="Detailed Settings").pack(side="top", fill="x", expand=0)
        combo = ttk.Combobox(parent, values=options)
        combo.pack(side="top", fill="x", expand=0)
        combo.current(0)

        # 新增多個設定選項
        for i in range(1, 4):
            ttk.Checkbutton(parent, text=f"Setting Option {i}").pack(side="top", fill="x", expand=0)

if __name__ == '__main__':
    app = App()
    app.mainloop()