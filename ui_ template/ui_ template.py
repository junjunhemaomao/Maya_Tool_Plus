from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


# ========================
# UI相关函数
# ========================
def maya_main_window():
    """获取Maya主窗口"""
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class ModelingToolsUI(QtWidgets.QDialog):
    """3D助手工具UI"""

    def __init__(self, parent=maya_main_window()):
        super(ModelingToolsUI, self).__init__(parent)
        self.setWindowTitle("3D Assistant Tools")
        self.setFixedWidth(400)
        # 移除了窗口右上角的问号按钮
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """创建UI组件"""
        # 标题
        self.title_label = QtWidgets.QLabel("3D Modeling Assistant")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #2c3e50;
                color: white;
                border-radius: 4px;
            }
        """)

        # 标签页控件
        self.tabs = QtWidgets.QTabWidget()

        # 建模页组件
        self.btn_modeling = QtWidgets.QPushButton("合并到中心")
        self.btn_modeling.setMinimumHeight(40)

        # 相机页组件
        self.btn_camera = QtWidgets.QPushButton("创建透视相机")
        self.btn_camera.setMinimumHeight(40)

        # 材质页组件
        self.btn_material = QtWidgets.QPushButton("分配红色材质")
        self.btn_material.setStyleSheet("background-color: #ff0000; color: white;")
        self.btn_material.setMinimumHeight(40)

        # 灯光页组件
        self.btn_lighting = QtWidgets.QPushButton("创建区域光")
        self.btn_lighting.setMinimumHeight(40)

        # 渲染页组件
        self.btn_rendering = QtWidgets.QPushButton("打开渲染视图")
        self.btn_rendering.setMinimumHeight(40)

        # 底部信息
        self.label_footer = QtWidgets.QLabel("v1.0")
        self.label_footer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_footer.setStyleSheet("color: gray;")

    def create_layout(self):
        """布局UI组件"""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.label_footer)

        # 建模页布局
        modeling_page = QtWidgets.QWidget()
        modeling_layout = QtWidgets.QVBoxLayout(modeling_page)
        modeling_layout.setContentsMargins(10, 10, 10, 10)

        modeling_group = QtWidgets.QGroupBox("建模工具")
        group_layout = QtWidgets.QVBoxLayout()
        group_layout.addWidget(self.btn_modeling)
        modeling_group.setLayout(group_layout)

        modeling_layout.addWidget(modeling_group)
        modeling_layout.addStretch()

        # 相机页布局
        cam_page = QtWidgets.QWidget()
        cam_layout = QtWidgets.QVBoxLayout(cam_page)
        cam_layout.setContentsMargins(10, 10, 10, 10)

        cam_group = QtWidgets.QGroupBox("相机工具")
        group_layout = QtWidgets.QVBoxLayout()
        group_layout.addWidget(self.btn_camera)
        cam_group.setLayout(group_layout)

        cam_layout.addWidget(cam_group)
        cam_layout.addStretch()

        # 材质页布局
        mat_page = QtWidgets.QWidget()
        mat_layout = QtWidgets.QVBoxLayout(mat_page)
        mat_layout.setContentsMargins(10, 10, 10, 10)

        mat_group = QtWidgets.QGroupBox("材质工具")
        group_layout = QtWidgets.QVBoxLayout()
        group_layout.addWidget(self.btn_material)
        mat_group.setLayout(group_layout)

        mat_layout.addWidget(mat_group)
        mat_layout.addStretch()

        # 灯光页布局
        light_page = QtWidgets.QWidget()
        light_layout = QtWidgets.QVBoxLayout(light_page)
        light_layout.setContentsMargins(10, 10, 10, 10)

        light_group = QtWidgets.QGroupBox("灯光工具")
        group_layout = QtWidgets.QVBoxLayout()
        group_layout.addWidget(self.btn_lighting)
        light_group.setLayout(group_layout)

        light_layout.addWidget(light_group)
        light_layout.addStretch()

        # 渲染页布局
        render_page = QtWidgets.QWidget()
        render_layout = QtWidgets.QVBoxLayout(render_page)
        render_layout.setContentsMargins(10, 10, 10, 10)

        render_group = QtWidgets.QGroupBox("渲染工具")
        group_layout = QtWidgets.QVBoxLayout()
        group_layout.addWidget(self.btn_rendering)
        render_group.setLayout(group_layout)

        render_layout.addWidget(render_group)
        render_layout.addStretch()

        # 添加标签页
        self.tabs.addTab(modeling_page, "建模")
        self.tabs.addTab(cam_page, "相机")
        self.tabs.addTab(mat_page, "材质")
        self.tabs.addTab(light_page, "灯光")
        self.tabs.addTab(render_page, "渲染")

    def create_connections(self):
        """连接信号和槽"""
        self.btn_modeling.clicked.connect(lambda: print("执行: 合并到中心"))
        self.btn_camera.clicked.connect(lambda: print("执行: 创建透视相机"))
        self.btn_material.clicked.connect(lambda: print("执行: 分配红色材质"))
        self.btn_lighting.clicked.connect(lambda: print("执行: 创建区域光"))
        self.btn_rendering.clicked.connect(lambda: print("执行: 打开渲染视图"))


# ========================
# 主函数
# ========================
def showUI():
    """显示UI"""
    dialog = ModelingToolsUI()
    dialog.show()


# 启动UI
showUI()