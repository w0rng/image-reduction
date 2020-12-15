from keras.layers import Dense, Flatten, Reshape, Input, InputLayer, LeakyReLU
from keras.models import Sequential, Model
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Lambda
from keras import backend as K
from keras.datasets import cifar10, cifar100


def custom_function(input):
    '''Кастомная функция активации'''
    input = K.maximum(0.,input)
    input = K.minimum(input, 255)
    return input


def build_encoder(img_shape, code_size):
    '''Создает модель, сворачивающую изображения размера img_shape до code_size'''
    encoder = Sequential()
    encoder.add(InputLayer(img_shape))
    encoder.add(Flatten())
    encoder.add(Dense(code_size))
    encoder.add(LeakyReLU())

    return encoder


def build_decoder(img_shape, code_size):
    '''Разворачивает изображения из размера code_size до img_shape'''
    decoder = Sequential()
    decoder.add(InputLayer((code_size,)))
    decoder.add(Dense(np.prod(img_shape)))
    decoder.add(Lambda(custom_function))
    decoder.add(Reshape(img_shape))

    return decoder


def build_autoencoder(img_shape, code_size):
    encoder = build_encoder(img_shape, code_size)
    decoder = build_decoder(img_shape, code_size)

    inp = Input(x_train_orig.shape[1:])
    code = encoder(inp)
    reconstruction = decoder(code)

    autoencoder = Model(inp,reconstruction)
    autoencoder.compile(optimizer='Adam', loss='mse')

    return encoder, decoder, autoencoder 


(x_train_orig, y_train), (x_test_orig, y_test) = cifar10.load_data()
encoder, decoder, autoencoder = build_autoencoder(x_train_orig.shape[1:], 500)
autoencoder.fit(
    x = x_train_orig, 
    y = x_train_orig, 
    epochs = 20, 
    validation_data = [x_test_orig, x_test_orig]
)


def show_image(x):
    x = x.astype(int)
    plt.imshow(x)


def visualize(img, encoder, decoder):
    code = encoder.predict(img[None])[0]
    reco = decoder.predict(code[None])[0]

    plt.subplot(1,3,1)
    plt.title("Исходное изображение")
    show_image(img)

    plt.subplot(1,3,2)
    plt.title("Код")
    plt.imshow(code.reshape([code.shape[-1]//20,-1]))

    plt.subplot(1,3,3)
    plt.title("Закодированное изображение")
    show_image(reco)
    plt.show()


for i in range(5):
    img = x_test_orig[i]
    visualize(img,encoder,decoder)


'''
Datas
-
id int PK
array list

Images
-
id int PK
name string
data int FK >- Datas.id
date data
size float
object FK >- Objects.id

Objects
-
id int PK
name string

'''