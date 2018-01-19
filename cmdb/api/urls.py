from django.conf.urls import url
from .views import v1

app_name = 'api'

urlpatterns = [
    url(r'^v1/register/(?P<uuid>\w{32,64})/$', view=v1.RegisterView.as_view(), name='register'),
    url(r'^v1/heartbeat/(?P<uuid>\w{32,64})/$', view=v1.HeartbeatView.as_view(), name='heartbeat'),
    url(r'^v1/resource/(?P<uuid>\w{32,64})/$', view=v1.ResourceView.as_view(), name='resource'),
]