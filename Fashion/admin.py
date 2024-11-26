from django.contrib import admin
from .models import new_user, Wardrobe, Rec, Category, Favourites
# Register your models here.

admin.site.register(new_user)
admin.site.register(Wardrobe)
admin.site.register(Rec)
admin.site.register(Category)
admin.site.register(Favourites)