from keras.layers import Dense, Flatten, Reshape, Input, InputLayer, LeakyReLU
from keras.models import Sequential, Model
import numpy as np
from keras.layers import Lambda
from keras import backend as K
from keras.datasets import cifar10
from os import path


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


def get_encoder_decoder_predict():
    if not path.exists('./image_compress/neural_network/models/decoder'):
        (x_train_orig, y_train), (x_test_orig, y_test) = cifar10.load_data()
        encoder, decoder, autoencoder = build_autoencoder(x_train_orig.shape[1:], 500)

        autoencoder.fit(
            x = x_train_orig, 
            y = x_train_orig, 
            epochs = 1, 
            validation_data = [x_test_orig, x_test_orig]
        )
    else:
        from tensorflow import keras
        decoder = keras.models.load_model('./image_compress/neural_network/models/decoder', compile=False)
        encoder = keras.models.load_model('./image_compress/neural_network/models/encoder', compile=False)
    predict = keras.models.load_model('./image_compress/neural_network/models/type_images')

    return encoder, decoder, predict