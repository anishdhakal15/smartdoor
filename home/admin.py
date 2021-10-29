from django.contrib import admin

# Register your models here.
from .models import AdminUsers


admin.site.register(AdminUsers)