import numpy as np
import cv2
from PIL import Image, ImageTk

def process_color_image(color_image):
    color_colormap = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    color_colormap = Image.fromarray(color_colormap)
    color_colormap = ImageTk.PhotoImage(image=color_colormap)
    return color_colormap

def process_depth_image(depth_image):
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    depth_colormap = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2RGB)
    depth_colormap = Image.fromarray(depth_colormap)
    depth_colormap = ImageTk.PhotoImage(image=depth_colormap)
    return depth_colormap

def process_infrared_image(infrared_image):
    infrared_colormap = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2BGR)
    infrared_colormap = Image.fromarray(infrared_colormap)
    infrared_colormap = ImageTk.PhotoImage(image=infrared_colormap)
    return infrared_colormap
