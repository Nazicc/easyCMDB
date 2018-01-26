from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from user.models import User

class  EditClientForm(forms.Form):
    uuid = forms.CharField(required=True)
    user = forms.CharField(required=True)
    application = forms.CharField(required=True)
    addr = forms.CharField(required=True)
    remark = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_user(self):
        user = self.cleaned_data.get('user', '').strip()
        uuid = self.cleaned_data.get('uuid', '').strip()

        try:
            Client.objects.get(uuid=uuid)
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Client does not exists')

        if User.objects.filter(name=user).count() == 0:
            raise forms.ValidationError('Invalid user.')
        return user