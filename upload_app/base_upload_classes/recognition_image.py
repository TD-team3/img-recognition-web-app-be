from imageai.Prediction import ImagePrediction


class ImgRecognition:
    MODEL_PATH = "/home/imgrecognitionteam3/img-recognition-dataset/resnet50_model.h5"
    #MODEL_PATH = "D:/Programmazione/Python/img_recognition_test/resnet.h5"

    def __init__(self):
        self.prediction = ImagePrediction()

        # set model type as ResNet
        self.prediction.setModelTypeAsResNet()
        self.prediction.setModelPath(self.MODEL_PATH)
        self.prediction.loadModel()

    # Recognize image function
    # @param img_file -> img file to recognize
    # @return -> string img prediction
    def recognize_image(self, img_file):
        try:
            prediction = self.prediction.predictImage(img_file.name, result_count=1)
            prediction_str = prediction[0][0]

            # remove "_" from result string
            prediction_str = prediction_str.replace("_", " ")
            return prediction_str

        except Exception as ex:
            # if there is any error, raise a ValueError
            raise ValueError(ex.args)


