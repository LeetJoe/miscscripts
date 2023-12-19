import os
import time
import replicate

from config import tokens, LLM_ego
from utils import json_send


url = 'https://api.replicate.com/v1/predictions'

if __name__ == "__main__":
    data_path = "data"
    with open(os.path.join(data_path, 'schema.txt'), 'r') as fs:
        cypher_schema = fs.read() + "\n"
    fs.close()

    for lang in ['en', 'cn']:
        result = []
        with open(os.path.join(data_path, 'expert_{}.txt'.format(lang)), 'r') as fr:
            for current_query in fr:
                if len(current_query) == 0:
                    continue

                # 构造输入
                input_text = "### Schema: " + cypher_schema + "### User: " + current_query + "\n### Cypher: "
                # print(input_text)

                headers = {'Authorization': 'Token {}'.format(tokens['replicate'])}
                data = {
                    "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                    'input': {
                        'debug': False,
                        'system_prompt': LLM_ego[lang],
                        'prompt': input_text,
                        'temperature': 0.75,
                        'top_k': 50,
                        'max_new_tokens': 500,
                        'min_new_tokens': -1
                    }
                }

                response = json_send(url, data, extra_headers=headers)
                # print(response)
                if response['status'] == 402:
                    print(response['title'] + "\n" + response['detail'])
                    exit()
                get_url = response['urls']['get']
                k = 30
                done = False
                while k >= 0 and not done:
                    time.sleep(5)
                    k -= 1
                    response = json_send(get_url, extra_headers=headers)
                    if response['status'] == 'succeeded':
                        output = response['output']
                        done = True
                    elif response['status'] == 'failed':
                        k = -1
                    else:
                        k += 1
                        # print(response['status'])

                if not done:
                    print("Failed to get response for {}".format(current_query))
                    exit()

                str_output = ''
                for term in output:
                    str_output += term
                print(str_output)
                result.append("### query:" + current_query + "\n### LLM output:\n" + str_output + "\n\n\n\n")
                time.sleep(2)

        # save to file
        with open(os.path.join(data_path, 'result_llama2_70B_expert_{}.txt'.format(lang)), 'w') as fo:
            for line in result:
                fo.write(line)

        print("Finished")

