
import string
import json
from collections import Counter
from nltk.corpus import stopwords
from os import listdir

# load doc into memory
def load_doc(filename):
    # open the file as read only
    with open(filename, 'r') as file:
        # read all text
        text = file.read()
        # close the file
        file.close()
        return text


# turn a doc into clean tokens, in order to init the vocab
def clean_doc_for_vocab(doc):
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

# load doc and add to vocab
def add_doc_to_vocab(filename, vocab):
    # load doc
    doc = load_doc(filename)
    # clean doc
    tokens = clean_doc_for_vocab(doc)
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


def save_list_in_lines(lines, filename):
    doc = '\n'.join(lines)
    with open(filename, 'w') as file:
        file.write(doc)
        file.close()

def save_list_in_json(list, filename):
    with open(filename, "w") as file:
        json.dump(list, file)
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
    save_list_in_lines(tokens, 'vocab.txt')


def load_vocab():
    # load vocabulary
    vocab_filename = 'vocab.txt'
    vocab = load_doc(vocab_filename)
    vocab = vocab.split()
    return set(vocab)


# clean doc with vocab and convert doc into string of space separated tokens
def doc_to_line(text, vocab):
    # split into tokens by white space
    tokens = text.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]

    # filter out tokens not in vocab
    tokens = [w for w in tokens if w in vocab]
    tokens = ' '.join(tokens)
    return tokens


# clean doc with vocab and convert doc into string of space separated tokens
def file_to_line(filename, vocab):
    # load the doc
    doc = load_doc(filename)
    return doc_to_line(doc, vocab)

# load docs in dir and convert them into space separated lines
# bag of word 格式的文件处理
def files_to_lines(directory, vocab, is_train=False):
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
        line = file_to_line(path, vocab)
        # add to list
        lines.append(line)
    return lines


# convert the docs into lines and save them into file
# bag of word 格式的文件保存
def save_lines_to_file(is_train=False):
    vocab = load_vocab()

    # prepare negative reviews
    if not is_train:
        neg_filename = 'negative_sample.txt'
        pos_filename = 'positive_sample.txt'
    else:
        neg_filename = 'negative.txt'
        pos_filename = 'positive.txt'
    negative_lines = files_to_lines('txt_sentoken/neg', vocab, is_train)
    save_list_in_lines(negative_lines, neg_filename)
    # prepare positive reviews
    positive_lines = files_to_lines('txt_sentoken/pos', vocab, is_train)
    save_list_in_lines(positive_lines, pos_filename)


# turn a doc into clean tokens
def doc_to_lines(doc, vocab):
    clean_lines = list()
    lines = doc.splitlines()
    for line in lines:
        # split into tokens by white space
        tokens = line.split()
        # remove punctuation from each token
        table = str.maketrans('', '', string.punctuation)
        tokens = [w.translate(table) for w in tokens]
        # filter out tokens not in vocab
        tokens = [w for w in tokens if w in vocab]
        clean_lines.append(tokens)
    return clean_lines


# load docs in dir and convert them into space separated lines
def files_to_clean_lines(directory, vocab, is_train=False):
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
        doc = load_doc(path)
        doc_lines = doc_to_lines(doc, vocab)
        # add to list
        lines += doc_lines
    return lines


# convert the docs into lines and save them into file
# 用于 Word2Vec 的模型
def save_clean_lines_to_file(is_train=False):
    vocab = load_vocab()

    # prepare negative reviews
    if not is_train:
        neg_filename = 'w2v_negative_sample.txt'
        pos_filename = 'w2v_positive_sample.txt'
    else:
        neg_filename = 'w2v_negative.txt'
        pos_filename = 'w2v_positive.txt'
    negative_lines = files_to_clean_lines('txt_sentoken/neg', vocab, is_train)
    save_list_in_json(negative_lines, neg_filename)
    # prepare positive reviews
    positive_lines = files_to_clean_lines('txt_sentoken/pos', vocab, is_train)
    save_list_in_json(positive_lines, pos_filename)


