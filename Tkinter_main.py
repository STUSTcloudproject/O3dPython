import tkinter as tk
import Tkinter_Text as tktest
import RealSenseManager as rsm
import threading

settings = {
    "color": False,
    "depth": False,
    "infrared": False
}

def toggle_switch_changed(is_on, pane):
    try:
        combo_value = pane.sub_frame.combo.get()  # 获取 ComboBox 的当前值
        stream_type = pane.title_label['text'].split()[0].lower()
        update_settings(stream_type, is_on)
        rsm.config(stream_type, is_on, combo_value)
        rsm.start()

    except Exception as e:
        print(f"An error occurred: {e}")

def update_settings(stream_type, is_on):
    if stream_type in settings:
        settings[stream_type] = is_on
    else:
        print(f"Invalid setting type: {stream_type}")

def background_worker(app, settings):
    while True:
        if settings['depth']:
            colormap = rsm.get_depth_colormap()
            app.right_panel.after(0, app.set_right_panel_image, colormap)

app = tktest.App(toggle_callback=toggle_switch_changed)
rsm = rsm.RealSenseManager()
worker_thread = threading.Thread(target=background_worker, args=(app, settings))
worker_thread.start()
app.mainloop()

