from django.contrib import admin
from .models import Movie, Collection

# Register your models here.
# for checking the data in admin login
admin.site.register(Movie)
admin.site.register(Collection)