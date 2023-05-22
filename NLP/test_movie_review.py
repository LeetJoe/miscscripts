# TODO: 这只是个半成品，只做到把文章分成字行，没有做 word embedding 或者 doc encoding。


from os import listdir
from collections import Counter
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense
import string
from numpy import array


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


# convert the docs into lines and save them into file
def save_lines_to_file(is_train=False):
    # load vocabulary
    vocab_filename = 'vocab.txt'
    vocab = load_doc(vocab_filename)
    vocab = vocab.split()
    vocab = set(vocab)

    # prepare negative reviews
    negative_lines = docs_to_lines('txt_sentoken/neg', vocab, is_train)
    if not is_train:
        neg_filename = 'negative_sample.txt'
        pos_filename = 'positive_sample.txt'
    else:
        neg_filename = 'negative.txt'
        pos_filename = 'positive.txt'
    save_list(negative_lines, neg_filename)
    # prepare positive reviews
    positive_lines = docs_to_lines('txt_sentoken/pos', vocab, is_train)
    save_list(positive_lines, pos_filename)


positive_lines = load_doc('positive.txt').split('\n')
negative_lines = load_doc('negative.txt').split('\n')
docs = positive_lines + negative_lines

tokenizer = Tokenizer()
# fit the tokenizer on the documents
tokenizer.fit_on_texts(docs)

# encode training data set
Xtrain = tokenizer.texts_to_matrix(docs, mode='freq')  # shape (1800, 13045)


# load all test reviews
positive_lines = load_doc('positive_sample.txt').split('\n')
negative_lines = load_doc('negative_sample.txt').split('\n')
docs = negative_lines + positive_lines

# encode test data set
Xtest = tokenizer.texts_to_matrix(docs, mode='freq')  # shape (200, 13045)

ytrain = array([0 for _ in range(900)] + [1 for _ in range(900)])
ytest = array([0 for _ in range(100)] + [1 for _ in range(100)])



n_words = Xtest.shape[1]  # doc的向量表示的长度，也即vocab的大小。

# define network
model = Sequential()
# 添加『一个』hidden layer，里面有『50个』神经元neurons，激活函数使用relu。
model.add(Dense(50, input_shape=(n_words,), activation='relu'))
# 添加一个『output layer』，里面有『1个』神经元neurons，激活函数使用sigmoid。
model.add(Dense(1, activation='sigmoid'))

# compile network. 使用二分交叉熵损失函数，与二分判定配套使用。
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit network，开始训练了。输入有两个数据集，一个是matrix格式的训练集，一个与训练集对应的list格式的0/1答案。
model.fit(Xtrain, ytrain, epochs=50, verbose=2)

# evaluate，也是有两个数据集，一个是matrix格式的测试集，一个是与测试集对应的list格式的0/1答案。
loss, acc = model.evaluate(Xtest, ytest, verbose=0)
print(loss)
print(acc)
print('Test Accuracy: %f' % (acc*100))  # 与之前的图片分类类似，对结果准确性进行打分。

# TODO: 结果acc太低了，只有9%，即正确率只有9%，肯定是哪里有问题。

