from django.contrib import admin
from .models import Available, Reserve, Confirm

# Register your models here.

admin.site.register(Available)

admin.site.register(Reserve)

admin.site.register(Confirm)
