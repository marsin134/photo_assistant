import os
from . import works
from flask import request
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
from flask_login import current_user
from .correct_image import allowed_file, original_name, correct_size


def make_sketch(input_path, output_path):
    """Создание шаблона"""
    input = Image.open(input_path)
    image = correct_size(input)
    output = image.filter(ImageFilter.CONTOUR)
    output.save(output_path)


def create_sketch(upload_folder):
    """Возвращает обработанное изображение пользователя"""
    upload_folder += '/sketch_im'

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = original_name(filename)

        file.save(os.path.join(upload_folder, filename))
        im = Image.open(os.path.join(upload_folder, filename))
        if im.load()[0, 0] != 0:   # проверка на корректность полученного файла
            # меняем размер изображения
            original_im = correct_size(Image.open(os.path.join(upload_folder, filename)))

            original_im.save(os.path.join(upload_folder, filename))
            rembg_img_name = filename.split('.')[0] + "_rembg.png"

            # обрабатываем фото
            make_sketch(upload_folder + '/' + filename, upload_folder + '/' + rembg_img_name)

            works.add_works(current_user.get_id(), 'delete_fons', upload_folder + '/' + rembg_img_name)
            return upload_folder + '/' + filename, upload_folder + '/' + rembg_img_name
        return None, None
    return None, None
