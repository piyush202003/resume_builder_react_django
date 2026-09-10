from django.urls import path

from .views import LoginApiView, RegisterApiView, UserDataApiView, UserResumesApiView


urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('data/', UserDataApiView.as_view(), name='user_data'),
    path('resumes/', UserResumesApiView.as_view(), name='user_resumes'),
]