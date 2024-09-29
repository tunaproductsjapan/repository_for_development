from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views import View
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

@method_decorator(csrf_protect, name='dispatch')
class CsrfProtectedView(View):
    pass

@method_decorator(csrf_protect, name='dispatch')
class CsrfProtectedAPIView(APIView):
    pass

@method_decorator(csrf_protect, name='dispatch')
class CsrfProtectedModelViewSet(ModelViewSet):
    pass