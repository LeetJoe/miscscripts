# from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer

'''
# list of text documents
text = ["The quick brown fox jumped over the lazy dog.",
        "The dog.",
        "The fox"]

'''
# load data
filename = './pg1513.txt'
file = open(filename, 'rt')
text = [file.read(), 'I love you', 'To be or not to be']
file.close()

# '''
# create the tokenizer
t = Tokenizer()
# fit the tokenizer on the documents
t.fit_on_texts(text)      # 使用了tensorflow库，执行速度非常快
# summarize what was learned
# print(t.word_counts)
# print(t.document_count)
# print(t.word_index)
# print(t.word_docs)
# integer encode documents
encoded_docs = t.texts_to_matrix(text, mode='count')
print(encoded_docs[2][:1000])

'''
# create the transform
vectorizer = TfidfVectorizer()
# tokenize and build vocab

vectorizer.fit(text)
# summarize
print(vectorizer.vocabulary_)
print(vectorizer.idf_)
# encode document
vector = vectorizer.transform([text[1]])
# summarize encoded vector
print(vector.shape)
print(vector.toarray())

'''