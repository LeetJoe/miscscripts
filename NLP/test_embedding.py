from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

import test_tokenize

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

# summarize the loaded model
# print(model)

# summarize vocabulary
words = list(model.wv.key_to_index)
# print(len(words))
# print(words)

X = [model.wv[word] for i, word in enumerate(words)]

# apply the dimensionality reduction on X
# 对X进行降维处理。原模型大小是wordcount x 100，降维后变成wordcount x 2。
pca = PCA(n_components=2)
result = pca.fit_transform(X)   # shape of [wordcount, 2]

# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()


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
