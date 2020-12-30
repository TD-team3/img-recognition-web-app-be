from base_upload_classes import ImgRecognition


class ImgRecognitionHandler:

    def __init__(self):
        self.recognition_dictionary = {}

    def store_recognitions(self, img_uploader):  # parameter must be an ImageUploader instance
        for temp_img in img_uploader.uploaded_images:
            image_recognizer = ImgRecognition()
            recognized_image = ImgRecognition.recognize_image(temp_img)
            self.recognition_dictionary[temp_img] = recognized_image
            # the key will be the name of the image and the value will be its recognition
