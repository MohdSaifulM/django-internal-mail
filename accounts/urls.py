from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.sign_up, name="register"),
    path('signin/', views.sign_in, name="login"),
    path('logout/', views.sign_out, name="logout")
]