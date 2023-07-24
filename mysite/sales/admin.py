from django.contrib import admin
from .models import User, Commodities, Pays, ShoppingCart, LoginUser

# Register your models here.

admin.site.register(User)
admin.site.register(Commodities)
admin.site.register(Pays)
admin.site.register(ShoppingCart)
admin.site.register(LoginUser)
