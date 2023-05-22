
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers import Conv1D
from keras.layers import MaxPooling1D

# Word Embedding Model + Convolutional Model + Fully connected Model
# define problem
vocab_size = 100
max_length = 200

# define model
model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=max_length))
model.add(Conv1D(32, 8, activation='relu'))
model.add(MaxPooling1D(2))
model.add(Flatten())
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# TODO: 一个model里面加这么多模型做什么？Sequential，是指定义一个model序列用于处理输入？
model.summary()

