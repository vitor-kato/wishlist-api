from django.contrib import admin
from .models import Wishlist, Product

admin.site.register([Wishlist, Product])