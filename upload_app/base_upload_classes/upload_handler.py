from django.core.files.temp import NamedTemporaryFile


class ImgUploadHandler:

    def __init__(self):
        self.uploaded_images = []

    def process_images(self, sent_files, name_of_container):
        # sent_files is a request.FILES dictionary
        # name_of_container is the name='...' attribute of the HTML form/input tag
        for file in sent_files.getlist(name_of_container):
            # ADD CHECK FORMAT AND SIZE OF IMAGE
            img_temp = NamedTemporaryFile()
            img_temp.write(file.read())
            img_temp.flush()

            self.uploaded_images.append(img_temp)

"""
useful prints:
# print(img_temp.name)
# print(img_temp.tell())
"""
