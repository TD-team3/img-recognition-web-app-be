from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import json
from authentication_app.base_auth_classes.authentication import auth
from .base_upload_classes.recognition_handler import ImgRecognitionHandler


def upload(request):
    if request.method == 'POST':
        # getting the json data from the http POST request made by front-end
        json_str = request.POST.get('data', '')  # FIRST PARAMETER MAY CHANGE !!!
        if json_str:
            # converting the json data into a json object
            json_obj = json.loads(json_str)
            if 'username' in json_obj and 'token' in json_obj:
                username = json_obj['username']
                token = json_obj['token']
                if auth.is_token_valid(username, token):
                    image_recognizer = ImgRecognitionHandler()
                    # ADD TRY EXCEPT TO SEE IF PASSED FILES RESPECT SIZE AND FORMAT !!!

                    # SECOND PARAMETER MAY CHANGE !!!
                    json_file_str = image_recognizer.process_images(request.FILES, 'photos')

                    return HttpResponse(json_file_str, status=200)
                else:
                    return HttpResponseForbidden("Session expired or user is not logged!")

    return HttpResponseBadRequest("Bad request")

# note that 'myfile' is the name= attribute of the form/input TAG in the HTML, and may change