from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils import timezone
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateUserForm
from .forms import EditUserForm

# Create your views here.
def index(request):
    # print(request.GET, request.POST)
    # print(request.POST.get('user'), request.POST.get('password'))
    # # 此处request.GET字典中的key是input中的name字段决定
    return render(request, 'user/login.html')

def login(request):
    #print(request.POST)
    name = request.POST.get('name')
    password = request.POST.get('password')
    #print(name,type(name))
    user = User.login(name,password)
    if user:
        request.session['user'] = {'name': user.name, 'id': user.id,}
        return redirect('user:users')
    else:
        context = {
        }
        context['error'] = '用户名或密码错误'
        context['name'] = name  # 用户名回显
        return render(request, 'user/login.html', context)

def users(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    context = {
        'data': User.objects.all(),
    }
    return  render(request, 'user/users.html',context)

def create(request):
    if request.session.get('user') is None:
        return redirect('user:index')

    return render(request, 'user/create.html')


# def valid_save(params):
#     is_valid = True
#     errors = {}
#     name = params.get('name', '').strip()
#     password = params.get('password', '').strip()
#     password2 = params.get('password2', '').strip()
#     age = params.get('age', '').strip()
#     email = params.get('email', '').strip()
#     telephone = params.get('telephone', '').strip()
#
#     # judge valid or not?
#     errors['name'] = []
#     if not name:
#         errors['name'].append('Username can not be None.')
#         is_valid = False
#     elif User.objects.filter(name=name).count() >0:
#         errors['name'].append('Username is already exist.')
#         is_valid = False
#
#     errors['password'] = []
#     if not password:
#         errors['password'].append('Password can not be None.')
#         is_valid = False
#     elif password != password2:
#         errors['password'].append('Password can not be confirmed successfully.')
#         is_valid = False
#
#     errors['age'] = []
#     if not age.isdigit():
#         errors['age'].append('Age must be Integer.')
#         is_valid = False
#     elif int(age) > 60 or int(age) < 18:
#         errors['age'].append('Age must between 18 to 60.')
#         is_valid = False
#
#     return is_valid, errors

def save(request):
    if request.session.get('user') is None:
        return redirect('user:index')
    # is_valid, errors = valid_save(request.POST)
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


# def valid_modify(params):
#     is_valid = True
#     errors = {}
#     uid = params.get('uid', -1)
#     name = params.get('name', '').strip()
#     age = params.get('age', '').strip()
#     email = params.get('email', '').strip()
#     telephone = params.get('telephone', '').strip()
#
#     # judge valid or not?
#     errors['name'] = []
#     try:
#         User.objects.get(id=uid)
#     except ObjectDoesNotExist as e:
#         errors['name'].append('User does not exists.')
#         is_valid = False
#
#     if not name:
#         errors['name'].append('Username can not be None.')
#         is_valid = False
#     elif User.objects.filter(name=name).exclude(id=uid).count() >0:
#         errors['name'].append('Username is already exist.')
#         is_valid = False
#
#     errors['age'] = []
#     if not age.isdigit():
#         errors['age'].append('Age must be Integer.')
#         is_valid = False
#     elif int(age) > 60 or int(age) < 18:
#         errors['age'].append('Age must between 18 to 60.')
#         is_valid = False
#
#     return is_valid, errors

def modify(request):
    if request.session.get('user') is None:
        return redirect('user:index')
    # is_valid, errors = valid_modify(request.POST)
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

