"""
URL configuration for tunaProducts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tunaProducts.views import (LoginView,
                                RefreshView,
                                LogoutView,
                                RegisterView,
                                TestView,TestHTTP205View,
                                ChangePasswordView,)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('test/', TestView.as_view(), name='test'),
    path('test2/', TestHTTP205View.as_view(), name='test2'),

    path('', include('users.urls')),
]
