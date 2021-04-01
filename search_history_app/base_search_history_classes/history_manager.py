from server.settings import BASE_DIR
from search_history_app.base_search_history_classes.image_store import ImageStore
from registration_app.models import Users
from datetime import datetime
from typing import Optional
from search_history_app.models import History
from datetime import date
import json
import os


class HistoryManager:

    FOLDER_NAME = 'history_storage'

    @staticmethod
    def create_user_folder(user_folder_name, parent_folder_name):
        user_path = os.path.join(BASE_DIR, parent_folder_name, user_folder_name)
        print(user_path)
        try:
            os.makedirs(user_path)
            # if folder already exists, skip
        except FileExistsError as error:
            print(error)
        return user_path

    @staticmethod
    def create_search_folder(user_path, search_id):
        # creating the sub-folder with the id of the search, starting from the user folder
        search_path = os.path.join(user_path, str(search_id))
        # print(search_path)
        print(search_path)
        os.mkdir(search_path)
        return search_path

    @staticmethod
    def get_user_folder_path(username):
        user_path = os.path.join(BASE_DIR, HistoryManager.FOLDER_NAME, username)
        return user_path

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

    @staticmethod
    def save_search_in_db(search, username):
        user = Users.objects.get(pk=username)
        search_db = History(rcg_output=search, datetime=str(datetime.now())[:-7], mail=user)
        search_db.save()
        return search_db

    @staticmethod
    def store_search(recognitions_as_json, username, images):
        # saving search on database
        search_on_database = HistoryManager.save_search_in_db(recognitions_as_json, username)
        # getting the user folder path
        user_folder_path = HistoryManager.get_user_folder_path(username)
        # creating the search sub-folder path inside user folder
        search_path = HistoryManager.create_search_folder(user_folder_path, search_on_database.id)
        # resize images and save them in search sub-folder
        ImageStore.resize_and_save(images, search_path)

    @staticmethod
    def count_user_searches(mail):
        return History.objects.filter(mail=mail).count()
