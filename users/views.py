from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import json, logging

from common.views import CsrfProtectedAPIView, CsrfProtectedModelViewSet
from common.authentications import CookieBasedJWTAuthentication
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsOwner


class UserViewSet(CsrfProtectedModelViewSet):
    authentication_classes = [CookieBasedJWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwner, ]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    lookup_value_regex = '[\w\-._]+@[\w\-._]+\.[A-Za-z]+'