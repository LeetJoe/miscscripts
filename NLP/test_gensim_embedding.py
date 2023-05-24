
from sklearn.decomposition import PCA
from matplotlib import pyplot
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.scripts.glove2word2vec import glove2word2vec


# load pretrained model
def load_google_pretrain_and_test():
    filename = 'GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)

    # calculate: (king - man) + woman = ?
    result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(result)

def load_stanford_glove_and_test():
    glove_input_file = 'glove_6B/glove.6B.100d.txt'
    word2vec_output_file = 'glove_6B/glove.6B.100d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)
    model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
    # calculate: (king - man) + woman = ?
    result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    print(result)



# define training data
sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
['this', 'is', 'the', 'second', 'sentence'],
['yet', 'another', 'sentence'],
['one', 'more', 'sentence'],
['and', 'the', 'final', 'sentence'],
# test_tokenize.stemmed
]


# train model
model = Word2Vec(sentences, min_count=1)

# summarize vocabulary
words = list(model.wv.key_to_index)
# print(len(words))
# print(words)

# access vector for one word, instead of model['sentence'] in old version
# print(model.wv.get_vector('sentence'))
# save model
model.save('model.bin')
# load model
new_model = Word2Vec.load('model.bin')

# summarize the loaded model
# print(model)

X = [model.wv[word] for i, word in enumerate(words)]

# apply the dimensionality reduction on X
# 对X进行降维处理。原模型大小是wordcount x 100，降维后变成wordcount x 2。
pca = PCA(n_components=2)
result = pca.fit_transform(X)   # shape of [wordcount, 2]

# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()   # 需要图形化界面支持，纯命令行环境无法展示窗口和图表。


# access vector for one word
# print(model.wv.get_vector('sentence'))
'''
print(model.wv.distance('start', 'begin'))     # 0.7847503423690796
print(model.wv.distance('romeo', 'juliet'))    # 0.11974340677261353
print(model.wv.distance('light', 'dark'))      # 0.7120851576328278
print(model.wv.distance('like', 'love'))       # 0.2088145613670349
print(model.wv.distance('book', 'ebook'))      # 1.1772918701171875
print(model.wv.distance('see', 'know'))        # 0.4938245415687561
'''
