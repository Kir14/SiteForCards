from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^type_card/$', views.TypeCardListView.as_view(), name='type_card'),
    url(r'^type_card/(?P<slug>[-\w]+)$', views.typescard_view, name='typescard_view'),
    url(r'^order_card/(?P<slug>[-\w]+)$', views.order_card, name='order_card'),
    url(r'^my_card/', views.my_card, name='my_card'),
    url(r'^registration/', views.registration, name='registration'),
]
