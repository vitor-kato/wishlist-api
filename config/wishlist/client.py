import requests
from django.conf import settings
from django.core.cache import cache

from .exceptions import ProductUnavailableError


class ProductClient:
    """This client interfaces with an external products API
    When a product is available, its data is returned
    and cached with Django low-level cache API

    The data has a default expiration time which can be set on the settings
    And when expired, its refreshed on the next request

    Raises:
        ProductUnavailableError: When a invalid ID is passed the client
        should raise this. This is useful when creating the product
        so in the view the error is returned to the response

    Returns:
        data: The product data, it can contain the following fields
        [price, image, brand, id, title, reviewScore]
        which should be available another API using this service
    """

    base_url = settings.PRODUCT_DATA_API
    cache_time = settings.PRODUCT_DATA_API_CACHE_TIME

    def __init__(self, id):
        self.id = id
        self.cache_key = f"product_data_{self.id}"

    def get_data(self):
        url = f"{self.base_url}/{self.id}/"
        r = requests.get(url)
        self.status = r.status_code
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
