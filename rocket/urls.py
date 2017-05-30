from django.conf.urls import url

from .views import (
    grievances,
    Profile,
    ImageUpload,
    login,
    logout,
    signup,
    edit_profile,
    change_password,
    home,
    activateuser,
    profilepage,
)

urlpatterns = [
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^signup/$', signup.as_view(), name='signup'),
    url(r'^logout/$', logout.as_view(), name='logout'),
    url(r'^profile/$', Profile.as_view(), name='profile'),
    url(r'^upload_profile_picture/$', ImageUpload.as_view(),
        name='profile_picture_upload'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^change_password/$', change_password, name='change_password'),
    url(r'^$', home.as_view()),
    url(r'^grievances/$', grievances.as_view(), name="grievances"),
    url(r'^activate/(?P<rhash>[0-9A-Za-z]+)/?$',
        activateuser.as_view(), name='activation_link'),
    url(r'^user/(?P<uname>[\w+]+)/?$', profilepage.as_view()),
]
