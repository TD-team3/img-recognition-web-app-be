import os
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50
import numpy as np


class ImgRecognition:
    model = ResNet50(weights='imagenet')

    def __init__(self):
        pass

    # Recognize image function
    # @param img_file -> img file to recognize
    # @return -> string img prediction
    def recognize_image(self, img_file):

        try:
            # get file path
            path = os.path.abspath(img_file.name)

            # Loading the Image for Prediction
            original_img = image.load_img(path, target_size=(224, 224))
            numpy_image = image.img_to_array(original_img)
            image_batch = np.expand_dims(numpy_image, axis=0)

            # process image
            processed_image = preprocess_input(image_batch)
            preds = self.model.predict(processed_image)
            pred_class = decode_predictions(preds, top=1)

            prediction_str = pred_class[0][0][1].replace("_", " ")
            return prediction_str

        except Exception as ex:
            # if there is any error, raise a ValueError
            raise ValueError(ex.args)



