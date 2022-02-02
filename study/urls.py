"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from allauth.account.views import confirm_email
from django.views.generic import TemplateView
from allauth.account import views as allauthviews
# from django_ravepay import urls as raveurls
urlpatterns = [
    path('', include('Myapi.urls')),
    
    path('admin/', admin.site.urls),
    # path("djangorave/", include("djangorave.urls", namespace="djangorave")),
    path('ravepay/', include(('ravepay.urls','ravepay' ), namespace='ravepay')),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', allauthviews.confirm_email, name="account_confirm_email"),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r"^api/", include("rating.urls")),
    # path('django_ravepay/', include(raveurls)),

]




