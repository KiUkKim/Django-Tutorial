from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accountapp.views import hello_world, AccountCreateView

app_name = "accountapp"

urlpatterns = [
    path('hello_world/', hello_world, name='hello_world'),

    path('login', LoginView.as_view(template_name='accountapp/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),


    # class view에서는 as_view()를 사용해서 함수형 처럼 받아준다.
    path('create/', AccountCreateView.as_view(), name='create'),
]