import os
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import request
from .correct_image import correct_size, original_name, allowed_file
from flask_login import current_user
from . import works


def remove_background(input_path, output_path):
    input = Image.open(input_path)
    image = correct_size(input)
    output = remove(image)
    output.save(output_path)


def delete(upload_folder):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

        original_im = correct_size(Image.open(os.path.join(upload_folder, filename)))

        os.remove(os.path.join(upload_folder, filename))

        filename = original_name(filename)

        original_im.save(os.path.join(upload_folder, filename))
        rembg_img_name = filename.split('.')[0] + "_rembg.png"

        remove_background(upload_folder + '/' + filename, upload_folder + '/' + rembg_img_name)

        works.add_works(current_user.get_id(), 'delete_fons', upload_folder + '/' + rembg_img_name)
        return upload_folder + '/' + filename, upload_folder + '/' + rembg_img_name
    return None, None
