from PIL import Image, ImageFilter
from flask import request
from werkzeug.utils import secure_filename
from data.python.correct_image import correct_size, allowed_file, original_name
import types
from . import works
import os
from flask_login import current_user

UPLOAD_FOLDER = 'static/image/example_effects'

effects = [(UPLOAD_FOLDER + '/' + 'sharpness.png', 'sharpness'),
           (UPLOAD_FOLDER + '/' + 'quantization.bmp', 'quantization'),
           (UPLOAD_FOLDER + '/' + 'smooth.png', 'smooth'), (UPLOAD_FOLDER + '/' + 'pixel.png', 'pixel'),
           (UPLOAD_FOLDER + '/' + 'blur.png', 'blur'), (UPLOAD_FOLDER + '/' + 'black_white.png', 'black_white'),
           (UPLOAD_FOLDER + '/' + 'black_find_edges.png', 'black_find_edges'),
           (UPLOAD_FOLDER + '/' + 'negative.png', 'negative'),
           (UPLOAD_FOLDER + '/' + 'ping+.png', 'ping+'), (UPLOAD_FOLDER + '/' + 'violet+.png', 'violet+'),
           (UPLOAD_FOLDER + '/' + 'blue+.png', 'blue+'), (UPLOAD_FOLDER + '/' + 'green+.png', 'green+')]


def black_white(size, image):
    x, y = size
    pixels = image.load()
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            bw = (r + g + b) // 3
            pixels[i, j] = bw, bw, bw
    return image


def violet_effect(size, image):
    pixels = image.load()
    x, y = size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = g, b, r
    return image


def ping_effect(size, image):
    pixels = image.load()
    x, y = size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = r, b, g
    return image


def negative(size, image):
    pixels = image.load()
    x, y = size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = 255 - r, 255 - g, 255 - b
    return image


def blue_effect(size, image):
    pixels = image.load()
    x, y = size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = b, g, r
    return image


def green_effect(size, image):
    pixels = image.load()
    x, y = size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = g, r, b
    return image


def quantization_effect(im):
    im = im.quantize(16)
    return im


dict_make_effects = {'sharpness': ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 9, -1, -1, -1, -1), 1, 0),
                     'quantization': quantization_effect, 'pixel': ImageFilter.MinFilter(5),
                     'blur': ImageFilter.GaussianBlur(5),
                     'black_white': black_white, 'smooth': ImageFilter.SMOOTH,
                     'black_find_edges': ImageFilter.FIND_EDGES,
                     'negative': negative, 'ping+': ping_effect, 'violet+': violet_effect, 'blue+': blue_effect,
                     'green+': green_effect}


def make_effect(effect_name, upload_folder):
    if effect_name in dict_make_effects:
        effect_fun = dict_make_effects[effect_name]
        im, filename = apply_the_effect(upload_folder)
        if im:
            new_name = original_name(filename)
            im.save(upload_folder + '/' + new_name)

            if isinstance(effect_fun, types.FunctionType):
                effect_fun(im.size, im).save(upload_folder + '/' + new_name.split('.')[0] + "_effect.png")
                works.add_works(current_user.get_id(), f'effect-{effect_name}',
                                upload_folder + '/' + new_name.split('.')[0] + "_effect.png")
                return upload_folder + '/' + new_name, upload_folder + '/' + new_name.split('.')[0] + '_effect.png'
            im.filter(effect_fun).save(upload_folder + '/' + new_name.split('.')[0] + "_effect.png")
            works.add_works(current_user.get_id(), f'effect-{effect_name}',
                            upload_folder + '/' + new_name.split('.')[0] + "_effect.png")
            return upload_folder + '/' + new_name, upload_folder + '/' + new_name.split('.')[0] + "_effect.png"
        return None
    return None


def apply_the_effect(upload_folder):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        original_im = correct_size(Image.open(os.path.join(upload_folder, filename)))
        os.remove(os.path.join(upload_folder, filename))
        return original_im, filename
    return None