from rest_framework import generics
from django.http import JsonResponse
from rest_framework import serializers
# from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from . import seriallizer
from django.contrib.auth.models import User
# from webGym.models import MainMenu
from rest_framework.response import Response


@api_view(('GET',))
def myCabinet(request):
    data = {
        'name': 'John Doe',
        'age': 25
    }
    return Response(data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = seriallizer.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = seriallizer.UserSerializer
