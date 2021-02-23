from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from user_manager import UsersManager
import json


def signup(request):
    if request.method == 'POST':
        json_str = request.POST.get('data', '')
        if json_str:
            json_obj = json.loads(json_str)
            if 'mail' in json_obj and 'name' in json_obj and 'surname' in json_obj and 'password' in json_obj:
                mail = json_obj['mail'].lower()
                name = json_obj['name']
                surname = json_obj['surname']
                password = json_obj['password']

                # ensuring no field is empty
                if not mail or not name or not surname or not password:
                    return HttpResponse('empty fields are not allowed', status=405)

                # create new user
                is_success, desc = UsersManager.add_new_user(mail, name, surname, password)
                if is_success:
                    return HttpResponse('Account created!', status=200)
                else:
                    return HttpResponse(desc, status=405)

    return HttpResponseBadRequest()








