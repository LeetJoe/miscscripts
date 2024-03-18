import gradio as gr


ext_allowd = ['doc', 'docx', 'pdf']


def file(filelist, type, html, btn):
    file_allowed = []
    for file in filelist:
        if ext_check(file):
            file_allowed.append(file)

    html = (
        "<div style='max-width:100%; max-height:360px; overflow:auto'>"
        + "<a href='https://www.baidu.com' target='_blank'>这是一个动态变化的超链接！</a>"
        + "</div>"
    )
    if type == 1:
        #  todo 提取文本
        return "输出返回结果：提取文本成功/失败", html
    elif type == 2:
        #  todo 提取图片
        return "输出返回结果：提取图片成功/失败", html
    else:
        #  todo 提取文本+图片
        return "输出返回结果：提取文本+图片成功/失败", html


def ext_check(file_name):
    file_extension = file_name.split(".")[-1]
    return file_extension in ext_allowd


demo = gr.Interface(
    fn=file,
    inputs=[
        gr.Files(show_label=True, label="请选择文件(仅支持doc/docx/pdf格式，允许多选)", file_types=["file", ".doc", ".docs", ".pdf"]),
        gr.Radio([("文本", 1), ("图片", 2), ("文本+图片", 3)], value=1, label="提取内容"),
        gr.HTML('<a href="https://www.baidu.com">这是一个HTML超链接！</a>'),
        gr.Button(link='https://www.baidu.com', value="这是一个Button超链接！")
    ],
    outputs=["text", "html"],
    title="知识抽取"
)

demo.launch()
