from django.urls import path
from . import views

urlpatterns = [
    path('sign', views.sign_page),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout_user', views.logout_user),
    path('logout_admin', views.logout_admin),
    path('forgot', views.forgot),
    path('forgot_reset', views.forgot_reset),
    path('change_pwd', views.change_pwd),
    path('update_pwd', views.update_pwd),
]