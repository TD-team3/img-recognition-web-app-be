from user_manager import UsersManager
from django.http import HttpResponse, HttpResponseForbidden
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


def logout(request):
    json_str = request.POST.get('data', '')
    if json_str:
        json_obj = json.loads(json_str)
        # check if the request contain authentication data
        if 'username' in json_obj and 'token' in json_obj:
            username = json_obj['username'].lower()
            token = json_obj['token']

            if not UsersManager.is_user_in_db(username):
                return HttpResponseForbidden("Username not found!")

            try:
                UsersManager.delete_token(username, token)
                return HttpResponse('ok', status=200)
            except ValueError:
                return HttpResponseForbidden('an error occurred: username and token are not associated')

    return HttpResponse('bad request', status=400)






