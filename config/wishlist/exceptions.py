from rest_framework import exceptions, status


class ProductUnavailableError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This product is unavailable"
