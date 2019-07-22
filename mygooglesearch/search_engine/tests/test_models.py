from search_engine.models import SearchConfig, SearchInformation, ResultSearch
from mixer.backend.django import mixer
from django.db.models.query import EmptyQuerySet
import pytest 

@pytest.mark.django_db
class TestModels:

    def test_search_config(self):
        search_config = mixer.blend('search_engine.SearchConfig')

        assert isinstance(search_config, SearchConfig)

    def test_empty_search_config(self):
        assert isinstance(SearchConfig.objects.none(), EmptyQuerySet)

    def test_search_information(self):
        search_info = mixer.blend('search_engine.SearchInformation')

        assert isinstance(search_info, SearchInformation)

    def test_empty_search_information(self):
        assert isinstance(SearchInformation.objects.none(), EmptyQuerySet)

    def test_result_search(self):
        result_search = mixer.blend('search_engine.ResultSearch')

        assert isinstance(result_search, ResultSearch)

    def test_empty_result_search(self):
        assert isinstance(ResultSearch.objects.none(), EmptyQuerySet)

    