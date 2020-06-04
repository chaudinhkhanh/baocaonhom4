"""django_ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from carts.views import view
from products.views import home, all, single, search
from carts.views import view, update_cart
from orders.views import checkout, orders
from accounts.views import login_view, logout_view, registration_view, activation_view

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^products/$', all, name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', single, name='single_product'),
    url(r'^s/$', search, name='search'),
    url(r'^cart/$', view, name='cart'),
    url(r'^cart/(?P<slug>[\w-]+)/$', update_cart, name='update_cart'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^orders/$', orders, name='user_orders'),
    # url(r'^product/(?P<product_id>[0-9]+)/$', product, name='product'),
    # url(r'^cart/$', view, name='cart'),
    url(r'^accounts/logout/$', logout_view, name='auth_logout'),
    url(r'^accounts/login/$', login_view, name='auth_login'),
    url(r'^accounts/register/$', registration_view, name='auth_register'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', activation_view, name='activation_view'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
