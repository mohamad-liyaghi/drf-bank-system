from django.urls import  path
from . import  views
app_name = "v1"

urlpatterns = [
    path("register/", views.RegisterUserApi.as_view(), name= "register-user"),
]