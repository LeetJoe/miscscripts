
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding


# define problem
vocab_size = 100

max_length = 32

# define the model
model = Sequential()
model.add(Embedding(vocab_size, 8, input_length=max_length))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# summarize the model
# TODO: 验证LLaMA的model也有这个summary()方法吗？
model.summary()

# TODO: 文档里说，可以通过其它pre-trained weights来初始化Embedding Layer。是否意味着llama model里的weight实际上
#  就是Embedding Layer？
