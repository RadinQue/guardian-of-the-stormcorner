from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from wand.color import Color
import wand, wand.drawing

class ImageFilterer:

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
        i.liquid_rescale(width=int(i.width * 0.5), height=int(i.height * 0.5), delta_x=int(0.5 * scale) if scale else 1, rigidity=0)
        i.liquid_rescale(width=int(i.width * 1.5), height=int(i.height * 1.5), delta_x=scale if scale else 2, rigidity=0)
        i.save(filename="./img.png")
        return i
