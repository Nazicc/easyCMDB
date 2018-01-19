from django.conf.urls import url
from . import views

app_name = 'agent'

urlpatterns = [
    url(r'^agents/$', view=views.agents, name='agents'),
    url(r'^edit/$', view=views.edit, name='edit'),
    url(r'^modify/$', view=views.modify, name='modify'),
    url(r'^monitor/$', view=views.monitor, name='monitor'),
]