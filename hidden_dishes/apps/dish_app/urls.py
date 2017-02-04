from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add$', views.add, name="add"),
    url(r'^profile/(?P<id>\d+)$', views.profile, name="profile")
]
