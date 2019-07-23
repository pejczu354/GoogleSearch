from mixer.backend.django import mixer
from django.test import RequestFactory
from search_engine.get_set_function import get_data_from_db, get_client_ip, save_result_to_db
import pytest


def test_save_data(db):
    items = {
        "items":[{
            "title": "test",
            "displayLink": "testLinkDisplay",
            "link": "testLink",
            "position": 1,
            "count_words": "test: 2"
        }]
    }
    user_ip = "127.0.0.1"
    search_value = "test1"
    response = save_result_to_db(items, user_ip, search_value)

    assert response==True


def test_save_wrong_data(db):
    items = {}
    user_ip = "127.0.0.1"
    search_value = "test1"
    response = save_result_to_db(items, user_ip, search_value)

    assert response["status"]==507


def test_get_db_data(db):
    items = {
        "items":[{
            "title": "test",
            "displayLink": "testLinkDisplay",
            "link": "testLink",
            "position": 1,
            "count_words": "test: 2"
        }]
    }
    user_ip = "127.0.0.1"
    search_value = "test1"
    response = save_result_to_db(items, user_ip, search_value)
    assert response == True

    get_data_response = get_data_from_db(search_value, user_ip)

    assert isinstance(get_data_response, dict)


def test_get_db_data_failed(db):
    get_data_response = get_data_from_db("NotExist", "123321")

    assert get_data_response == False