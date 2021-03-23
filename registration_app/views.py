from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from user_manager import UsersManager
import json
from search_history_app.base_search_history_classes.history_manager import HistoryManager


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
                    # create user folder for search history storage
                    HistoryManager.create_user_folder(user_folder_name=mail,
                                                      parent_folder_name=HistoryManager.FOLDER_NAME)

                    return HttpResponse('Account created!', status=200)
                else:
                    return HttpResponse(desc, status=405)

    return HttpResponseBadRequest()


def send_mail_password(request):
    if request.method == 'POST':
        json_str = request.POST.get('data', '')
        if json_str:
            json_obj = json.loads(json_str)
            if 'mail' in json_obj:
                mail = json_obj['mail'].lower()
                print(mail)
                status, desc = UsersManager.send_password(mail)
                print(status)
                if status:
                    return HttpResponse("ok")
                else:
                    return HttpResponse(desc, status=405)

    return HttpResponseBadRequest("bad request")






