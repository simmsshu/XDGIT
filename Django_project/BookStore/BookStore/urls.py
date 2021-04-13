"""BookStore URL Configuration

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
from django.urls import path,include
from index.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_html/', test_html),
    path('test_if/', test_if),
    path('test_forloop/', test_forloop),
    path('test_filter/', test_filter,name='_filter'),
    path('test_url/<int:id>',test_urls,name='hello'),
    path('base_html/',base_html),
    path('index_html/',index_html),
    path('index/',include('index.urls')),
    path('logincbv/',LoginView.as_view(username="test")),
    path('user/',include('user.urls')),


]
