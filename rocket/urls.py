from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from .views import grievances, Profile, ImageUpload

urlpatterns = [
    url(r'^login/$', views.loginview.as_view(), name='login'),
    url(r'^signup/$', views.signup.as_view(), name='signup'),
    url(r'^profile/$', Profile.as_view(), name='profile'),
    url(r'^upload_profile_picture/$', ImageUpload.as_view(),
        name='profile_picture_upload'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^$', views.home),
    url(r'^grievances/$', grievances.as_view(), name="grievances"),
    url(r'^activate/(?P<rhash>[0-9A-Za-z]+)/?$',
        views.activationview.as_view(), name='activation_link'),
]
