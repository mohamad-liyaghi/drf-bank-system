from django.urls import  path
from . import  views

app_name = "v1"


urlpatterns = [
    path("register/", views.RegisterUserApi.as_view(), name= "register-user"),

    path("card/", views.CardListApi.as_view(), name="list-card"),
    path("create-card/", views.CardCreateApi.as_view(), name="create-card"),
    path("card-detail/<str:token>/", views.CardDetailApi.as_view(), name="detail-cart"),

]

