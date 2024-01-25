import cv2
import os

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
        cv2.imwrite(os.path.join(script_directory, file_path), color_image)

    
def save_infrared_image(infrared_image, folder_name="images"):
    if infrared_image is not None:
        file_path = os.path.join(folder_name, 'infrared_image.png')
        ensure_dir(file_path)
        cv2.imwrite(os.path.join(script_directory, file_path), infrared_image)

def save_depth_image(depth_image, folder_name="images"):
    if depth_image is not None:
        file_path = os.path.join(folder_name, 'depth_image.png')
        ensure_dir(file_path)
        cv2.imwrite(os.path.join(script_directory, file_path), depth_image)

"""
def capture_point_cloud_and_show():
    global last_depth_image, profile
    
    if last_depth_image is not None:
        print("正在生成点云...")
        # 获取深度图像的内参
        depth_intrinsic = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
        
        # 将深度图像转换为Open3D图像格式
        depth_o3d = o3d.geometry.Image(last_depth_image)
        
        # 从深度图像创建点云
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
        
        # 可以调整点云的位置和方向（视需要而定）
        pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        
        # 保存点云文件为PLY格式
        o3d.io.write_point_cloud("captured_point_cloud.ply", pcd)
        print("点云已保存为 captured_point_cloud.ply")

        # 显示点云
        o3d.visualization.draw_geometries([pcd], window_name="Captured Point Cloud", width=800, height=600)

"""
