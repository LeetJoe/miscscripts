
import json
import numpy
import math


# split instructions into fixed numbers

num = 128
lang = "ch"

# save the batch to file
def save_file(rank_num, dict_small):
    # print("./instinwild_" + lang + "_" + str(num) + "_" + rank_num + ".json")
    # print(len(dict_small))
    with open("./instinwild_" + lang + "_" + str(num) + "_" + rank_num + ".json", "w", encoding='utf-8') as dump_f:
        json.dump(dict_small, dump_f, ensure_ascii=False, indent=4, separators=(',', ':'))


with open("./instinwild_" + lang + ".json", "r") as f:
    load_dict = json.load(f)
    appendix_lenth = math.ceil(numpy.log10(len(load_dict)/num))
    rank = 0
    load_dict_small = []
    for item in load_dict:
        load_dict_small.append(item)
        if len(load_dict_small) >= num:
            save_file(str(rank).zfill(appendix_lenth), load_dict_small)
            load_dict_small = []
            rank += 1
    if len(load_dict_small) > 0:
        save_file(str(rank).zfill(appendix_lenth), load_dict_small)

print("done.")

