from django.contrib import admin
from index.models import Book,Author,UserInfo
admin.site.register([Book,Author,UserInfo])
# Register your models here.
