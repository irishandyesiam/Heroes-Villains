from django.contrib import admin
from .models import Super
from .models import SuperType

# Register your models here.
admin.site.register(Super)
admin.site.register(SuperType)