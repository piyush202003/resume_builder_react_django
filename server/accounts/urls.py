from django.urls import path

from .views import LoginApiView, RegisterApiView, UserDataApiView


urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('user/<int:user_id>/', UserDataApiView.as_view(), name='user_data')
]