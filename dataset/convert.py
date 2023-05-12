
import json

# convert jsonl file to json file
file = open("./seed_prompts_en.jsonl")

jsonlist = []
for line in file:
    jsonlist.append(json.loads(line))

with open("./seed_prompts_en.json", "w") as f:
    json.dump(jsonlist, f)

print('done.')