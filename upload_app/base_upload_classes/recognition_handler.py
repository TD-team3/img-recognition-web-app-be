from django.core.files.temp import NamedTemporaryFile
from .recognition_image import ImgRecognition


class ImgRecognitionHandler:

    allowed_formats = ['.jpg', '.jpeg', '.png']

    def __init__(self):
        # output dictionary
        self.recognition_output = {}

    def process_images(self, sent_files, name_of_container):
        # sent_files is a request.FILES dictionary
        # name_of_container is the name='...' attribute of the HTML form/input tag

        image_recognizer = ImgRecognition()

        for file in sent_files.getlist(name_of_container):
            # ADD CHECK FORMAT AND SIZE OF IMAGE
            if file.name[-4:].lower() not in ImgRecognitionHandler.allowed_formats and \
                    file.name[-3:].lower() not in ImgRecognitionHandler.allowed_formats:
                raise TypeError('format of the image is not valid')

            img_temp = NamedTemporaryFile()

            img_temp.write(file.read())
            img_temp.flush()

            # add recognition result to a list
            self.recognition_output[file.name] = image_recognizer.recognize_image(img_temp)

        # Create JSON FILE
        json_file_str = "{"
        for key, value in self.recognition_output.items():
            json_file_str += '"' + key + '":"' + value + '",'

        # remove last comma
        json_file_str = json_file_str[:-1]
        json_file_str += "}"

        return json_file_str


"""
useful prints:
# print(img_temp.name)
# print(img_temp.tell())
"""
