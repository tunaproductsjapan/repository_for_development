from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

from .views import TestView


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/test/', TestView.as_view(), name='test_view'),
]