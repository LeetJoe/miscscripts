import gradio as gr
import numpy as np

def greet(name, intensity):
    return "Hello " * int(intensity) + name + "!"


def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img


def file(file):
    print(file)
    return ''

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
    inputs=["file"],
    outputs=["text"]
)

demo.launch()
