from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^type_card/$', views.TypeCardListView.as_view(), name='type_card'),
    url(r'^type_card/(?P<slug>[-\w]+)$', views.typescard_view, name='typescard_view'),
]