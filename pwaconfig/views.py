from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from SEGUE import settings
import json


def service_worker(request):
    response = HttpResponse(
        open(settings.PWA_SERVICE_WORKER_PATH).read(),
        content_type='application/javascript'
    )
    return response


"""def manifest(request):
    return render(request, 'manifest.json', {
        setting_name: getattr(app_settings, setting_name)
        for setting_name in dir(app_settings)
        if setting_name.startswith('PWA_')
})"""

def manifest(request):
    with open(settings.PWA_MANIFEST_JSON, 'r') as file:
        return JsonResponse(json.load(file))