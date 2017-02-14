from django.conf.urls import patterns, include, url

from django.contrib import admin
from score import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dscore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^(?P<name>\w+)-(?P<number>\d+)/$', views.index),
    url(r'^(?P<name>\w+)-(?P<number>\d+)/(?P<hero_id>\d+)/$', views.index),
    url(r'^p', views.profile, name='profile'),
    url(r'^h', views.hero, name='hero'),
    url(r'^deckard/', include(admin.site.urls)),
)
