from django.conf.urls import patterns, url
from idt import views

urlpatterns = patterns(
    '',
    url(r'^identitone', views.get_raw_identitone, name='raw_get_identitone'),
    url(r'^idt', views.get_raw_identitone, name='raw_get_idt'),
    url(r'^(?P<seed_hash>[0-9abcdef]{128})/', views.get_identitone, name='get_identitone'),
)
