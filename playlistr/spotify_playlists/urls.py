from django.conf.urls import url
from . import views

app_name = 'spotify_playlists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^redirect$', views.redirect, name='redirect')
]
