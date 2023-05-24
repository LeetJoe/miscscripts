

from movie_review_vocab import load_doc, init_vocab, save_lines_to_file

from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

from numpy import array

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
def train_a_model(Xtrain, ytrain, max_length, vocab_size):
    # define model
    model = Sequential()
    model.add(Embedding(vocab_size, 100, input_length=max_length))
    model.add(Conv1D(filters=32, kernel_size=8, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # print(model.summary())
    # compile network
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    model.fit(Xtrain, ytrain, epochs=10, verbose=2)

    return model


def multi_train_and_test():
    tokenizer, Xtrain, ytrain, Xtest, ytest, max_length, vocab_size = prepare_sequence()

    n_repeats = 8
    total_acc = 0
    for i in range(n_repeats):
        model = train_a_model(Xtrain, ytrain, max_length, vocab_size)

        # evaluate
        loss, acc = model.evaluate(Xtest, ytest, verbose=0)
        total_acc += acc
        print('Test Accuracy of turn %s/%d: %f' % (str(i+1).zfill(2), n_repeats, acc*100))

    print('Average accuracy is: %f' % (total_acc / n_repeats * 100))


# init_vocab()
# save_lines_to_file(True)
# save_lines_to_file(False)

multi_train_and_test()

