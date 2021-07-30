from django.urls import path, include

from .views import ShowSubscriptionsView, SubscribeView, CustomAuthToken, Logout


urlpatterns = [
    path(
        'users/<int:author_id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomAuthToken.as_view()),
    path('auth/token/logout/', Logout.as_view())
]
