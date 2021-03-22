from PIL import Image
import os


class ImageStore:

    @staticmethod
    def resize_and_save(img_container, folder_path):
        files = [img_container.get('photos[%d]' % i) for i in range(0, len(img_container))]
        for file in files:
            image = Image.open(file)
            image = image.resize((128, 128), Image.ANTIALIAS)
            image.save(os.path.join(folder_path, file.name))

