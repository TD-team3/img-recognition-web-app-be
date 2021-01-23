from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from registration_app.models import Users
import json


def signup(request):
    if request.method == 'POST':
        json_str = request.POST.get('data', '')
        if json_str:
            json_obj = json.loads(json_str)
            if 'mail' in json_obj and 'name' in json_obj and 'surname' in json_obj and 'password' in json_obj and\
                    'password2' in json_obj:
                mail = json_obj['mail'].lower()
                name = json_obj['name']
                surname = json_obj['surname']
                password = json_obj['password']
                password2 = json_obj['password2']

                # checking if email already exists in database
                check_mail = Users.objects.filter(mail=mail)
                # if the email filter leads to some result, then user already exists in database
                if check_mail.count() != 0:
                    res = json.dumps('email already registered.')
                    return HttpResponseNotAllowed(res, content_type='application/json')
                # validating two passwords
                if password != password2:
                    res = json.dumps('passwords do not match.')
                    return HttpResponseNotAllowed(res, content_type='application/json')

                # if no problem is found, a user gets created
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








