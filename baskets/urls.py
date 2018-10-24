from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.baskets, name='baskets'),
#    url(r'^$', views.list_baskets, name='index'),
    url(r'^(?P<basket_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<basket_id>[0-9]+)/add_item/$', views.add_item, name='add_item'),
    url(r'^add_basket/$', views.add_basket, name='add_basket'),
    url(r'^(?P<basket_id>[0-9]+)/delete_item/(?P<item_id>[0-9]+)/$', views.delete_item, name='delete_item'),
    url(r'^vendor/(?P<vendor_number>[0-9]+)$', views.vendor_detail, name='vendor_detail'),
]

