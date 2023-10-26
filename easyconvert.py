import PySimpleGUI as sg
import os
import torch
import threading

def convert_pth_2_onnx(pth_path,window):
    output_text = f"将.pth模型文件转换为.onnx格式文件：{file_path}\n"
    window["output"].update(output_text, append=True)
    # 输出路径就在pth文件所在目录下，用pth文件的原始文件名作为输出文件名
    output_path = f'{pth_path.split(".")[0]}.onnx'
    model = torch.load(pth_path, map_location='cpu')

    meta_info = model['meta'] if 'meta' in model else None
    if meta_info is None:
        print("Meta info not found!")
        window["output"].update("Meta info not found!\n", append=True)
        # return "Meta info not found! Please check your .pth file!"
    if meta_info['tool'] == 'BaseNN':
        print("BaseNN model detected!")
        window["output"].update("BaseNN model detected!\n", append=True)
        from BaseNN import nn
        nn_model = nn()
        nn_model.convert(checkpoint=pth_path, out_file=output_path)
        print(f"Convert successfully! Output path: {output_path}")
        window["output"].update(f"Convert successfully! Output path: {output_path}\n", append=True)
        # return f"Convert successfully! Output path: {output_path}"
    elif 'MMEdu' in meta_info['tool']:
        print("MMEdu model detected!")
        window["output"].update("MMEdu model detected!\n", append=True)
        backbone = meta_info['backbone']
        task = meta_info['task']
        if task=="Classification":
            print("Classification task detected!")
            window["output"].update("Classification task detected!\n", append=True)
            from MMEdu import MMClassification as cls
            cls_model = cls(backbone=backbone)
            cls_model.convert(checkpoint=pth_path, out_file=output_path)
            print(f"Convert successfully! Output path: {output_path}")
            window["output"].update(f"Convert successfully! Output path: {output_path}\n", append=True)
            # return f"Convert successfully! Output path: {output_path}"
        elif task=="Detection":
            print("Detection task detected!")
            window["output"].update("Detection task detected!\n", append=True)
            from MMEdu import MMDetection as det
            det_model = det(backbone=backbone)
            det_model.convert(checkpoint=pth_path, out_file=output_path)
            print(f"Convert successfully! Output path: {output_path}")
            window["output"].update(f"Convert successfully! Output path: {output_path}\n", append=True)
            # return f"Convert successfully! Output path: {output_path}"
        else:
            print("Task not supported yet!")
            window["output"].update("Task not supported yet!\n", append=True)
            # return "Task not supported yet!"
    else:
        print("Tool not supported yet!")
        window["output"].update("Tool not supported yet!\n", append=True)
        # return "Tool not supported yet!"

# 定义处理函数2
def process_file_option2(file_path):
    # 在这里执行模型操作2，这里仅仅打印文件路径作为示例
    output_text = f"处理文件（选项2）：{file_path}\n"
    window["output"].update(output_text, append=True)

# 定义GUI布局
layout = [
    [sg.Text("选择要处理的文件：")],
    [sg.InputText(key="file_path"), sg.FileBrowse(button_text="选择模型文件")],
    [sg.Text("选择操作选项：")],
    [sg.Radio("pth转onnx", "options", default=True, key="option1"), sg.Radio("onnx转pth", "options", key="option2")],
    [sg.Button("模型转换")],
    [sg.Multiline(size=(60, 20), key="output", autoscroll=True)],
    [sg.Button("退出")]
]

# 创建窗口
window = sg.Window("Easy Convert", layout)

# 事件循环
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "退出":
        break
    elif event == "模型转换":
        file_path = values["file_path"]
        option1_selected = values["option1"]
        option2_selected = values["option2"]

        if os.path.exists(file_path):
            if option1_selected:
                # use multithreading to avoid blocking the GUI
                thread_id = threading.Thread(
                    target=convert_pth_2_onnx,
                    args=(file_path,window,),
                    daemon=True)
                thread_id.start()
                # convert_pth_2_onnx(file_path)
            elif option2_selected:
                process_file_option2(file_path)
        else:
            window["output"].update("模型文件路径无效，请选择一个有效文件。\n", append=True)

# 关闭窗口
window.close()
