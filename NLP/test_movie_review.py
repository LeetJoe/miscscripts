# TODO: 这只是个半成品，只做到把文章分成字行，没有做 word embedding 或者 doc encoding。


from os import listdir
from collections import Counter
from nltk.corpus import stopwords
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
def docs_to_lines(directory, vocab):
    lines = list()
    # walk through all files in the folder
    for filename in listdir(directory):
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
    min_occurane = 2
    tokens = [k for k,c in vocab.items() if c >= min_occurane]
    # print(len(tokens))

    # save tokens to a vocabulary file
    save_list(tokens, 'vocab.txt')


# load vocabulary
vocab_filename = 'vocab.txt'
vocab = load_doc(vocab_filename)
vocab = vocab.split()
vocab = set(vocab)

# prepare negative reviews
negative_lines = docs_to_lines('txt_sentoken/neg', vocab)
save_list(negative_lines, 'negative.txt')
# prepare positive reviews
positive_lines = docs_to_lines('txt_sentoken/pos', vocab)
save_list(positive_lines, 'positive.txt')

