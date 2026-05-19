############################################################################
# A simple demo for async http request.
# 1. simple producer with no daemon;
# 2. one consumer with no conflicts;
# 3. worker result transmitted using queue, not gather().
############################################################################

import os
import json
import argparse
import asyncio
import aiohttp

from utils import load_map, evaluate_avg


entity_map={}
relation_map={}
time_map={}
ollama_gateway = 'http://localhost:11434/api/generate'
ollama_model = 'gemma4:31b'

prompt_base = """
### Role
You are an international event predictor, and you are good at predicting the missing element of an event described like {{subject, predicate, ?, time}} or {{?, predicate, object, time}}.

"""

prompt_content = """
### Query
{}

### Candidates list 1:
{}

### Candidates list 2:
{}

### Output:
"""


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Re-evaluate rank using LLM',
        usage='python llm_reeval.py [<args>] [-h | --help]'
    )

    parser.add_argument('--data_path', '-d', type=str, help='path to data')
    parser.add_argument('--exp_folder', '-e', type=str, help='folder of the experiment')
    parser.add_argument('--iter', '-i', type=int, help='iteration number of the experiment')
    parser.add_argument('--rank_thresh', '-r', type=int, default=10, help='rank threshold to re-evaluate')

    return parser.parse_args(args)



def load_complete(pred_path):
    result = {}
    rerank_file = os.path.join(pred_path, 'reranks.txt')
    if os.path.exists(rerank_file) and os.path.getsize(pred_path) > 10:
        with open(rerank_file, 'r') as fr:
            _ = fr.readline()
            for line in fr:
                split = line.strip().split('\t')
                query = split[0].split(',')
                query.append(split[1])
                result[tuple(query)] = 1
            fr.close()
    else:
        with open(rerank_file, 'w') as fw_rank:
            fw_rank.write('query\tdirection\tkge_rank\tllm_rank\n')
            fw_rank.close()

    return result


def get_query_list(pred_path: str, rank_threshold: int = 3):
    kge_pred_file = os.path.join(pred_path, 'kge/pred_kge.txt')
    mln_pred_file = os.path.join(pred_path, 'mln/pred_test.txt')

    # list of {'query': [s, p, o, t, task, old rank], 'target': 'target name', 'content': 'prompt content'}
    query_list = []
    finished_list = load_complete(str(pred_path))
    with open(kge_pred_file, 'r') as fr_kge:
        with open(mln_pred_file, 'r') as fr_mln:
            while True:
                kge_fact = fr_kge.readline()
                kge_candidates = fr_kge.readline()
                mln_fact = fr_mln.readline()
                mln_candidates = fr_mln.readline()
                if ((not kge_fact) and (not kge_candidates)) or ((not mln_fact) and (not mln_candidates)):
                    break
                kge_fact = kge_fact.strip().split('\t')
                if int(kge_fact[5]) <= rank_threshold:
                    continue

                kge_candidates = kge_candidates.strip().split(';')
                kge_candidates = {item.split('*')[0]: item.split('*')[1] for item in kge_candidates}
                mln_fact = mln_fact.strip().split('\t')
                mln_candidates = json.loads(mln_candidates)

                # assert (len(kge_fact) > 0 and len(mln_fact) > 0 and int(kge_fact[0]) == int(mln_fact[0]) and int(
                #     kge_fact[1]) == int(mln_fact[1]) and int(kge_fact[2]) == int(mln_fact[2]) and int(kge_fact[3]) == int(
                #     mln_fact[3]) and kge_fact[4] == mln_fact[4])

                if tuple(kge_fact[:5]) in finished_list:
                    continue

                name_fact = [entity_map[kge_fact[0]], relation_map[kge_fact[1]], entity_map[kge_fact[2]],
                             time_map[kge_fact[3]]]

                if kge_fact[4] == 'sp':
                    target = name_fact[2]
                    name_fact[2] = '?'
                else:
                    target = name_fact[0]
                    name_fact[0] = '?'

                new_kge_candidates = {}
                i = 0
                stop_num = int(kge_fact[5]) + 10
                for cand, score in kge_candidates.items():
                    new_kge_candidates[entity_map[cand]] = round(float(score), 6)
                    i += 1
                    if i >= stop_num:
                        break

                new_mln_candidates = {}
                stop_num = 10
                findit = False
                for cand, score in mln_candidates.items():
                    new_mln_candidates[entity_map[cand]] = round(float(score), 6)
                    if entity_map[cand] == target:
                        findit = True
                    if findit:
                        stop_num -= 1
                    if stop_num < 0:
                        break

                query_list.append({
                    'fact': kge_fact,
                    'target': target,
                    'content': prompt_content.format(name_fact, new_mln_candidates, new_kge_candidates)
                })
            fr_mln.close()
        fr_kge.close()

    return query_list


def reeval(pred_path):
    rank_file = os.path.join(pred_path, 'ranks.txt')
    rerank_file = os.path.join(pred_path, 'reranks.txt')
    rank_dict = {}
    with open(rank_file, 'r') as fr_rank:
        _ = fr_rank.readline()
        for line in fr_rank:
            split = line.strip().split('\t')
            query = split[0].split(',')
            query.append(split[1])
            rank_dict[tuple(query)] = int(split[2])
        fr_rank.close()

    with open(rerank_file, 'r') as fr_rank:
        _ = fr_rank.readline()
        for line in fr_rank:
            split = line.strip().split('\t')
            query = split[0].split(',')
            query.append(split[1])
            rank_dict[tuple(query)] = int(split[3])
        fr_rank.close()

    result = evaluate_avg(rank_dict)

    result_file = os.path.join(pred_path, 'result_llm.txt')
    with open(result_file, 'w') as fw:
        fw.write('kge+mln+llm:\nMR: {}, MRR: {}, Hit@1: {}, Hit@3: {}, Hit@10: {}\n\n'.format(*result.values()))
        fw.close()


def clear_llm_output(out_str):
    if out_str[:8] == '```json\n':
        out_str = out_str[8:]
    if out_str[-4:] == '\n```':
        out_str = out_str[:-4]
    if out_str[:1] == '[':
        out_str = out_str[1:]
    if out_str[-1:] == ']':
        out_str = out_str[:-1]

    return out_str


async def worker(worker_id: int, in_queue: asyncio.Queue, out_queue: asyncio.Queue, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    while True:
        try:
            query = await in_queue.get()
            data = {
                'model': ollama_model,
                'stream': False,
                'prompt': query['content']
            }
            print('Worker: {}, request start: {}'.format(worker_id, query['fact']))
            async with semaphore:
                async with session.post(ollama_gateway, json=data, timeout=3000) as response:
                    response_dict = await response.json()

                    if response.status != 200:
                        result = '[ERROR] Response staus: {}, text: {}.'.format(response.status, response_dict)
                    else:
                        try:
                            output_str = response_dict['response']
                            output_str = clear_llm_output(output_str)
                            result_dict = json.loads(output_str)
                            if query['target'] not in result_dict:
                                result = '[ERROR] Target {} not exists: {}.'.format(query['target'], output_str)
                            else:
                                result = result_dict[query['target']]
                        except e:
                            result = '[ERROR] Exception: {}, output: {}'.format(e, output_str)

                    print('Worker: {}, request end: {}, rank: {}'.format(worker_id, query['fact'], result))

                    if isinstance(result, int):
                        await out_queue.put('{},{},{},{}\t{}\t{}\t{}\n'.format(
                            *query['fact'][:4], query['fact'][4], query['fact'][5], result
                        ))

        except Exception as e:
            print('[ERROR] Worker: {}, request end: {}, exception: {}'.format(worker_id, query['fact'], e))
        finally:
            in_queue.task_done()


async def producer(queue: asyncio.Queue, query: dict):
    query['content'] = prompt_base.format(query['target']) + query['content']
    await queue.put(query)


async def consumer(kge_path:str, queue: asyncio.Queue):
    print("[INFO] Consumer started.")
    rerank_file = os.path.join(kge_path, 'reranks.txt')

    while True:
        try:
            result = await queue.get()
            if len(result) != 0:
                with open(rerank_file, 'w') as fw:
                    fw.write(result)
                    fw.flush()
                    fw.close()
        except Exception as e:
            print("[ERROR] Consumer exception: {}.".format(e))
        finally:
            queue.task_done()


async def aio_task(query_list: list, kge_path: str):
    in_queue = asyncio.Queue(maxsize=5)
    out_queue = asyncio.Queue(maxsize=5)
    max_concurrent_requests = 3
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    timeout = aiohttp.ClientTimeout(total=15)
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        workers = [asyncio.create_task(worker(i, in_queue, out_queue, session, semaphore)) for i in range(max_concurrent_requests)]
        consumer_task = asyncio.create_task(consumer(kge_path, out_queue))

        for query in query_list:
            producer_task = asyncio.create_task(producer(in_queue, query))
        await producer_task
        await in_queue.join()
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
        await out_queue.join()
        consumer_task.cancel()


if __name__ == '__main__':
    # print(prompt_base.format('Beijing'))

    args = parse_args()
    kge_path = os.path.join(args.data_path, args.exp_folder, str(args.iter))
    entity_map, relation_map, time_map = load_map(args.data_path)
    query_list = get_query_list(str(kge_path), args.rank_thresh)

    print('LLM re-rank start, amount: {}'.format(len(query_list)))

    asyncio.run(aio_task(query_list, str(kge_path)))
    # parse_task(str(kge_path), query_list)
    reeval(kge_path)

    print('LLM re-rank finished.')
