from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add$', views.add, name="add"),
    url(r'^add_dish$', views.add_dish, name="add_dish"),
    url(r'^profile/(?P<id>\d+)$', views.profile, name="profile"),
    url(r'^plate/(?P<id>\d+)$', views.show_plate, name="show_plate"),
    url(r'^top$', views.top, name="top"),
    url(r'^add_comment/(?P<id>\d+)$', views.add_comment, name="add_comment"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name="delete"),
    url(r'^delete_comment/(?P<id>\d+)$', views.delete_comment, name="delete_comment"),
]
