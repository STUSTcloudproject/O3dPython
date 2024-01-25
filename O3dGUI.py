import open3d as o3d
import tkinter as tk
from PIL import Image, ImageTk
import pyrealsense2 as rs
import numpy as np
import cv2
import threading
import image_saver as iser
import stream_processing as spro

def update_image():
    global color_image, depth_image, infrared_image, stop_thread
    while not stop_thread:
        try:
            frames = pipeline.wait_for_frames()
        except rs.error as e:
            print(f"RealSense error: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")        
            continue

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        infrared_frame = frames.get_infrared_frame(0)

        if not color_frame or not depth_frame or not infrared_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data()) # Color Stream
        depth_image = np.asanyarray(depth_frame.get_data()) # Depth Stream
        infrared_image = np.asanyarray(infrared_frame.get_data()) # Infrared Stream

        color_colormap = spro.process_color_image(color_image)
        depth_colormap = spro.process_depth_image(depth_image)
        infrared_colormap = spro.process_infrared_image(infrared_image)

        window.after(0, update_gui, color_colormap, depth_colormap, infrared_colormap)

def update_gui(color_colormap, depth_colormap, infrared_colormap):
    label_color.config(image=color_colormap)
    label_color.image = color_colormap
    label_depth.config(image=depth_colormap)
    label_depth.image = depth_colormap
    label_infrared.config(image=infrared_colormap)
    label_infrared.image = infrared_colormap
    
# 拍照並保存圖像
def capture_and_save_images():
    global depth_image, color_image, infrared_image

    iser.save_color_image(color_image)
    iser.save_infrared_image(infrared_image)
    iser.save_depth_image(depth_image)      

# 關閉 Tkinter 視窗
def close_program():
    global stop_thread
    stop_thread = True

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
thread_update_image = threading.Thread(target=update_image)

thread_update_image.start()

# 運行 Tkinter 主循環
window.mainloop()

# 停止捕獲影像
stop_thread = True
thread_update_image.join()

pipeline.stop()
