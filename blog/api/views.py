from rest_framework import generics, viewsets
from account.models import *
from blog.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    @action(detail=False,
            methods=['post'])
    def get_profile(self, request, *args, **kwargs):
        api_key = request.data.get('api_token')
        if api_key:
            try:
                profile = Profile.objects.get(api_key=api_key)
                return Response({
                    'status': 'success',
                    'message': 'data fetched',
                    'data': ProfileSerializer(profile.data),
                })
            except:
                return Response({
                    'status': 'error',
                    'message': 'invalid API key'
                })
        else:
            return Response({
                'status': 'error',
                'message': 'No API key provided'
            })
    