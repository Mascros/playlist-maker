from django.conf.urls import url
from . import views

app_name = 'spotify_playlists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^redirect/$', views.redirecter, name='redirect'),
    url(r'^join/p$', views.join, name='join'),
    url(r'^start/$', views.start, name='start'),
    url(r'^save-party/$', views.save_party, name='save_party'),
    url(r'^testing/session/$', views.testing_session, name='testing_session'),
    url(r'^publish/$', views.publish, name='publish')
]
