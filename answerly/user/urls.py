from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='sign_up')
]