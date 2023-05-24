
import json

from numpy import array
from numpy import asarray
from numpy import zeros

from movie_review_vocab import load_doc, init_vocab, save_clean_lines_to_file, save_lines_to_file

from gensim.models import Word2Vec
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

dim = 300

def prepare_sequence():
    # load all training reviews
    positive_lines = load_doc('positive.txt').split('\n')
    negative_lines = load_doc('negative.txt').split('\n')
    train_docs = negative_lines + positive_lines

    # load all test reviews
    positive_lines = load_doc('positive_sample.txt').split('\n')
    negative_lines = load_doc('negative_sample.txt').split('\n')
    test_docs = negative_lines + positive_lines

    # create the tokenizer
    tokenizer = Tokenizer()
    # fit the tokenizer on the documents
    tokenizer.fit_on_texts(train_docs)

    # sequence encode
    encoded_docs = tokenizer.texts_to_sequences(train_docs)
    # pad sequences
    max_length = max([len(s.split()) for s in train_docs])
    Xtrain = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
    # define training labels
    ytrain = array([0 for _ in range(int(Xtrain.shape[0]/2))] + [1 for _ in range(int(Xtrain.shape[0]/2))])

    # sequence encode
    encoded_docs = tokenizer.texts_to_sequences(test_docs)
    # pad sequences
    Xtest = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
    # define test labels
    ytest = array([0 for _ in range(int(Xtest.shape[0]/2))] + [1 for _ in range(int(Xtest.shape[0]/2))])

    # define vocabulary size (largest integer value)
    vocab_size = len(tokenizer.word_index) + 1

    return tokenizer, Xtrain, ytrain, Xtest, ytest, max_length, vocab_size


# 使用Embedding layer + Conv1D layer + MaxPooling1D layer + Flatten layer + Dense + Dense 的模型
def train_a_model(tokenizer, Xtrain, ytrain, max_length, vocab_size):
    # load embedding from file
    # raw_embedding = load_embedding('embedding_word2vec.txt')

    # 使用 glove_6B/glove.6B.100d.txt 结果正确率在75%左右，略有提升; 使用 300B 结果高于80%一点，比100B略好。
    # glove_6B里的100d, 300d表示vector dimension，选用不同的dimension要相应的调整一些代码参数，如Embedding()函数的第二个参数等。
    raw_embedding = load_embedding('glove_6B/glove.6B.300d.txt')
    # get vectors in the right order
    embedding_vectors = get_weight_matrix(raw_embedding, tokenizer.word_index)
    # create the embedding layer, if trainable is true, the result may be a little better.
    embedding_layer = Embedding(vocab_size, dim, weights=[embedding_vectors], input_length=max_length, trainable=True)

    # define model
    model = Sequential()
    model.add(embedding_layer)   # 使用自己生成的word embeddings进行训练得到的结果非常差，经常正确率都不到60%。
    # model.add(Embedding(vocab_size, 100, input_length=max_length))   # 与上面相比，这种简单的layer准确率有接近90%。
    model.add(Conv1D(filters=128, kernel_size=8, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    # print(model.summary())

    # compile network
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    model.fit(Xtrain, ytrain, epochs=10, verbose=2)

    return model


def save_word2wec_embedding(filename):
    # load training data
    positive_docs = json.load(open('w2v_positive.txt'))
    negative_docs = json.load(open('w2v_negative.txt'))
    train_docs = negative_docs + positive_docs

    # train Word2Vec model
    model = Word2Vec(train_docs, vector_size=100, window=5, workers=8, min_count=1)

    # summarize vocabulary size in model
    words = list(model.wv.key_to_index)
    print('Vocabulary size: %d' % len(words))

    # save model in ASCII (Word2Vec) format
    model.wv.save_word2vec_format(filename, binary=False)


# load embedding as a dict
def load_embedding(filename):
    # load embedding into memory, skip first line
    file = open(filename,'r')
    # lines = file.readlines()[1:]   # 自己训练的word embedding使用这句
    lines = file.readlines()   # 使用glove embedding使用这句
    file.close()
    # create a map of words to vectors
    embedding = dict()
    for line in lines:
        parts = line.split()
        # key is string word, value is numpy array for vector
        embedding[parts[0]] = asarray(parts[1:], dtype='float32')
    return embedding


# create a weight matrix for the Embedding layer from a loaded embedding
def get_weight_matrix(embedding, vocab):
    # total vocabulary size plus 0 for unknown words
    vocab_size = len(vocab) + 1
    # define weight matrix dimensions with all 0, 第二个参数数字是 vector_size，选用不同的word embedding要修改此值。
    weight_matrix = zeros((vocab_size, dim))
    # step vocab, store vectors using the Tokenizer's integer mapping
    for word, i in vocab.items():
        vector = embedding.get(word)
        # 这里对word进行判断，如果选择的embedding中没有word，将其加入到weight_matrix会严重影响准确度。使用其它来源的embedding
        # 的话，要进行这一步判断。
        if vector is not None:
            weight_matrix[i] = vector
    return weight_matrix


embedding_filename = 'embedding_word2vec.txt'

# init_vocab()
# save_lines_to_file(True)
# save_lines_to_file(False)
# ave_clean_lines_to_file(True)    # 生成 word embedding 生成所需要的输入文件
# save_word2wec_embedding(embedding_filename)


tokenizer, Xtrain, ytrain, Xtest, ytest, max_length, vocab_size = prepare_sequence()
model = train_a_model(tokenizer, Xtrain, ytrain, max_length, vocab_size)

# evaluate
loss, acc = model.evaluate(Xtest, ytest, verbose=0)
print('Test Accuracy: %f' % (acc*100))


