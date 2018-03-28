import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .forms import CreateUserForm
from .forms import EditUserForm
from .forms import ChangePasswordForm
# Create your views here.
def index(request):
    return render(request, 'user/login.html')

def login(request):
    name = request.POST.get('name')
    password = request.POST.get('password')
    user = User.login(name, password)
    if user:
        request.session['user'] = {'name': user.name, 'id': user.id,}
        return redirect('user:users')
    else:
        context = {}
        context['error'] = '用户名或密码错误'
        context['name'] = name   # 用户名回显
        return render(request, 'user/login.html', context)

def users(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    context = {
        'data': User.objects.all(),
    }
    return  render(request, 'user/users.html',context)

class PasswordChangeView(View):
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=form.cleaned_data.get('id'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return JsonResponse({'code': 200, 'text': 'success', 'result': None, 'errors': {}})
        else:
            return JsonResponse({'code': 400, 'text': 'error', 'result': None, 'errors': json.loads(form.errors.as_json())})


def save(request):
    if request.session.get('user') is None:
        return redirect('user:index')
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = User()
        user.is_admin = False
        user.name = request.POST.get('name', '').strip()
        user.set_password(request.POST.get('password', '').strip())
        user.email = request.POST.get('email', '').strip()
        user.telephone = request.POST.get('telephone', '').strip()
        user.age = request.POST.get('age', '').strip()

        user.save()
        return redirect('user:users')
    else:
        context = {}
        context['form'] = form.errors
        context['password'] = request.POST.get('password', '')
        context['name'] = request.POST.get('name', '')
        context['email'] = request.POST.get('email', '')
        context['telephone'] = request.POST.get('telephone', '')
        context['age'] = request.POST.get('age', '')

        return render(request, 'user/create.html',context)

def edit(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    uid = request.GET.get('id', -1)
    try:
        user = User.objects.get(id=uid)
        return render(request, 'user/edit.html', user.as_dict())
    except ObjectDoesNotExist as e:
        return redirect('user:users')



def modify(request):
    if request.session.get('user') is None:
        return redirect('user:index')
    form = EditUserForm(request.POST)
    if form.is_valid():
        uid = request.POST.get('uid', -1)
        user = User.objects.get(id=uid)

        user.name = request.POST.get('name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.telephone = request.POST.get('telephone', '').strip()
        user.age = request.POST.get('age', '').strip()
        user.save()
        return redirect('user:users')

    else:
        context = {}
        context['form'] = form.errors
        context['name'] = request.POST.get('name', '')
        context['email'] = request.POST.get('email', '')
        context['telephone'] = request.POST.get('telephone', '')
        context['age'] = request.POST.get('age', '')
        context['id'] = request.POST.get('uid', -1)
        return render(request, 'user/edit.html', context)


def delete(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    uid = request.GET.get('id', -1)
    User.objects.filter(pk=uid).delete()
    return redirect('user:users')

def logout(request):
    request.session.flush()

    return redirect('user:index')

