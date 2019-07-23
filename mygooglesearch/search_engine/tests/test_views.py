from django.test import RequestFactory
from django.urls import reverse
from search_engine.views import get_configuration_data, set_configure_data, get_data
from mixer.backend.django import mixer
import pytest

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def config(request, db):
    mixer.blend('search_engine.SearchConfig', id=request.param)


def test_set_configure_data(factory, db):
    path = reverse('set_configure_data')
    data = {'config_id': 1, 'time_config': '600'}
    request = factory.post(path, data, content_type='application/json')
    response = set_configure_data(request)
    assert response.status_code == 200


def test_set_configure_data_with_empty_string(factory, db):
    path = reverse('set_configure_data')
    request = factory.post(path, content_type='application/json')
    response = set_configure_data(request)
    assert response.status_code == 400


def test_set_configure_data_failed(factory, db):
    path = reverse('set_configure_data')
    request = factory.post(path, "", content_type='application/json')
    response = set_configure_data(request)
    assert response.status_code == 400


def test_get_config_data(factory, db):
    path = reverse('get_configuration_data')
    request = factory.get(path)
    response = get_configuration_data(request)
    assert response.status_code == 200


@pytest.mark.parametrize('config', [1], indirect=True)
def test_get_data(factory, config):
    path = reverse('get_data')
    data = {'search_item': 'test'}
    request = factory.post(path, data, content_type='application/json')

    response = get_data(request)
    assert response.status_code == 200


@pytest.mark.parametrize('config', [1], indirect=True)
def test_get_data_failed(factory, config):
    path = reverse('get_data')
    request = factory.post(path, content_type='application/json')

    response = get_data(request)
    assert response.status_code == 400
