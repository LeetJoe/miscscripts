import gradio as gr


ext_allowd = ['doc', 'docx', 'pdf']


def file(filelist, type):
    file_allowed = []
    for file in filelist:
        if ext_check(file):
            file_allowed.append(file)
    if type == 1:
        #  提取文本
        return "提取文本"
    elif type == 2:
        #  提取图片
        return "提取图片"
    else:
        #  提取文本+图片
        return "提取文本+图片"


def ext_check(file_name):
    file_extension = file_name.split(".")[-1]
    return file_extension in ext_allowd


# gr.Image() 作为输入时，在 fn 那里接收到的是一个 shape=(height, width, 3) 的 NumPy 类型的数组
# demo = gr.Interface(sepia, gr.Image(), "image")

# 定义了多个 gr.Interface 的实例的时候，只有第一个会正常工作，其余的执行了 launch() 也没用
'''
demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.Slider(step=1, value=2, minimum=1, maximum=10)],
    outputs=[gr.Textbox(label="greeting", lines=3)],
    title="Simple gradio",
    description="Repeat some Hello's to you",
    article="something text or markdown"
)
'''

# gr.Radio(['a', 'b', 'c'])  # 它的 label 同时也是它的 value

demo = gr.Interface(
    fn=file,
    inputs=[
        gr.Files(show_label=True, label="请选择文件(仅支持doc/docx/pdf格式，允许多选)", file_types=["file", ".doc", ".docs", ".pdf"]),
        gr.Radio([("文本", 1), ("图片", 2), ("文本+图片", 3)], value=1, label="提取内容")],
    outputs=["text"]
)

demo.launch()
