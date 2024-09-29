from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
import logging, jwt

from common.views import CsrfProtectedAPIView, CsrfProtectedModelViewSet
from tunaProducts.throttles import LoginThrottle, RefreshThrottle


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):

    # throttle_classes = [LoginThrottle]

    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                response.set_cookie(
                    key='refresh_token',
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully"}
                return response
            else:
                return Response({"Error": "This account is not active"}, status=400)
        else:
            return Response({"Error": "Invalid credentials"}, status=400)


class RefreshView(TokenRefreshView):
    throttle_classes = [RefreshThrottle]