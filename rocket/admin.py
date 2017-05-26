from django.contrib import admin

from rocket.models import (
    Userprofile,
    Portal,
    user_activation_cache,
)

# Register your models here.
admin.site.register(Portal)
admin.site.register(user_activation_cache)
admin.site.register(Userprofile)
