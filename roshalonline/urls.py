"""roshalonline URL Configuration

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
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls import url
from django.contrib import admin
from ro_app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^subscribe/', views.subscribe),
    url(r'^feedback/', views.feedback),
    url(r'^calls/', views.phone_calls),
    url(r'^prices/', views.calulated_phone_tarif),
    url(r'^admin/', admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)