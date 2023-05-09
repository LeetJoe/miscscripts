from nltk.tokenize import word_tokenize

# load data
filename = './pg1513.txt'
file = open(filename, 'rt')
text = file.read()
file.close()
# split into words
words = word_tokenize(text)
# words = text.split()

# remove punctuation from each word
import string

table = str.maketrans('', '', string.punctuation)

# convert to lower case
words = [word.lower() for word in words]

# remove all tokens that are not alphabetic
words = [word for word in words if word.isalpha()]
words = [w.translate(table) for w in words]

# filter out stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]

# stemming of words
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()
stemmed = [porter.stem(word) for word in words]

print(words[:100])

