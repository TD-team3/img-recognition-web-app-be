from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import json
from .base_upload_classes.recognition_handler import ImgRecognitionHandler
from user_manager import UsersManager
from authentication_app.base_auth_classes.authentication import TokenJwt


def upload(request):
    if request.method == 'POST':
        # getting the json data from the http POST request made by front-end
        json_str = request.POST.get('data', '')

        if json_str:
            # converting the json data into a json object
            json_obj = json.loads(json_str)

            # check if the request contain authentication data
            if 'username' in json_obj and 'token' in json_obj:
                username = json_obj['username'].lower()
                token = json_obj['token']

            if not UsersManager.is_user_in_db(username):
                return HttpResponseForbidden("Username not found!")

            # validate token
            is_token_valid, message = TokenJwt.is_token_valid(username, token)
            if is_token_valid:
                image_recognizer = ImgRecognitionHandler()

                # check if there is the 'photos' argument in request arguments
                if 'photos[0]' in request.FILES:
                    list_of_photos = request.FILES.getlist('photos')
                    if len(list_of_photos) > 10:
                        return HttpResponseBadRequest('a maximum of 10 images is allowed for recognition.')
                    try:
                        json_file_str = image_recognizer.process_images(request.FILES, 'photos')
                    except Exception as ex:
                        return HttpResponse(ex.args, status=405)

                    # If all is ok, send the recognition json
                    return HttpResponse(json_file_str, status=200)

            else:
                # token not valid! Error may be due to 1) session expired or 2) not corresponding or empty token
                return HttpResponseForbidden(message)

    # request argument not valid!
    return HttpResponseBadRequest("Bad request")


# upload test function is only for test, there is no authentication check!
def upload_test(request):
    if request.method == 'POST':
        # getting the json data from the http POST request made by front-end
        json_str = request.POST.get('data', '')

        if json_str:
            # converting the json data into a json object
            json_obj = json.loads(json_str)

            image_recognizer = ImgRecognitionHandler()

            # check if there is the 'photos' argument in request arguments
            if 'photos[0]' in request.FILES:
                list_of_photos = request.FILES.getlist('photos')
                if len(list_of_photos) > 10:
                    return HttpResponseBadRequest('a maximum of 10 images is allowed for recognition.')
                try:
                    json_file_str = image_recognizer.process_images(request.FILES, 'photos')
                except Exception as ex:
                    return HttpResponse(ex.args, status=405)

                # If all is ok, send the recognition json
                return HttpResponse(json_file_str, status=200)

    # request argument not valid!
    return HttpResponseBadRequest("Bad request")

# note that 'photos' will have to be the name= attribute of the form/input TAG in the HTML
