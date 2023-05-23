
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense

from movie_review_vocab import load_doc, clean_doc, init_vocab, load_vocab

from numpy import array

# parse line arrays of train and test to matrix
def prepare_matrix(mode):
    # load all train reviews
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
    # encode training data set
    Xtrain = tokenizer.texts_to_matrix(train_docs, mode=mode)
    # encode training data set
    Xtest = tokenizer.texts_to_matrix(test_docs, mode=mode)

    ytrain = array([0 for _ in range(int(Xtrain.shape[0]/2))] + [1 for _ in range(int(Xtrain.shape[0]/2))])
    ytest = array([0 for _ in range(int(Xtest.shape[0]/2))] + [1 for _ in range(int(Xtest.shape[0]/2))])

    n_words = Xtrain.shape[1]  # doc的向量表示的长度，也即vocab的大小。
    return tokenizer, Xtrain, Xtest, ytrain, ytest, n_words

def train_a_model(n_words, Xtrain, ytrain):
    # define network
    model = Sequential()
    # 添加『一个』hidden layer，里面有『50个』神经元neurons，激活函数使用relu。
    model.add(Dense(50, input_shape=(n_words,), activation='relu'))
    # 添加一个『output layer』，里面有『1个』神经元neurons，激活函数使用sigmoid。
    model.add(Dense(1, activation='sigmoid'))

    # compile network. 使用二分交叉熵损失函数，与二分判定配套使用。
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit network，开始训练了。输入有两个数据集，一个是matrix格式的训练集，一个与训练集对应的list格式的0/1答案。
    # verbose 指示日志输出的详细程度，取值如0,1,2；越大越详细。
    model.fit(Xtrain, ytrain, epochs=50, verbose=0)

    return model

# train and test. txt files needed as prerequisite
def multi_train_and_test():
    tokenizer, Xtrain, Xtest, ytrain, ytest, n_words = prepare_matrix('freq')

    n_repeats = 30
    total_acc = 0
    for i in range(n_repeats):
        model = train_a_model(n_words, Xtrain, ytrain)

        # evaluate，也是有两个数据集，一个是matrix格式的测试集，一个是与测试集对应的list格式的0/1答案。
        loss, acc = model.evaluate(Xtest, ytest, verbose=0)
        total_acc += acc
        print('Test Accuracy of turn %s/%d: %f' % (str(i+1).zfill(2), n_repeats, acc*100))  # 与之前的图片分类类似，对结果准确性进行打分。binary: 92, freq: 91, count: 88.5, tfidf: 86

    print('Average accuracy is: %f' % (total_acc / n_repeats * 100))


# classify a review as negative (0) or positive (1)
def predict_sentiment(review, vocab, tokenizer, model):
    """
    Args:
        review: doc in string
        vocab: vocab in list
    """
    # clean
    tokens = clean_doc(review)
    # filter by vocab
    tokens = [w for w in tokens if w in vocab]
    # convert to line
    line = ' '.join(tokens)
    # encode
    encoded = tokenizer.texts_to_matrix([line], mode='freq')
    # prediction
    yhat = model.predict(encoded, verbose=0)
    print(yhat)
    return round(yhat[0,0])


tokenizer, Xtrain, Xtest, ytrain, ytest, n_words = prepare_matrix('freq')
model = train_a_model(n_words, Xtrain, ytrain)
vocab = load_vocab()

print(predict_sentiment('This is a very good movie!', vocab, tokenizer, model))

print(predict_sentiment('This is a bad movie.', vocab, tokenizer, model))


