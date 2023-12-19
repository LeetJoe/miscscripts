import gradio as gr
import os
import torch
import threading
import argparse
import warnings

from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer, GenerationConfig
from config import LLM_ego


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


if __name__ == "__main__":
    warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--datapath", type=str, default="data")
    parser.add_argument("--load_in_8bit", action="store_true")
    args = parser.parse_args()
    checkpoint = args.checkpoint
    data_path = args.datapath

    print("Loading model...")
    tokenizer = LlamaTokenizer.from_pretrained(checkpoint)
    generation_config = GenerationConfig.from_pretrained(checkpoint)
    if args.load_in_8bit:
        model = LlamaForCausalLM.from_pretrained(checkpoint, device_map="auto", load_in_8bit=True)
    else:
        model = LlamaForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.float16)
    print("Model loaded.")

    with open(os.path.join(data_path, 'schema.txt'), 'r') as fs:
        cypher_schema = fs.read() + "\n"

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        input_msg = gr.Textbox(label="Input")
        with gr.Row():
            lang_dropdown = gr.Dropdown(['en', 'cn'], label="Language", elem_id='language')
            generate_button = gr.Button('Generate', elem_id='generate', variant='primary')
            clear_button = gr.Button('Clear', elem_id='clear', variant='secondary')

        def lang(selected_option):
            return selected_option

        def user(user_message, lang):
            user_message = user_message.strip()
            if len(lang) == 0:
                lang = 'en'

            return user_message, lang
        
        def bot(user_message, lang):
            print(user_message)
            print(lang)

            # extract user inputs from chat history and retrieve law articles
            current_user_input = user_message

            if len(current_user_input) == 0:
                return

            # 构造输入
            input_text = LLM_ego['en'] + "\n### Schema: " + cypher_schema + "### User: " + current_user_input + "\n### Cypher: "

            print("=== Input ===")
            print("input_text: ", input_text)

            inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
            streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

            # Run the generation in a separate thread, so that we can fetch the generated text in a non-blocking way.
            generation_kwargs = dict(inputs, generation_config=generation_config, streamer=streamer, max_new_tokens=400, do_sample=False, repetition_penalty=1.1)
            thread = StoppableThread(target=model.generate, kwargs=generation_kwargs)
            thread.start()

            # 开始流式生成
            output = ""
            for new_text in streamer:
                output += new_text
                yield output

            streamer.end()
            thread.stop()
            print("Output: ", output)

        def stop(invitation_code):
            global stop_everything
            stop_everything[invitation_code] = True

        input_msg.submit(user, [input_msg, lang_dropdown], [input_msg, lang_dropdown], queue=False).then(
            bot, [input_msg, lang_dropdown], chatbot
        )
        generate_button.click(user, [input_msg, lang_dropdown], [input_msg, lang_dropdown], queue=False).then(
            bot, [input_msg, lang_dropdown], chatbot
        )

    demo.queue()
    demo.launch(share=False, server_port=args.port, server_name='127.0.0.1')

