from rest_framework import exceptions, status


class ProductUnavailableError(exceptions.APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "This product is unavailable"
