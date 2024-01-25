import open3d as o3d
import numpy as np
import cv2
import os

# 修改目錄
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)
print(f"当前工作目录已更改为: {os.getcwd()}")

# 讀取深度影像
depth_image = cv2.imread("depth_image.png", cv2.IMREAD_UNCHANGED)
if depth_image is None:
    raise FileNotFoundError("未找到深度图像文件。")

# 將深度圖像轉換為點雲
# 假設深度圖像已經是以毫米為單位的深度值
# 你需要根據你的相機參數調整下面的fx， fy， cx， cy值
fx = 1.0  # 相機的焦距
fy = 1.0
cx = depth_image.shape[1] / 2  # 影像中心點
cy = depth_image.shape[0] / 2
depth_image = depth_image / 1000.0  # 將深度從毫米轉換為米
depth_image[depth_image == 0] = np.nan  # 將深度為0的點設置為nan，避免在點雲中顯示

# 建立點雲
points = []
for v in range(depth_image.shape[0]):
    for u in range(depth_image.shape[1]):
        Z = depth_image[v, u]
        if np.isnan(Z):  # 忽略無效點
            continue
        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy
        points.append([X, Y, Z])

point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)

# 視覺化點雲
o3d.visualization.draw_geometries([point_cloud])
