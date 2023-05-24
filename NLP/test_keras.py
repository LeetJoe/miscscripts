from keras.preprocessing.text import hashing_trick
from keras.preprocessing.text import one_hot
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import one_hot
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten

from numpy import array
from numpy import asarray
from numpy import zeros


# load data
filename = './pg1513.txt'    # 电子书《罗密欧与朱丽叶》
file = open(filename, 'rt')
text = file.read()
file.close()

# 使用Keras的text_to_word_sequence可以一次性完成split+filter+lowercase
result = text_to_word_sequence(text)
# print(result[:20])

words = set(result)    # 即集合
vocab_size = len(words)
# print(vocab_size)   # = 4282

# integer encode the document, Keras里也有现成的one_hot方法
# round(vocab_size*1.3) = 5576, result的实际长度为 29352，是对整个text进行编码，这个数字大约是文章的单词数量。
# result = one_hot(text, round(vocab_size*1.3))

# print(len(set(result)))    # = 2984  ？？ 怎么与vocab_size差别这么大？ 不应该是一词一个integer吗？

# 像刚才这样的编码必然会要求使用的时候要同时记录vocab和它们对应的编码。如果使用一种hash函数建立word到int的关系，就不需要再维持一个
# 单词表了，需要的时候直接hash即可。

# integer encode the document
result = hashing_trick(text, round(vocab_size*1.3), hash_function='md5')
# print(len(set(result)))  # = 3032，与前面的one_hot结果差不太多，多几十个。？？？为啥。

# define 5 documents
docs = ['Well done!',
 'Good work',
 'Great effort',
 'nice work',
 'Excellent!',
#  text
        ]
# create the tokenizer
t = Tokenizer()
# fit the tokenizer on the documents
t.fit_on_texts(docs)

# summarize what was learned
# print(t.word_counts)       # 所有单词计数
# print(t.document_count)     # 总文档数，即docs的长度
# print(t.word_index)         # 单词下标
# print(t.word_docs)          # 单词在多少个文档中出现过

# integer encode documents
# texts_to_matrix 用于对『doc』（注意不是word）进行编码，文档编码长度与vocab长度相同。 doc embedding??
encoded_docs = t.texts_to_matrix(docs, mode='count')
# print(encoded_docs)

from keras.layers import Embedding

# 200 是单词表长度，32是向量维度，50是输入句子的长度。
e = Embedding(200, 32, input_length=50)

# define documents
docs = ['Well done!',
 'Good work',
 'Great effort',
 'nice work',
 'Excellent!',
 'Weak',
 'Poor effort!',
 'not good',
 'poor work',
 'Could have done better.']

# define class labels 积极或消极
labels = array([1,1,1,1,1,0,0,0,0,0])

# integer encode the documents
vocab_size = 50
encoded_docs = [one_hot(d, vocab_size) for d in docs]
# print(encoded_docs)

# pad documents to a max length of 4 words
# 上面的encoded_docs最长是4，把所有doc的编码对齐到4，不足4位的后面补0
max_length = 4
padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
# print(padded_docs)


# load the whole embedding into memory
use_GloVe = True

if use_GloVe:   # 如何使用 Pre-Trained GloVe Embedding
    embeddings_index = dict()

    # 数据去GloVe（Global Vector）https://github.com/stanfordnlp/GloVe 项目里找。
    f = open('glove_6B/glove.6B.100d.txt')
    for line in f:
     values = line.split()
     word = values[0]
     coefs = asarray(values[1:], dtype='float32')
     embeddings_index[word] = coefs
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))
    # create a weight matrix for words in training docs
    embedding_matrix = zeros((vocab_size, 100))
    for word, i in t.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    e = Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=4, trainable=False)
else:
    e = Embedding(vocab_size, 8, input_length=max_length)


# define model， Sequential是一个模型的名字，或者说类型？ColossalAI里也有这个关键字。
model = Sequential()
model.add(e)
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# summarize the model
print(model.summary())

# fit the model
model.fit(padded_docs, labels, epochs=50, verbose=0)

# evaluate the model
loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
print('Accuracy: %f' % (accuracy*100))


