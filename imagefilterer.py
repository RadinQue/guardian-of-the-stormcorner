from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from wand.color import Color
import wand
import wand.drawing
from os import path
import os


class ImageFilterer:

    def clean_all_temp_files(self):
        possible_temp_files = ["img.png", "img.jpg",
                               "img2.png", "img2.jpg", "img3.png", "img3.jpg"]
        for file in possible_temp_files:
            if path.exists(file):
                os.remove(file)

    def apply_contrast(self, contrast_amount, img):
        return ImageEnhance.Contrast(img).enhance(contrast_amount)

    def apply_emboss(self, emboss_amount, img):
        i = 0
        while i < emboss_amount:
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            i += 1
        return img

    def apply_magik(self, scale, img):
        img.save('./img.png')
        i = wand.image.Image(filename="./img.png")
        i.format = 'jpg'
        i.background_color = Color("white")
        i.transform(resize='800x800>')
        """ so far these are notsobot's parameters, but would be useful to let the user pass more commands to it through the bot """
        i.liquid_rescale(width=int(i.width * 0.5), height=int(i.height * 0.5),
                         delta_x=int(0.5 * scale) if scale else 1, rigidity=0)
        i.liquid_rescale(width=int(i.width * 1.5), height=int(i.height *
                         1.5), delta_x=scale if scale else 2, rigidity=0)
        i.save(filename="./img.png")
        return i

    """ these two do work but not always TODO: fix this"""

    def apply_haah(self, img):
        img.save('./img2.png')

        i = wand.image.Image(filename="./img2.png")
        i.format = 'jpg'
        i.background_color = Color("white")
        i.transform(resize='800x800')

        """ not having a proper copy of i is quite nasty, better solution needed """
        i2 = wand.image.Image(filename="./img2.png")
        i2.format = 'jpg'
        i2.background_color = Color("white")
        i2.transform(resize='800x800')

        i.flop()
        i2.crop(0, 0, width=400, height=800)
        i.composite(i2, left=0, top=0)
        i.save(filename="./img.png")
        return i

    def apply_waaw(self, img):
        img.save('./img2.png')

        i = wand.image.Image(filename="./img2.png")
        i.format = 'jpg'
        i.background_color = Color("white")
        i.transform(resize='800x800')

        """ not having a proper copy of i is quite nasty, better solution needed """
        # i2 = i
        i2 = wand.image.Image(filename="./img2.png")
        i2.format = 'jpg'
        i2.background_color = Color("white")
        i2.transform(resize='800x800')

        i2.flop()
        i2.crop(0, 0, width=400, height=800)
        i.composite(i2, left=0, top=0)
        i.save(filename="./img.png")
        return i
