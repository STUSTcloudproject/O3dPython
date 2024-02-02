import tkinter as tk
import Tkinter_Text as tktest
import RealSenseManager as rsm

def toggle_switch_changed(is_on, pane):
    try:
        combo_value = pane.sub_frame.combo.get()  # 获取 ComboBox 的当前值
        stream_type = ((pane.title_label['text']).split()[0]).split()[0].lower()
        rsm.config(stream_type, is_on, combo_value)
        rsm.start()

    except Exception as e:
        print(f"An error occurred: {e}")


app = tktest.App(toggle_callback=toggle_switch_changed)
rsm = rsm.RealSenseManager()
app.mainloop()

