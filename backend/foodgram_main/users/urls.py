from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShowSubscriptionsView, SubscribeView, UsersViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='Users')

urlpatterns = [
    path(
        r'users/<int:id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('', include(router_v1.urls))
]
