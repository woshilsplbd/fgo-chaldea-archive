from django.contrib import admin
from .models import MyNew

class MyNewAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyNew, MyNewAdmin)