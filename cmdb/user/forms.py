from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import User

class CreateUserForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()
    age = forms.IntegerField()
    email = forms.CharField()
    telephone = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name','').strip()

        if User.objects.filter(name=name).count() > 0:
            raise forms.ValidationError('User is already exists.')
        return name

    def clean_password2(self):
        password = self.cleaned_data.get('password', '').strip()
        password2 = self.cleaned_data.get('password2', '').strip()

        if password2 != password:
            raise forms.ValidationError('两次密码不一致')
        return password2

    def clean_age(self):
        age = self.cleaned_data.get('age', -1)
        if not isinstance(age, int):
            raise forms.ValidationError('Age must be Interger.')
        elif int(age) > 60 or int(age) < 18:
            raise forms.ValidationError('Age must between 18 to 60.')
        return age


class EditUserForm(forms.Form):
    uid = forms.IntegerField()
    name = forms.CharField()
    age = forms.IntegerField()
    email = forms.CharField()
    telephone = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        uid = self.cleaned_data.get('uid', -1)
        try:
            User.objects.get(id=uid)
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('User does not exists')

        if User.objects.filter(name=name).exclude(id=uid).count() > 0:
            raise forms.ValidationError('User is already exists.')
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age', -1)
        if not isinstance(age, int):
            raise forms.ValidationError('Age must be Interger.')
        elif int(age) > 60 or int(age) < 18:
            raise forms.ValidationError('Age must between 18 to 60.')

        return age

class ChangePasswordForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField()
    oldpassword = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        id = self.cleaned_data.get('id', -1)
        try:
            User.objects.get(id=id)
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('User does not exists')
        if User.objects.filter(name=name).count() == 0:
            raise forms.ValidationError('User does not exists')
        return name

    def clean_oldpassword(self):
        id = self.cleaned_data.get('id', -1)
        oldpassword = self.cleaned_data.get('oldpassword', '').strip()
        user = User.objects.get(id=id)
        if not user.check_password(oldpassword):
            raise forms.ValidationError('旧密码输入错误')
        return oldpassword

    def clean_password2(self):
        password = self.cleaned_data.get('password', '').strip()
        password2 = self.cleaned_data.get('password2', '').strip()

        if password2 != password:
            raise forms.ValidationError('两次密码不一致')
        return password2