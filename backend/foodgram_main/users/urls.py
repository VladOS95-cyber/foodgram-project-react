from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet


router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='Users')

urlpatterns = [
    path('', include(router_v1.urls))
]
