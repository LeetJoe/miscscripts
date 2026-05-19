import torch
import transformers


def load_map():
    entity_map = {}
    relation_map = {}

    origin_entity_map_file = '/home/songchao/work/code/tLogicNet/data/icews14/entitymap.txt'
    origin_relation_map_file = '/home/songchao/work/code/tLogicNet/data/icews14/relationmap.txt'

    with open(origin_entity_map_file, 'r') as f:
        for line in f:
            entity_id, entity_name = line.strip().split('\t')
            entity_map[entity_id] = entity_name
        f.close()

    with open(origin_relation_map_file, 'r') as f:
        for line in f:
            relation_id, relation_name = line.strip().split('\t')
            relation_map[relation_id] = relation_name
        f.close()
    
    print(f"origin map loaded! 实体数量: {len(entity_map)}, 关系数量: {len(relation_map)}")

    return entity_map, relation_map


def save_new_map(new_entity_map, new_relation_map):
    new_entity_map_file = '/home/songchao/work/code/tLogicNet/data/icews14/new_entitymap.txt'
    new_relation_map_file = '/home/songchao/work/code/tLogicNet/data/icews14/new_relationmap.txt'

    with open(new_entity_map_file, 'w') as f:
        for entity_id, new_entity_id in new_entity_map.items():
            f.write(f"{entity_id}\t{new_entity_id}\n")
        f.close()

    with open(new_relation_map_file, 'w') as f:
        for relation_id, new_relation_id in new_relation_map.items():
            f.write(f"{relation_id}\t{new_relation_id}\n")
        f.close()


def encode_id(text, tokenizer, word_embeddings):
    inputs = tokenizer(text, return_tensors="pt")
    # print("分词结果 ID：", inputs["input_ids"])
    # print("还原后的文本：", tokenizer.decode(inputs["input_ids"][0]))

    with torch.no_grad():
        # embeddings = model.model.language_model.embed_tokens(inputs["input_ids"])
        outputs = model(**inputs, output_hidden_states=True)
        hidden_states = outputs.hidden_states[-1].squeeze(0)

    # print(embeddings)
    sentence_vector = hidden_states.mean(dim=0)
    # print(f"合并后的句子向量形状: {sentence_vector.shape}")  # 2560
    similarities = torch.matmul(word_embeddings, sentence_vector)
    closest_word_id = torch.argmax(similarities).item()
    # closest_word = tokenizer.decode([closest_word_id])
    # print(f"最相似的词: {closest_word}")

    return closest_word_id



if __name__ == "__main__":
    local_model_path = '/mnt/data/songchao/hfmodels/gemma4/gemma-4-e4b-it'

    tokenizer = transformers.AutoTokenizer.from_pretrained(
        local_model_path, 
        trust_remote_code=True
    )
    model = transformers.AutoModelForCausalLM.from_pretrained(
        local_model_path,
        device_map="auto",
        dtype=torch.bfloat16 
    )
    # model = model.to("cuda:0")
    
    word_embeddings = model.model.language_model.embed_tokens.weight
    print("本地 Model 加载成功！")

    entity_map, relation_map = load_map()

    new_entity_map = {}
    new_relation_map = {}

    for entity_id, entity_name in entity_map.items():
        new_entity_id = encode_id(entity_name, tokenizer, word_embeddings)
        new_entity_map[entity_id] = new_entity_id
    
    print("实体编码完成！")
    
    for relation_id, relation_name in relation_map.items():
        new_relation_id = encode_id(relation_name, tokenizer, word_embeddings)
        new_relation_map[relation_id] = new_relation_id
    
    print("关系编码完成！")
    
    save_new_map(new_entity_map, new_relation_map)
