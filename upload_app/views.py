from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
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

                    if 'photos' in request.FILES:
                        try:
                            json_file_str = image_recognizer.process_images(request.FILES, 'photos')
                        except TypeError:
                            return HttpResponseNotAllowed('error: format must be either jpg or png')

                        return HttpResponse(json_file_str, status=200)  # recognitions are sent here

                else:
                    return HttpResponseForbidden("Session expired or user not logged in!")

    return HttpResponseBadRequest("Bad request")

# note that 'photos' will have to be the name= attribute of the form/input TAG in the HTML
