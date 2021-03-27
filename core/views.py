from django.shortcuts import redirect, render
from django.conf.urls import handler404,handler500

def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)