from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseAbstractModel(models.Model):
    """
    Base class with commom itens for each model
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
