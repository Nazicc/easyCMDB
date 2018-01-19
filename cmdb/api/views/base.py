from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json

class APIView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)

    def get_json(self):
        try:
            return json.loads(self.request.body.decode())
        except BaseException as e:
            return {}

    def response(self, result=None, code=200, text='SUCCESS'):
        return JsonResponse({'code': code, 'text': text, 'result': result})
