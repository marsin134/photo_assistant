from PIL import Image, ImageFilter
import types
from data.python.correct_image import correct_size

im = Image.open('static/image/example_effects/example_effect.png')


# im.filter(ImageFilter.CONTOUR).save('static/image/6.png') # на создание наброска
# im.filter(ImageFilter.FIND_EDGES).show()
# im.filter(ImageFilter.SMOOTH).save('smooth.png')
# im.filter(ImageFilter.GaussianBlur(5)).save('static/image/blur.png')
# im.filter(ImageFilter.MinFilter(5)).save('static/image/pixel.png')
# im.filter(ImageFilter.Kernel((3, 3),
#        (-1, -1, -1, -1, 9, -1, -1, -1, -1), 1, 0)).save('static/image/sharpness.png')
# im2 = im.quantize(16)
# im2.save('static/image/quantization.bmp')
def quantization_effect(im):
    im = im.quantize(16)
    return im


s = quantization_effect
print(isinstance(ImageFilter.SMOOTH, types.FunctionType))
# rew(im.size, im).save('static/image/example_effects/black_white.png')
