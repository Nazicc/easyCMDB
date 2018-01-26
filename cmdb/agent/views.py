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
#
# def agents(request):
#     if request.session.get('user') is None:
#         return redirect('user:index')
#
#     context = {
#         'data': Client.objects.all(),
#     }
#     return  render(request, 'agent/agents.html', context)

# def edit(request):
#     if request.session.get('user') is None:
#         return redirect('user:index')
#
#     uuid = request.GET.get('uuid', '')
#     try:
#         client = Client.objects.get(uuid=uuid)
#         context = {}
#         context['uuid'] = client.uuid
#         context['user'] = client.user
#         context['addr'] = client.addr
#         context['application'] = client.application
#         return render(request, 'agent/edit.html', context)
#
#     except ObjectDoesNotExist as e:
#         return redirect('agent:agents')
#
# def modify(request):
#     if request.session.get('user') is None:
#         return redirect('user:index')
#
#     form = EditClientForm(request.POST)
#     if form.is_valid():
#         uuid = request.POST.get('uuid', '')
#         client = Client.objects.get(uuid=uuid)
#
#         client.user = request.POST.get('user', '').strip()
#         client.application = request.POST.get('application', '').strip()
#         client.addr = request.POST.get('addr', '').strip()
#         client.remark = request.POST.get('remark', '').strip()
#         client.save()
#         return redirect('agent:agents')
#     else:
#         context = {}
#         context['form'] = form.errors
#         context['uuid'] = request.POST.get('uuid', '').strip()
#         context['user'] = request.POST.get('user', '').strip()
#         context['addr'] = request.POST.get('addr', '').strip()
#         context['application'] = request.POST.get('application').strip()
#         return render(request, 'agent/edit.html', context)
#
# def monitor(request):
#     if request.session.get('user') is None:
#         return redirect('user:index')
#
#     uuid = request.GET.get('uuid', '')
#     context = {
#         'data': Resource.objects.filter(uuid=uuid),
#     }
#     return render(request, 'agent/resource.html', context)
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