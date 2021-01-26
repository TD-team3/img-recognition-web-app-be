from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from registration_app.models import Users
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

                # checking if email already exists in database
                check_mail = Users.objects.filter(mail=mail)
                # if the email filter leads to some remanasult, then user already exists in database
                if check_mail.count() != 0:
                    return HttpResponse('email already registered.', status=405)

                user = Users(
                    mail=mail,
                    name=name,
                    surname=surname,
                    password=password
                )
                user.save()
                return HttpResponse('Account created!', status=200)

                # check if can use method User.objects.create_user(mail, ....)

    return HttpResponseBadRequest()








