from django.db import models
from  django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
# Create your models here.

class ASDictMixin:
    def as_dict(self):
        dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (int, float, str)):
                dict[key] = value
            else:
                dict[key] = str(value)
        return dict

class Client(ASDictMixin,models.Model):
    uuid = models.CharField(max_length=61, unique=True,default='')
    hostname = models.CharField(max_length=128, default='')
    ip = models.GenericIPAddressField(default='0.0.0.0')
    mac = models.CharField(max_length=32,default='')
    paltform = models.CharField(max_length=128,default='')
    arch = models.CharField(max_length=16, default='')
    cpu = models.IntegerField(default=0)
    mem = models.BigIntegerField(default=0)
    pid = models.IntegerField(default=0)
    time = models.FloatField(default=0)

    user = models.CharField(max_length=64, default='')
    application = models.CharField(max_length=64, default='')
    addr = models.CharField(max_length=256, default='')
    remark = models.TextField(default='')

    heartbeat_time = models.DateTimeField(auto_now_add=True)
    register_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'

    def __repr__(self):
        return f'Host<ID: {self.uuid}, Name: {self.hostname}>'

    __str__ = __repr__


    # Judge host is online or not?
    @property
    def is_online(self):
        return timezone.now() - self.heartbeat_time < datetime.timedelta(minutes=5)

    # Register a Host
    @classmethod
    def register(cls, uuid, **kwargs):
        instance  = None
        created = False
        try:
            instance = cls.objects.get(uuid=uuid)
        except ObjectDoesNotExist as e:
            instance = cls()
            setattr(instance, 'uuid', uuid)
            created = True
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return created, instance

    # Set a Heartbeat time
    @classmethod
    def heartbeat(cls, uuid):
        try:
            instance = cls.objects.get(uuid=uuid)
            instance.heartbeat_time = timezone.now()
            instance.save()
            return True
        except ObjectDoesNotExist as e:
            return False


class Resource(ASDictMixin, models.Model):
    uuid = models.CharField(max_length=64, default='')
    time = models.DateTimeField(auto_now_add=True)
    cpu = models.FloatField(default=0)
    mem = models.FloatField(default=0)

    @classmethod
    def create(cls, uuid, **kwargs):
        instance = cls()
        setattr(instance, 'uuid', uuid)
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        db_table = 'resources'
