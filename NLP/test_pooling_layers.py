# example of vertical line detection with a convolutional layer
from numpy import asarray
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import MaxPooling2D
from keras.layers import GlobalMaxPooling2D


# define input data
data = [[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0],
		[0, 0, 0, 1, 1, 0, 0, 0]]
data = asarray(data)
data = data.reshape(1, 8, 8, 1)

# create model
model = Sequential()
# 添加一个2D卷积模型
model.add(Conv2D(1, (3,3), activation='relu', input_shape=(8, 8, 1)))
# 添加一个average pooling 2D layer
# model.add(AveragePooling2D())
# 添加一个max pooling 2D layer
# model.add(MaxPooling2D())
# 添加一个global pooling 2D layer
model.add(GlobalMaxPooling2D())

# summarize model
model.summary()

# define a vertical line detector
detector = [[[[0]],[[1]],[[0]]],
            [[[0]],[[1]],[[0]]],
            [[[0]],[[1]],[[0]]]]
weights = [asarray(detector), asarray([0.0])]

# store the weights in the model
model.set_weights(weights)

# apply filter to input data
yhat = model.predict(data)

# enumerate rows
'''
for r in range(yhat.shape[1]):
	# print each column in the row
	print([yhat[0,r,c,0] for c in range(yhat.shape[2])])
'''

print(yhat)
