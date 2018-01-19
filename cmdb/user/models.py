from django.db import models
from  django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import hashlib
import base64
import os

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=512, default='cmdb123')
    age = models.IntegerField()
    telephone = models.CharField(max_length=32)
    email = models.EmailField()
    registe_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'User<name: {self.name},age: {self.age}, phone: {self.telephone}>'

    __repr__ = __str__

    def set_password(self, password):
        _salt = base64.b64encode(os.urandom(8))
        _sha256 = hashlib.sha256()
        _sha256.update(_salt+password.encode())
        self.password = f'{_salt.decode()}${_sha256.hexdigest()}'

    def check_password(self, password):
        _salt, _hash = self.password.split('$')
        _sha256 = hashlib.sha256()
        _sha256.update(_salt.encode()+password.encode())
        return _hash == _sha256.hexdigest()


    @classmethod
    def login(cls, name, password):
        try:
            user = User.objects.get(name=name)
            if user.check_password(password):
                user.login_time = timezone.now()
                user.save()
                return user
        except ObjectDoesNotExist as e:
            print('User does not exist or password error')
        return None

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'password': self.password,
            'email': self.email,
            'telephone': self.telephone,
        }

    class Meta:
        db_table = 'users'