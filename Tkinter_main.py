import tkinter as tk
import Tkinter_Text as tktest
#import RealSenseManager

def toggle_switch_changed(is_on, pane):
    combo_value = pane.sub_frame.combo.get()  # 获取 ComboBox 的当前值
    if is_on:
        print(f"ToggleSwitch in {pane.title_label['text']} is turned ON. ComboBox value: {combo_value}")
        app.set_right_panel_text(f"ToggleSwitch in {pane.title_label['text']} is turned ON. ComboBox value: {combo_value}")
    else:
        print(f"ToggleSwitch in {pane.title_label['text']} is turned OFF. ComboBox value: {combo_value}") 
        app.set_right_panel_text(f"ToggleSwitch in {pane.title_label['text']} is turned OFF. ComboBox value: {combo_value}") 
    # 这里你可以根据需要访问 pane 的其他属性

app = tktest.App(toggle_callback=toggle_switch_changed)
#rlsm = RealSenseManager()
app.mainloop()

