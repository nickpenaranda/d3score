from django.conf.urls import patterns, url

from score import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
    url(r'^profile$', views.profile, name='index')
    url(r'^hero$', views.hero, name='index')
)
