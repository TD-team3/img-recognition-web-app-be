from authentication_app.base_auth_classes.authentication import auth
from django.http import HttpResponse
import json


def login(request):
    # getting the json data from the http POST request made by front-end
    json_str = request.POST.get('data', '')
    if json_str:
        # converting the json data into a json object
        json_obj = json.loads(json_str)
        if 'username' in json_obj and 'password' in json_obj:
            username = json_obj['username'].lower()
            password = json_obj['password']
            # the following checks if username is present in database and if password is correct
            if auth.is_auth_data_valid(username, password):
                # the following creates a token based on username and current time
                encoded_jwt = auth.generate_and_save_jwt(username)

                return HttpResponse(encoded_jwt, status=200, content_type='application/json')
            else:
                return HttpResponse('authentication not valid', status=401)

    return HttpResponse('bad request', status=400)




