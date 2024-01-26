import cv2
import os
import open3d as o3d
import pyrealsense2 as rs

script_directory = os.path.dirname(os.path.abspath(__file__))

def ensure_dir(file_path):
    """
    確保目錄存在。 如果目錄不存在，則創建它。
    """
    directory = os.path.join(script_directory, os.path.dirname(file_path))
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_color_image(color_image, folder_name="images"):
    if color_image is not None:
        file_path = os.path.join(folder_name, 'color_image.png')
        ensure_dir(file_path)
        full_path = os.path.join(script_directory, file_path)
        cv2.imwrite(full_path, color_image)
        print(f"Color image has been saved to {full_path}")

    
def save_infrared_image(infrared_image, folder_name="images"):
    if infrared_image is not None:
        file_path = os.path.join(folder_name, 'infrared_image.png')
        ensure_dir(file_path)
        full_path = os.path.join(script_directory, file_path)
        cv2.imwrite(full_path, infrared_image)
        print(f"Infrared image has been saved to {full_path}")

def save_depth_image(depth_image, folder_name="images"):
    if depth_image is not None:
        file_path = os.path.join(folder_name, 'depth_image.png')
        ensure_dir(file_path)
        full_path = os.path.join(script_directory, file_path)
        cv2.imwrite(full_path, depth_image)
        print(f"Depth image has been saved to {full_path}")



def save_point_cloud(depth_image, profile, folder_name="images"):
    if depth_image is not None:

        # 獲取深度圖像的內參
        depth_intrinsic = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
        
        # 將深度圖像轉換為Open3D圖像格式
        depth_o3d = o3d.geometry.Image(depth_image)
        
        # 從深度圖像創建點雲
        pcd = o3d.geometry.PointCloud.create_from_depth_image(
            depth_o3d, 
            o3d.camera.PinholeCameraIntrinsic(
                depth_intrinsic.width, 
                depth_intrinsic.height, 
                depth_intrinsic.fx, 
                depth_intrinsic.fy, 
                depth_intrinsic.ppx, 
                depth_intrinsic.ppy
            )
        )
        
        # 可以調整點雲的位置和方向（視需要而定）
        pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        
        
        # 確保目錄存在
        file_path = os.path.join(folder_name, 'captured_point_cloud.ply')
        ensure_dir(file_path)
        
        # 保存點雲檔為PLY格式
        full_path = os.path.join(script_directory, file_path)
        o3d.io.write_point_cloud(full_path, pcd)
        print(f"Point cloud has been saved to {full_path}")

        # 显示点云
        #o3d.visualization.draw_geometries([pcd], window_name="Captured Point Cloud", width=800, height=600)


