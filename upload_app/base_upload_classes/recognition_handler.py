from django.core.files.temp import NamedTemporaryFile
from .recognition_image import ImgRecognition

# This class in an Handler for do the image recognition


class ImgRecognitionHandler:

    def __init__(self):
        # output dictionary, key is file name, value is the recognized value
        self.recognition_output = {}

        # create a new instance of ImgRecognition class, this is used for do the img recognition
        self.image_recognizer = ImgRecognition()

    # This is an handler for process images
    # @param "sent_files" is a request.FILES dictionary from http request
    # @param "name_of_container" is the http request image data argument
    #
    # @return -> Json data
    def process_images(self, sent_files, name_of_container):
        #
        # name_of_container is the name='...' attribute of the HTML form/input tag
        files = [sent_files.get('photos[%d]' % i)for i in range(0, len(sent_files))]

        # iterate every file
        for file in files:

            # check image format using endswith with a tuple of possible extensions
            if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise TypeError('Format of the image is not valid')

            # store the image in a NamedTemporaryFile
            img_temp = NamedTemporaryFile()
            img_temp.write(file.read())
            img_temp.flush()

            # check image dimension, files cannot be larger than 10mb
            print(img_temp.tell())
            if img_temp.tell() > 10000000:
                raise TypeError('Image file is too big')

            # recognize image and add recognition result to a list
            self.recognition_output[file.name] = self.image_recognizer.recognize_image(img_temp)

        # Create JSON FILE
        json_file_str = "{"
        for key, value in self.recognition_output.items():
            json_file_str += '"' + key + '":"' + value + '",'

        # remove last comma
        json_file_str = json_file_str[:-1]
        json_file_str += "}"

        # return formatted JSON file
        return json_file_str


"""
useful prints:
# print(img_temp.name) # file path
# print(img_temp.tell()) # dimension
"""
