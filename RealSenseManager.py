import pyrealsense2 as rs
import time

class RealSenseManager:
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

        # 重新配置流
        self.config_streams()

        # 重启 pipeline
        self.restart_pipeline()

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
            print(f"An error occurred when restarting the pipeline: {e}")

    def stop(self):
        if self.is_pipeline_started:
            # 停止 pipeline
            self.pipeline.stop()
            self.is_pipeline_started = False  # 更新标志状态

depth_resolutions = ["320 x 240", "640 x 480", "1024 x 768"]
infrared_resolutions = ["320 x 240", "640 x 480", "1024 x 768"]
color_resolutions = ["640 x 360", "640 x 480", "960 x 540", "1280 x 720", "1920 x 1080"]

def test_resolutions(manager, stream_type, resolutions):
    for resolution in resolutions:
        print(f"测试 {stream_type} 流, 分辨率 {resolution}")
        manager.toggle_stream(stream_type, True, resolution)
        time.sleep(0.5)  # 等待一段时间以便观察（如果需要）
        manager.stop()
        print(f"测试 {stream_type} 流, 分辨率 {resolution} 完成\n")

if __name__ == '__main__':
    manager = RealSenseManager()

    try:
        # 测试深度流的每种分辨率
        test_resolutions(manager, 'depth', depth_resolutions)

        # 测试红外流的每种分辨率
        test_resolutions(manager, 'infrared', infrared_resolutions)

        # 测试彩色流的每种分辨率
        test_resolutions(manager, 'color', color_resolutions)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        manager.stop()  # 确保最终会停止 pipeline


