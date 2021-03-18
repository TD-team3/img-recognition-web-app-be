from typing import Optional

from search_history_app.models import History
from datetime import date
import json


class SearchHelper:
    # return number of user searches
    @staticmethod
    def count_user_searches(mail):
        return History.objects.filter(mail=mail).count()

    @staticmethod
    def get_user_searches(mail, search_from: Optional[date] = None, search_to: Optional[date] = None) -> str:
        result_list = []

        if search_from is not None and search_to is not None:
            # get only searches in a range of date
            searches = History.objects.filter(mail=mail, datetime__range=(search_from, search_to))
        elif search_from is not None:
            # get only searches in a single date
            searches = History.objects.filter(mail=mail, datetime__date=search_from)
        else:
            # get all searches
            searches = History.objects.filter(mail=mail)

        # generate json file
        for search in searches:
            result_list.append({"id": search.id, "date_time": str(search.datetime),
                                "rcg_output": search.rcg_output, "mail": search.mail_id})

        result_json = json.dumps({'items_count': len(searches), "searches": result_list})

        return result_json


