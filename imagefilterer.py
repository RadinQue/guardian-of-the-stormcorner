from PIL import Image, ImageEnhance, ImageFilter

class ImageFilterer:
	
    def apply_contrast(self, contrast_amount, img):
   	return ImageEnhance.Contrast(img).enhance(contrast_amount)

    def saturate(self, saturation_amount, img):
        return ImageEnhance.Color(img).enhance(saturation_amount)

    def apply_emboss(self, emboss_amount, img):
        i = 0
        while i < emboss_amount:
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            i += 1
        return img
