from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import logging, jwt

from common.views import CsrfProtectedAPIView, CsrfProtectedModelViewSet
from tunaProducts.serializers import RegisterSerializer
from tunaProducts.throttles import LoginThrottle, RefreshThrottle, TestThrottle
# from users.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def _set_tokens_for_response(request, response, user):
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
        key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
        value=data["refresh"],
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    csrf.get_token(request)


class LoginView(APIView):

    permission_classes = []
    # throttle_classes = [LoginThrottle]

    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                _set_tokens_for_response(request, response, user)
                response.data = {"Success": "Login successfully"}
                return response
            else:
                return Response({"Error": "This account is not active"}, status=400)
        else:
            return Response({"Error": "Invalid credentials"}, status=400)


class RefreshView(CsrfProtectedAPIView):

    permission_classes = [] # do not include auth
    # throttle_classes = [RefreshThrottle]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is missing"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.check_blacklist()
            except Exception as e:
                # return redirect('logout')
                return Response({"error": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            response = Response({"message": "Token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=new_access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            )
            # response.set_cookie(
            #     key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
            #     value=,
            #     expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            #     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            #     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            #     samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            # )
            csrf.get_token(request)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(CsrfProtectedAPIView):

    permission_classes = []
    throttle_classes = []

    def post(self, request, format=None):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'])
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass # continue processing if raised InvalidToken error
            response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(CsrfProtectedAPIView):

    throttle_classes = []

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                response = Response()
                _set_tokens_for_response(request, response, user)
                response.data = {"Success": "Register successfully"}
                return response
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(CsrfProtectedAPIView):

    throttle_classes = []

    def post(self, request, format=None):
        return Response(status=None)


class TestView(CsrfProtectedAPIView):
    
    permission_classes = []
    throttle_classes = [TestThrottle]

    logger = logging.getLogger('tunaProducts')

    def get(self, request):
        return render(request, 'test.html')
    
    def post(self, request):
        self.logger.debug('tuna debug:'+request.data.get('post_data'))
        return render(request, 'test.html', context=request.data)


class TestHTTP205View(CsrfProtectedAPIView):

    permission_classes = []
    throttle_classes = []

    logger = logging.getLogger('tunaProducts')
    def post(self, request):
        # self.logger.debug('tuna debug:')
        return Response({"message": "this is test!!!!"}, status=status.HTTP_205_RESET_CONTENT)