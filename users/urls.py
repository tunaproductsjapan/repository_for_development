from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, TestView


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('test/', TestView.as_view(), name='test'),
]