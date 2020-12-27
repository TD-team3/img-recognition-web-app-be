from authentication_app.authentication import auth
from django.http import HttpResponse
import json


def login(request):
    # getting the json data from the http POST request made by front-end
    json_str = request.POST.get('data', '')
    if json_str:
        # converting the json data into a json object
        json_obj = json.load(json_str)
        if 'username' in json_obj and 'password' in json_obj:
            username = json_obj['username']
            password = json_obj['password']
            # the following stores a boolean and eventually stores a generated token
            auth_result = auth.is_auth_data_valid(username, password)
            if auth_result:
                json_token = '{"token":"{0}"}'.format(auth.token[username])
                return HttpResponse(json_token, status=200, content_type='application/json')
            else:
                return HttpResponse('authentication not valid', status=401)

    return HttpResponse('bad request', status=400)




