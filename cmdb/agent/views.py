from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from .models import Resource
from .forms import EditClientForm
# Create your views here.
def agents(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    context = {
        'data': Client.objects.all(),
    }
    return  render(request, 'agent/agents.html', context)

def edit(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    uuid = request.GET.get('uuid', '')
    try:
        client = Client.objects.get(uuid=uuid)
        context = {}
        context['uuid'] = client.uuid
        context['user'] = client.user
        context['addr'] = client.addr
        context['application'] = client.application
        return render(request, 'agent/edit.html', context)

    except ObjectDoesNotExist as e:
        return redirect('agent:agents')

def modify(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    form = EditClientForm(request.POST)
    if form.is_valid():
        uuid = request.POST.get('uuid', '')
        client = Client.objects.get(uuid=uuid)

        client.user = request.POST.get('user', '').strip()
        client.application = request.POST.get('application', '').strip()
        client.addr = request.POST.get('addr', '').strip()
        client.remark = request.POST.get('remark', '').strip()
        client.save()
        return redirect('agent:agents')
    else:
        context = {}
        context['form'] = form.errors
        context['uuid'] = request.POST.get('uuid', '').strip()
        context['user'] = request.POST.get('user', '').strip()
        context['addr'] = request.POST.get('addr', '').strip()
        context['application'] = request.POST.get('application').strip()
        return render(request, 'agent/edit.html', context)

def monitor(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    uuid = request.GET.get('uuid', '')
    context = {
        'data': Resource.objects.filter(uuid=uuid),
    }
    return render(request, 'agent/resource.html', context)