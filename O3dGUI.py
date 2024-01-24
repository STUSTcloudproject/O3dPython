import tkinter as tk
from PIL import Image, ImageTk
import pyrealsense2 as rs
import numpy as np
import cv2
import threading

# RGB Camera
def update_color_image():
    global color_colormap, stop_thread, color_image
    while not stop_thread:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        color_colormap = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        color_colormap = Image.fromarray(color_colormap)
        color_colormap = ImageTk.PhotoImage(image=color_colormap)

        label_color.config(image=color_colormap)
        label_color.image = color_colormap
        window.update()

# Depth
def update_depth_image():
    global depth_colormap, depth_image, stop_thread
    while not stop_thread:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2RGB)
        depth_colormap = Image.fromarray(depth_colormap)
        depth_colormap = ImageTk.PhotoImage(image=depth_colormap)

        label_depth.config(image=depth_colormap)
        label_depth.image = depth_colormap
        window.update()


# Infrared
def update_infrared_image():
    global infrared_colormap, stop_thread, infrared_image
    while not stop_thread:
        frames = pipeline.wait_for_frames()
        infrared_frame = frames.get_infrared_frame(0)
        if not infrared_frame:
            continue

        infrared_image = np.asanyarray(infrared_frame.get_data())
        infrared_colormap = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2BGR)
        infrared_colormap = Image.fromarray(infrared_colormap)
        infrared_colormap = ImageTk.PhotoImage(image=infrared_colormap)

        label_infrared.config(image=infrared_colormap)
        label_infrared.image = infrared_colormap
        window.update()

# 拍照並保存圖像
def capture_and_save_images():
    global depth_image, color_image, infrared_image

    if depth_image is not None:
        cv2.imwrite('depth_image.png', depth_image)  # 直接保存原始深度圖像
    if color_image is not None:
        cv2.imwrite('color_image.png', color_image)
    if infrared_image is not None:
        cv2.imwrite('infrared_image.png', infrared_image)

# 關閉 Tkinter 視窗
def close_program():
    global stop_thread
    stop_thread = True

global color_image, depth_image, infrared_image
color_image = None
depth_image = None
infrared_image = None

# 初始化 RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.infrared, 0, 640, 480, rs.format.y8, 30)
pipeline.start(config)

# 建立 Tkinter
window = tk.Tk()
window.title("RealSense Camera Streams")

# 創建顯示彩色影像、深度影像和紅外線影像的標籤
label_color = tk.Label(window)
label_color.pack(side=tk.LEFT)

label_depth = tk.Label(window)
label_depth.pack(side=tk.LEFT)

label_infrared = tk.Label(window)
label_infrared.pack(side=tk.LEFT)

capture_button = tk.Button(window, text="Capture Images", command=capture_and_save_images)
capture_button.pack()

close_button = tk.Button(window, text="Close Program", command=close_program)
close_button.pack()

# 開始捕獲影像的線程
stop_thread = False
thread_color = threading.Thread(target=update_color_image)
thread_depth = threading.Thread(target=update_depth_image)
thread_infrared = threading.Thread(target=update_infrared_image)

thread_color.start()
thread_depth.start()
thread_infrared.start()

# 運行 Tkinter 主循環
window.mainloop()

# 停止捕獲影像
stop_thread = True
thread_color.join()
thread_depth.join()
thread_infrared.join()

pipeline.stop()
