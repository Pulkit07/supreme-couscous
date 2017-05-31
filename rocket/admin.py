from django.contrib import admin

from rocket.models import (
    Userprofile,
    Portal,
    user_activation_cache,
    password_forget_cache,
)

# Register your models here.
admin.site.register(Portal)
admin.site.register(user_activation_cache)
admin.site.register(Userprofile)
admin.site.register(password_forget_cache)
