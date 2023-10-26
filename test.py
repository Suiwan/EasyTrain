import sys
import os
import torch
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QRadioButton, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, pyqtSlot

class ModelConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Easy Convert")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.file_label = QLabel("选择要处理的文件：", self)
        self.layout.addWidget(self.file_label)

        self.file_path = None
        self.file_path_label = QLabel("", self)
        self.layout.addWidget(self.file_path_label)

        self.browse_button = QPushButton("选择模型文件", self)
        self.browse_button.clicked.connect(self.browseFile)
        self.layout.addWidget(self.browse_button)

        self.options_label = QLabel("选择操作选项：", self)
        self.layout.addWidget(self.options_label)

        self.option1 = QRadioButton("pth转onnx", self)
        self.option1.setChecked(True)
        self.layout.addWidget(self.option1)

        self.option2 = QRadioButton("onnx转pth", self)
        self.layout.addWidget(self.option2)

        self.convert_button = QPushButton("模型转换", self)
        self.convert_button.clicked.connect(self.convertModel)
        self.layout.addWidget(self.convert_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.centralWidget.setLayout(self.layout)

    @pyqtSlot()
    def browseFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("模型文件 (*.pth *.onnx)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.file_path = file_paths[0]
                self.file_path_label.setText(self.file_path)

    @pyqtSlot()
    def convertModel(self):
        if self.file_path is not None:
            option1_selected = self.option1.isChecked()
            option2_selected = self.option2.isChecked()

            if option1_selected:
                thread_id = threading.Thread(
                    target=self.convert_pth_2_onnx,
                    daemon=True)
                thread_id.start()
            elif option2_selected:
                self.process_file_option2()
        else:
            self.output_text.append("模型文件路径无效，请选择一个有效文件。")

    def convert_pth_2_onnx(self):
        self.output_text.append(f"将.pth模型文件转换为.onnx格式文件：{self.file_path}")
        output_path = f'{self.file_path.split(".")[0]}.onnx'
        model = torch.load(self.file_path, map_location='cpu')
        # ... 其余的转换代码 ...
        meta_info = model['meta'] if 'meta' in model else None
        if meta_info is None:
            print("Meta info not found!")
            self.output_text.append("Meta info not found!")
            # return "Meta info not found! Please check your .pth file!"
        if meta_info['tool'] == 'BaseNN':
            print("BaseNN model detected!")
            self.output_text.append("BaseNN model detected!")
            from BaseNN import nn
            nn_model = nn()
            nn_model.convert(checkpoint=self.file_path, out_file=output_path)
            print(f"Convert successfully! Output path: {output_path}")
            self.output_text.append(f"Convert successfully! Output path: {output_path}")
            # window["output"].update(f"Convert successfully! Output path: {output_path}\n", append=True)
            # return f"Convert successfully! Output path: {output_path}"
        elif 'MMEdu' in meta_info['tool']:
            print("MMEdu model detected!")
            self.output_text.append("MMEdu model detected!")
            backbone = meta_info['backbone']
            task = meta_info['task']
            if task=="Classification":
                print("Classification task detected!")
                self.output_text.append("Classification task detected!")
                from MMEdu import MMClassification as cls
                cls_model = cls(backbone=backbone)
                cls_model.convert(checkpoint=self.file_path, out_file=output_path)
                print(f"Convert successfully! Output path: {output_path}")
                self.output_text.append(f"Convert successfully! Output path: {output_path}")
                # return f"Convert successfully! Output path: {output_path}"
            elif task=="Detection":
                print("Detection task detected!")
                self.output_text.append("Detection task detected!")
                from MMEdu import MMDetection as det
                det_model = det(backbone=backbone)
                det_model.convert(checkpoint=self.file_path, out_file=output_path)
                print(f"Convert successfully! Output path: {output_path}")
                self.output_text.append(f"Convert successfully! Output path: {output_path}")
                # return f"Convert successfully! Output path: {output_path}"
            else:
                print("Task not supported yet!")
                self.output_text.append("Task not supported yet!")
                # return "Task not supported yet!"
        else:
            print("Tool not supported yet!")
            self.output_text.append("Tool not supported yet!")
            # return "Tool not supported yet!"

    def process_file_option2(self):
        self.output_text.append(f"处理文件（选项2）：{self.file_path}")

def main():
    app = QApplication(sys.argv)
    window = ModelConverter()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
