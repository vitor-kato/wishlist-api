import requests
from django.conf import settings
from django.core.cache import cache

from .exceptions import ProductUnavailableError


class ProductClient:
    base_url = settings.PRODUCT_DATA_API
    cache_time = settings.PRODUCT_DATA_API_CACHE_TIME

    def __init__(self, id):
        self.id = id
        self.cache_key = f"product_data_{self.id}"

    def get_data(self):
        url = f"{self.base_url}/{self.id}/"
        r = requests.get(url)
        if not r.status_code == 200:
            raise ProductUnavailableError
        self.data = r.json()
        self.set_cache(self.data)
        return self.data

    def set_cache(self, data):
        cache.set(self.cache_key, data, self.cache_time)

    def get_cache(self):
        data = cache.get(self.cache_key)
        if not data:
            return self.get_data()
        return data
