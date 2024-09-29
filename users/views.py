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
from users.throttles import TestThrottle


class UserViewSet(CsrfProtectedModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [CookieBasedJWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwner, ]
    lookup_field = 'email'
    lookup_value_regex = '[\w\-._]+@[\w\-._]+\.[A-Za-z]+'


# @method_decorator(csrf_exempt, name='dispatch')
class TestView(CsrfProtectedAPIView):
    permission_classes = []
    throttle_classes = [TestThrottle]

    logger = logging.getLogger('tunaProducts')

    def get(self, request):
        return render(request, 'test.html')
    
    def post(self, request):
        self.logger.debug('tuna debug:'+request.data['post_data'])
        return render(request, 'test.html', context=request.data)