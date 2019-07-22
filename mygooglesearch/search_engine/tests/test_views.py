from django.test import RequestFactory
from django.urls import reverse
from search_engine.views import get_configuration_data, set_configure_data, get_data
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestViews:

    def test_set_configure_data(self):
        factory = RequestFactory()
        path = reverse('set_configure_data')
        data = {'config_id': None, 'time_config': '600'}
        request = factory.post(path, data, content_type='application/json')

        response = set_configure_data(request)
        assert response.status_code == 200


    def test_get_client_ip(self):
        path = reverse('get_configuration_data')
        request = RequestFactory().get(path)

        response = get_configuration_data(request)
        assert response.status_code == 200


    def test_get_data(self):
        mixer.blend('search_engine.SearchConfig', id=1)
        factory = RequestFactory()
        path = reverse('get_data')
        data = {'search_item': 'test'}
        request = factory.post(path, data, content_type='application/json')

        response = get_data(request)
        assert response.status_code == 200
