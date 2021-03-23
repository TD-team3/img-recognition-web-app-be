from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from authentication_app.base_auth_classes.authentication import TokenJwt
from datetime import datetime
from user_manager import UsersManager
from search_history_app.base_search_history_classes.history_manager import HistoryManager
import json


def get_user_history_searches(request):
    if request.method == 'POST':

        # getting the json data from the http POST request made by front-end
        json_str = request.POST.get('data', '')

        if json_str:
            # converting the json data into a json object
            json_obj = json.loads(json_str)

            # check if the request contain authentication data
            if 'token' in json_obj and 'username' in json_obj:
                token = json_obj['token']
                username = json_obj['username']

                search_from = None
                search_to = None

                if not UsersManager.is_user_in_db(username):
                    return HttpResponseForbidden("Username not found!")

                # check if there are optional parameters in the request
                try:
                    if 'searchFrom' in json_obj:
                        search_from = datetime.strptime(json_obj['searchFrom'], "%d/%m/%Y")

                    if 'searchTo' in json_obj:
                        search_to = datetime.strptime(json_obj['searchTo'], "%d/%m/%Y")

                except Exception as ex:
                    return HttpResponseBadRequest(str(ex.args) + "  Date must be formatted like: 01/01/1990")

                # check Token
                is_token_valid, message = TokenJwt.is_token_valid(username, token)
                if not is_token_valid:
                    return HttpResponseForbidden(message)

                json_result = HistoryManager.get_user_searches(username, search_from, search_to)

                return HttpResponse(json_result)

            else:
                return HttpResponseBadRequest('no token')
        else:
            return HttpResponseBadRequest('no data parameter')

    # generic error or the request isn't 'POST' type
    return HttpResponseBadRequest()
