from django.urls import path
from user import views
urlpatterns=[
    path('reg/',views.reg_view)
]