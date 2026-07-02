from .models import User, UserFollows
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Admin panel
admin.site.register(User, UserAdmin)
admin.site.register(UserFollows)
