import RealSense
import time

class RealSenseManager:

    def __init__(self):
        self.Rs = RealSense.RealSense()

    def config(self, stream_type, is_enabled, resolution):
        self.Rs.toggle_stream(stream_type, is_enabled, resolution)
        self.Rs.config_streams()
    
    def start(self):
        self.Rs.stop_streaming()
        self.Rs.restart_pipeline()
        self.Rs.restart_streaming()

    def stop(self):
        self.Rs.stop_streaming()
        self.Rs.stop_pipeline()

    
depth_resolutions = ["320 x 240", "640 x 480", "1024 x 768"]
infrared_resolutions = ["320 x 240", "640 x 480", "1024 x 768"]
color_resolutions = ["640 x 360", "640 x 480", "960 x 540", "1280 x 720", "1920 x 1080"]

def test_resolutions(manager, stream_type, resolutions):
    for resolution in resolutions:
        print(f"测试 {stream_type} 流, 分辨率 {resolution}")
        manager.config(stream_type, True, resolution)
        manager.start()
        time.sleep(2)  # 等待一段时间以便观察（如果需要）
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