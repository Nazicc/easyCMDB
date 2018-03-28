from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from agent.models import Client
from agent.models import Resource
from .base import APIView
import time
# Create your views here.

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        json_body = self.get_json()
        created, client = Client.register(uuid, **json_body)
        return self.response({'created': created, 'client':client.as_dict()})

class HeartbeatView(APIView):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        Client.heartbeat(uuid)
        return self.response(time.time())

class ResourceView(APIView):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        json_body = self.get_json()
        resource = Resource.create(uuid, **json_body)
        return self.response(resource.as_dict())