import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QLabel, QStatusBar, QCheckBox,
                             QPushButton, QComboBox, QGroupBox, QFormLayout, QFrame)

class CollapsibleBox(QGroupBox):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(title, parent)
        
        self.toggleButton = QPushButton(title)
        self.toggleButton.setStyleSheet("QPushButton { text-align: left; }")
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)
        
        self.toggleButton.clicked.connect(self.on_pressed)
        
        self.contentArea = QFrame()
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.toggleButton)
        self.layout.addWidget(self.contentArea)
        
        self.setLayout(self.layout)
        self.contentArea.setVisible(False)

    def on_pressed(self):
        checked = self.toggleButton.isChecked()
        self.contentArea.setVisible(checked)

    def add_content(self, layout):
        self.contentArea.setLayout(layout)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('仿 Intel RealSense Viewer')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建一个 QWidget 作为主窗口中央控件
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        # 水平布局
        hbox = QHBoxLayout(self.centralWidget)
        
        # 控制面板
        controlPanelLayout = QVBoxLayout()
        
        # 向控制面板添加可折叠组件
        self.addCollapsibleBox(controlPanelLayout, "Depth Stream", ["Option 1", "Option 2", "Option 3"])
        self.addCollapsibleBox(controlPanelLayout, "Infrared Stream", ["Option A", "Option B"])
        self.addCollapsibleBox(controlPanelLayout, "Color Stream", ["Option X", "Option Y", "Option Z"])

        controlPanel = QWidget()
        controlPanel.setLayout(controlPanelLayout)
        
        # 3D视觉化区域
        visualizationArea = QLabel("这里是3D视觉化区域的代替品")
        visualizationArea.setStyleSheet("background-color: gray; color: white; text-align: center")
        
        # 使用 QSplitter 创建可调节大小的分割窗口
        splitter = QSplitter(self.centralWidget)
        splitter.addWidget(controlPanel)
        splitter.addWidget(visualizationArea)
        splitter.setSizes([200, 600])  # 初始化大小比例
        
        hbox.addWidget(splitter)
        
        # 状态栏
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.showMessage("就绪")

    def addCollapsibleBox(self, layout, title, options):
        box = CollapsibleBox(title)
        formLayout = QFormLayout()
        
        comboBox = QComboBox()
        comboBox.addItems(options)
        formLayout.addRow("详细设置", comboBox)
        
        for i in range(1, 4):
            checkBox = QCheckBox(f"设置选项 {i}")
            formLayout.addRow(checkBox)
        
        box.add_content(formLayout)
        layout.addWidget(box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
