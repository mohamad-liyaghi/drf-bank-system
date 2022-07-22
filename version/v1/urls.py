from django.urls import  path
from . import  views

app_name = "v1"

urlpatterns = [
    path("register/", views.RegisterUserApi.as_view(), name= "register-user"),

    path("create-card/", views.CardCreateApi.as_view(), name="create-card"),
]