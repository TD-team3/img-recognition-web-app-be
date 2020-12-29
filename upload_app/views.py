from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import json
from authentication_app.base_auth_classes.authentication import auth
from .base_upload_classes.upload import ImageUploader
from .base_upload_classes.recognition import ImageRecognizer


def upload(request):
    # getting the json data from the http POST request made by front-end
    json_str = request.POST.get('data', '')  # FIRST PARAMETER MAY CHANGE !!!
    if json_str:
        # converting the json data into a json object
        json_obj = json.loads(json_str)
        if 'username' in json_obj and 'token' in json_obj:
            username = json_obj['username']
            token = json_obj['token']
            if request.method == 'POST' and auth.is_token_valid(username, token):
                my_image_uploader = ImageUploader()
                my_image_uploader.process_images(request.FILES, 'myfile')  # SECOND PARAMETER MAY CHANGE !!!
                my_image_recognizer = ImageRecognizer()
                my_image_recognizer.recognize_images(my_image_uploader)

                final_result = my_image_recognizer.recognition_dictionary
                # WRITE JSON BASED ON FINAL RESULT !!!

                return HttpResponse('PUT JSON HERE', status=200)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

# note that 'myfile' is the name= attribute of the form/input TAG in the HTML, and may change