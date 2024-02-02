import pyrealsense2 as rs
import threading
import numpy as np
import stream_processing as spro
import time

class RealSense:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.is_color_enabled = False
        self.color_resolution = '320 x 240'
        self.is_depth_enabled = False
        self.depth_resolution = '320 x 240'
        self.is_infrared_enabled = False
        self.infrared_resolution = '640 x 360'
        self.is_pipeline_started = False

        self.stop_thread = False
        self.thread = None
        
        self.depth_image = None
        self.depth_colormap = None
        

    def toggle_stream(self, stream_type, is_enabled, resolution):
        # 更新流状态
        if stream_type == 'color':
            self.is_color_enabled = is_enabled
            self.color_resolution = resolution
        elif stream_type == 'depth':
            self.is_depth_enabled = is_enabled
            self.depth_resolution = resolution
        elif stream_type == 'infrared':
            self.is_infrared_enabled = is_enabled
            self.infrared_resolution = resolution
        else:
            raise ValueError("Unknown stream type")

    def config_streams(self):
        # 清除之前的配置
        self.config = rs.config()

        # 根据当前状态配置流
        if self.is_color_enabled:
            resolution_no_spaces = ''.join(self.color_resolution.split())
            parts = resolution_no_spaces.split('x')
            self.config.enable_stream(rs.stream.color, int(parts[0]), int(parts[1]), rs.format.bgr8, 30)
            
        if self.is_depth_enabled:
            resolution_no_spaces = ''.join(self.depth_resolution.split())
            parts = resolution_no_spaces.split('x')
            self.config.enable_stream(rs.stream.depth, int(parts[0]), int(parts[1]), rs.format.z16, 30)
            
        if self.is_infrared_enabled:
            resolution_no_spaces = ''.join(self.infrared_resolution.split())
            parts = resolution_no_spaces.split('x')
            self.config.enable_stream(rs.stream.infrared, 0, int(parts[0]), int(parts[1]), rs.format.y8, 30)

    def restart_pipeline(self):
        try:
            if self.is_pipeline_started:
                self.pipeline.stop()
                self.is_pipeline_started = False

            self.pipeline.start(self.config)
            self.is_pipeline_started = True
        
        except Exception as e:
            self.is_pipeline_started = False
            print(f"An error occurred when restarting the pipeline: {e}")
            raise e

    def stop_pipeline(self):
        try:
            if self.is_pipeline_started:
                self.pipeline.stop()
                self.is_pipeline_started = False

        except Exception as e:
            self.is_pipeline_started = False
            print(f"An error occurred when stopping the pipeline: {e}")
            raise e 
    
    def update_image(self):
        while not self.stop_thread:
            if self.is_color_enabled or self.is_depth_enabled or self.is_infrared_enabled:
                try:
                    frames = self.pipeline.wait_for_frames()
                except rs.error as e:
                    print(f"RealSense error: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error: {e}")        

                depth_frame = frames.get_depth_frame()

                if not depth_frame:
                    continue

                self.depth_image = np.asanyarray(depth_frame.get_data())

                self.depth_colormap = spro.process_depth_image(self.depth_image)

                print('更新完成')

                time.sleep(0.5)

    def restart_streaming(self):
        # 确保在启动新线程前旧线程已经停止
        if self.thread is not None and self.thread.is_alive():
            self.stop_streaming()
            self.thread.join(timeout=1)  # 等待最多5秒让旧线程结束

            if self.thread.is_alive():
                print("Warning: Old streaming thread did not stop properly.")

        self.stop_thread = False
        try:
            self.thread = threading.Thread(target=self.update_image)
            self.thread.start()
        except Exception as e:
            print(f"An error occurred when starting the streaming thread: {e}")

    def stop_streaming(self):
        self.stop_thread = True
        if self.thread is not None:
            try:
                self.thread.join()

            except Exception as e:
                print(f"An error occurred when stopping the thread: {e}")
                raise e