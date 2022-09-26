from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

app_name = "v2"

router = routers.DefaultRouter()

router.register('card', views.CardViewSet, basename="card")

urlpatterns = router.urls