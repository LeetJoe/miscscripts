## LLaMA2Cypher

### 环境配置与运行

```
conda install python=3.10.11
git clone git@github.com:huggingface/transformers.git
cd transformers
pip install .
cd <PATH_TO_LLaMA2Cypher>
pip install -r requirements.txt

# web mode default on http://127.0.0.1:7860
python demo_web.py --checkpoint /home/neo/work/data/cnllama2

# interactive mode in terminal
python demo_cmd.py --checkpoint /home/neo/work/data/cnllama2
```

### 使用的 LLM 

主要使用 [LLaMA2-7B-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf) 进行实验。

用于对比实验的 LLM

* [Chinese-LlaMA2-chat-7B-sft-v0.3](https://huggingface.co/michaelwzhu/Chinese-LlaMA2-chat-7B-sft-v0.3)（[github](https://github.com/michael-wzhu/Chinese-LlaMA2)）；

* [lawyer-llama-13b-beta1.0](https://huggingface.co/pkupie/lawyer-llama-13b-beta1.0)（[github](https://github.com/AndrewZhe/lawyer-llama)）；

* [replicate LLaMA2-70B](https://replicate.com/)；

* [ngql-gpt](https://ngql-gpt.siwei.io/)（[github](https://github.com/wey-gu/NebulaGraph-GPT)）；


todo: 


> 注：gnql-gpt 的执行效果非常好，但是对中文进行转换时，长语句会出现截断的情况，导致生成的结果不全。
> LLaMA2-70B 对于复杂的问题还是会输出很多非 Cypher 的内容，需要进一步构建 prompt 里的知识来排除这些内容。（可以就使用这些结果，最终的目标是评测 LLaMA-7B，对它优化 prompt 即可。）


1. 对所有的结果进行评估，制作表格，按照 完全正确或接近完全正确 - A，能理解到基本意图但是不准确，但是结果仍具参考价值 - B，对意图的理解错误或非 Cypher 格式等，结果几乎不可用 - C；
2. 对 LLaMA-7B 英文执行效果做重点分析，其它只要执行一遍，对比说明下即可。录制视频（查一下用什么录屏工具）。
3. 完成 LaTeX 文档草稿的编写，等阳智整理完后，再完善注释、引用等内容。让阳智做 PPT。


### 关于数据


数据基于 Neo4j 官方给出的在线 demo 图数据库 [Movie Graph](https://demo.neo4jlabs.com:7473)，用户名：recommendations，密码：recommendations，数据库：recommendations。

简易 schema 如下图：

![schema](img/schema.png)

其中 Movie 表示电影，Director 是导演，Actor 是演员，Person 是 Director 与 Actor 的并集，且 Director 与 Actor 存在交集。

*data/cypher.txt* 文件中的 12 个问题也取自 Neo4j 关于 Movie Graph 的官方教程中的示例，通过在上述在线交互界面中输入`:play movie-graph
`即可看到。

由于数据为教程中为展示数据库特性而设置的，其优点是从简单到复杂的语句都有，缺点是对于太复杂的语句，用自然语言都不太方便描述。在进行 NL2Cypher 的任务中，要把这些复杂的 Cypher 语句用自然语言表述出来都不太容易，可见对于专业性比较强的问题，还是适合使用更加严谨的结构化表达。NL2Cypher 更适合处理一些语义明确并且直接的自然语言。对于复杂的问题，即使可以用自然语言表述，其输出结果也很难控制——实际上，这些描述复杂问题的自然语言，即使是交给一个没有受过专业训练的人类去理解，都未必准确，更别说 LLM 了。

不过，这也并非意味着 LLM 完全无法解决此类问题。对于那些复杂的问题，实际上可以拆分成一些简单的步骤，各个步骤之间的约束，以及最终结果的表达，由人工进行整理。虽然对用户来说，这样做似乎复杂了一些，但是也不失为一种解决问题的方法。

对数据文件的说明如下：
* data/cypher.txt 原始 Cypher 语句；
* data/expert_cn.txt 以对 Cypher 语言有一定了解的专业人员的思维，用中文表达的问题；
* data/expert_en.txt 以对 Cypher 语言有一定了解的专业人员的思维，用英文表达的问题；
* data/user_cn.txt 以普通用户的思维，用中文表达的问题；
* data/user_en.txt 以普通用户的思维，用英文表达的问题；
* data/result_xxx.txt 各类数据相应的处理结果记录。

