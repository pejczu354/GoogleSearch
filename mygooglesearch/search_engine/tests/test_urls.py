from django.urls import reverse, resolve


class TestUrls:

    def test_get_config_data(self):
        path = reverse('get_configuration_data')
        assert resolve(path).view_name=='get_configuration_data'

    def test_set_config_data(self):
        path = reverse('set_configure_data')
        assert resolve(path).view_name=='set_configure_data'

    def test_get_data(self):
        path = reverse('get_data')
        assert resolve(path).view_name=='get_data'

    