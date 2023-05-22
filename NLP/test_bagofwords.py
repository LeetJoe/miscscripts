from sklearn.feature_extraction.text import TfidfVectorizer
# from keras.preprocessing.text import Tokenizer


# list of text documents
text = ["I love you and you love me.",
        "I love my mom.",
        "I love my work.",
        "My cat love me.",
        "I love my cat."
]

'''
# load data
filename = './pg1513.txt'    # 电子书《罗密欧与朱丽叶》
file = open(filename, 'rt')
text = [file.read(), 'I love you', 'To be or not to be']
file.close()
'''

'''
# ----------------------- 这段使用的是 Keras ----------------------
# create the tokenizer
t = Tokenizer()
# fit the tokenizer on the documents
t.fit_on_texts(text)      # 使用了tensorflow库，执行速度非常快

# summarize what was learned
print(t.word_counts)
# print(t.document_count)     # 文档数量，即text的列表长度
print(t.word_index)     # 后面text_to_matrix的编排字典。

# '<word>' => <countnum>, 这里统计的是每个单词有出现过的文档数量。在同一个文档中出现多次只计一次。
# 代码不变的情况下，重复执行得到的列表顺序不同，但内容是一样的。
print(t.word_docs)

# integer encode documents
# 对文档的编码后，向量里的位置对应于t.word_index，顺序也是以t.word_index 的顺序编排的，与文档原文顺序不一致。
# 比如t.word_index是{'dog': 1, 'cat': 2, 'you': 3, 'phone': 4, 'i': 5, 'wolf': 6, 'love': 7}
# 文档'I love you'的编码类似于：[0, 0, 0, 1, 0, 1, 0, 1, 0, 1]. 其中第0个位置始终是0，第一个位置是文档中dog出现的次数，以此类推。
encoded_docs = t.texts_to_matrix(text, mode='freq')    # mode有binary, count, freq, tfidf等值
print(encoded_docs[0])

'''
# ------------------------- 这段使用的是 sklearn ------------------------
# create the transform
vectorizer = TfidfVectorizer()
# tokenize and build vocab

# 这里注意输入的是一个list，直接输入string会报错
vectorizer.fit(text)

# summarize
# 单词表，encode是按vocabulary_下标定位的，但是它本身没有按下标排序
print(vectorizer.vocabulary_)
print(vectorizer.idf_)
# encode document
vector = vectorizer.transform([text[0]])

# summarize encoded vector
# print(vector.shape)
# 句子中对应vocabulary_下标位置的值非0. (有一句里存在的单词对应位置的值也是0？)
print(vector.toarray())
