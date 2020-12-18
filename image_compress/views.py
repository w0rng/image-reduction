from .neural_network.tmp import get_encoder_decoder_predict
from . import models
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
import io
import urllib, base64
from random import randint

encoder, decoder, predict = get_encoder_decoder_predict()


def get_image(request, id_image):
    image = models.Image.objects.filter(id=id_image).first()
    code = np.array(image.data.array)
    x = decoder.predict(code[None])[0]

    plt.axis('off') 

    x = x.astype(int)
    plt.imshow(x)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    args = {'image':uri, 'author': str(image.user), 'object': str(image.obj)}

    return render(request, 'test.html', args)


def get_random_image(request):
    max_ = int(request.GET['max'])
    min_ = int(request.GET['min'])

    code = [randint(min_, max_) for _ in range(500)]
    code = np.array(code)
    x = decoder.predict(code[None])[0]

    plt.axis('off') 

    x = x.astype(int)
    plt.imshow(x)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    args = {'image': uri, 'author': 'Random', 'object': 'Random'}

    return render(request, 'test.html', args)