from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from baskets import views as baskets_views

urlpatterns = [
    url(r'^$', baskets_views.redirect_index, name='index'),
    url(r'^baskets/', include('baskets.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'registration/logged_out.html'} , name='logout'),
    url(r'^vendors/$', baskets_views.vendors, name='vendors'),
    url(r'^vendors_all/$', baskets_views.vendors_all, name='vendors_all'),
    url(r'^vendors/vendors_to_pdf/$', baskets_views.vendors_to_pdf, name='vendors_to_pdf'),
]
