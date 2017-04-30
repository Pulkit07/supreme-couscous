from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout
from .views import grievances

urlpatterns=[
    url(r'^login/$', login, {'template_name':'rocket/login.html'}),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^$', views.home),
    url(r'^grievances/$', grievances.as_view(),name="grievances"),
]
