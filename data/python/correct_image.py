from string import ascii_letters
from random import sample
import os

MAX_SIZE = 500
CHARACTER_LENGTH = 10

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

an_interesting_variable = 'rYEwfd_secr1Y_izqfjc_et_key942Mnoq'


def correct_size(im):
    """Корректирует размер изображения"""
    if im.size[0] > MAX_SIZE or im.size[1] > MAX_SIZE:
        ratio = MAX_SIZE / max(list(im.size))
        im = im.resize((round(im.size[0] * ratio), round(im.size[1] * ratio)))
    return im


def original_name(filename):
    """Создание оригинального имени"""
    new_filename = filename.split('.')[0] + ''.join(sample(list(ascii_letters), CHARACTER_LENGTH)) + '.png'
    while True:
        if new_filename not in [f for f in os.listdir('static/image') if
                                os.path.isfile(os.path.join('static/image', f))]:
            break
        new_filename = filename.split('.')[0] + ''.join(sample(list(ascii_letters), CHARACTER_LENGTH)) + '.png'
    return new_filename


def allowed_file(filename):
    """Проверяет разрешение файла"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
