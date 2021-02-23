from user_manager import UsersManager
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

            status, desc = UsersManager.login_user(username, password)

            if status:
                return HttpResponse(desc, status=200, content_type='application/json')
            else:
                return HttpResponse(desc, status=401)

    return HttpResponse('bad request', status=400)




