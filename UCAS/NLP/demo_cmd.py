import os
import torch
import argparse
from transformers import LlamaForCausalLM, LlamaTokenizer, GenerationConfig


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--datapath", type=str, default="")

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

    self_recog = ("You are a cypher expert and you can tranform the question of user into cypher format. "
                  "Please use the given schema and complete the transformation. "
                  "Only the cypher sentences should be printed.\n")

    with open(os.path.join(data_path, 'schema.txt'), 'r') as fs:
        cypher_schema = fs.read() + "\n"

    while True:
        current_user_input = input("[Human] >>> ")
        current_user_input = current_user_input.strip()
        if len(current_user_input) == 0:
            continue

        # 构造输入
        input_text = self_recog + "### Schema: " + cypher_schema + "### User: " + current_user_input + "\n### Cypher: "
        # print(input_text)

        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        outputs = model.generate(input_ids, generation_config=generation_config, max_new_tokens=400, do_sample=False, repetition_penalty=1.1)
        output_text = str(tokenizer.decode(outputs[0], skip_special_tokens=True))
        # skip prompt
        output_text = output_text[len(input_text):]

        print("[AI] >>> " + output_text)
