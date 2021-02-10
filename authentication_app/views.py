from authentication_app.base_auth_classes.authentication import auth
from django.http import HttpResponse
import json
import jwt


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
                payload = auth.generate_token_payload(username)
                # the payload will be encoded and added as a key
                jwt_token = {'token': jwt.encode(payload, "SECRET_KEY", algorithm="HS256")}
                encoded_token_str = json.dumps(jwt_token)

                # saving token for later check
                auth.save_token(username, encoded_token_str)

                return HttpResponse(encoded_token_str, status=200, content_type='application/json')
            else:
                return HttpResponse('authentication not valid', status=401)

    return HttpResponse('bad request', status=400)




