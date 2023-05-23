from os import listdir

from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense

from numpy import array
from collections import Counter

import string

# load doc into memory
def load_doc(filename):
    # open the file as read only
    with open(filename, 'r') as file:
        # read all text
        text = file.read()
        # close the file
        file.close()
        return text


# turn a doc into clean tokens
def clean_doc(doc):
    # split into tokens by white space
    tokens = doc.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # filter out short tokens
    tokens = [word for word in tokens if len(word) > 1]
    return tokens


# load doc, clean and return line of tokens
def doc_to_line(filename, vocab):
    # load the doc
    doc = load_doc(filename)
    # clean doc
    tokens = clean_doc(doc)
    # filter by vocab
    tokens = [w for w in tokens if w in vocab]
    return ' '.join(tokens)


# load docs in dir and convert them into space separated lines
def docs_to_lines(directory, vocab, is_train=False):
    lines = list()
    # walk through all files in the folder
    for filename in listdir(directory):
        # skip any reviews in the test set, 非训练模式只取cv9开头的100个文件，训练模式使用其它900个文件。
        if is_train and filename.startswith('cv9'):
            continue
        if not is_train and not filename.startswith('cv9'):
            continue
        # skip files that do not have the right extension
        if not filename.endswith(".txt"):
            continue
        # create the full path of the file to open
        path = directory + '/' + filename
        # load and clean the doc
        line = doc_to_line(path, vocab)
        # add to list
        lines.append(line)
    return lines


# load doc and add to vocab
def add_doc_to_vocab(filename, vocab):
    # load doc
    doc = load_doc(filename)
    # clean doc
    tokens = clean_doc(doc)
    # update counts
    vocab.update(tokens)


# load all docs in a directory
def docs_to_vocab(directory, vocab):
    # walk through all files in the folder
    for filename in listdir(directory):
        # skip files that do not have the right extension
        if not filename.endswith(".txt"):
            continue

        # create the full path of the file to open
        path = directory + '/' + filename
        # add doc to vocab
        add_doc_to_vocab(path, vocab)


def save_list(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()


# init the vocab and save it into file
def init_vocab():
    # define vocab
    vocab = Counter()
    # add all docs to vocab
    docs_to_vocab('txt_sentoken/neg', vocab)
    docs_to_vocab('txt_sentoken/pos', vocab)

    # keep tokens with > 5 occurrence
    min_occurane = 6  # 台式机只能搞定到6（内存占用61%），到5就不行了。
    tokens = [k for k,c in vocab.items() if c >= min_occurane]
    # print(len(tokens))

    # save tokens to a vocabulary file
    save_list(tokens, 'vocab.txt')


def load_vocab():
    # load vocabulary
    vocab_filename = 'vocab.txt'
    vocab = load_doc(vocab_filename)
    vocab = vocab.split()
    return set(vocab)


# convert the docs into lines and save them into file
def save_lines_to_file(is_train=False):
    vocab = load_vocab()

    # prepare negative reviews
    if not is_train:
        neg_filename = 'negative_sample.txt'
        pos_filename = 'positive_sample.txt'
    else:
        neg_filename = 'negative.txt'
        pos_filename = 'positive.txt'
    negative_lines = docs_to_lines('txt_sentoken/neg', vocab, is_train)
    save_list(negative_lines, neg_filename)
    # prepare positive reviews
    positive_lines = docs_to_lines('txt_sentoken/pos', vocab, is_train)
    save_list(positive_lines, pos_filename)


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


