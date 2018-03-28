from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from .models import Resource
from .forms import EditClientForm
from django.views.generic import ListView,View

# Create your views here.

class ClientListView(ListView):
    model = Client
    template_name = 'agent/agents.html'

class ClientModifyView(View):
    def post(self, request, *args, **kwargs):
        form = EditClientForm(request.POST)
        if form.is_valid():
            client = Client.objects.get(uuid=form.cleaned_data.get('uuid'))
            client.addr = form.cleaned_data.get('addr')
            client.application = form.cleaned_data.get('application')
            client.user = form.cleaned_data.get('user')
            client.remark = form.cleaned_data.get('remark')
            client.save()
            return JsonResponse({'code' : 200, 'text' : 'success', 'result' : None, 'errors' : {}})
        else:
            print(form.errors.as_json())
            return JsonResponse({'code' : 400, 'text' : 'error', 'result' : None, 'errors' : json.loads(form.errors.as_json())})


class ResourceListView(View):
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get('uuid', '')
        resources = Resource.objects.filter(uuid=uuid).order_by('-time')[:180]
        result = [resource.as_dict() for resource in resources]
        return JsonResponse({'code' : 200, 'text' : 'success', 'result' : result, 'errors' : {}})