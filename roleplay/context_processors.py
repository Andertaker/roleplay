# -*- coding: utf-8 -*-
#from django.http import HttpRequest, HttpResponse


def url_reslove(request):
    context = {}
    rslv = request.resolver_match
    
    context["url_name"] = rslv.url_name
    context["app_name"] = rslv.app_name
    context["args"] = rslv.args
    context["kwargs"] = rslv.kwargs
    context["namespace"] = rslv.namespace
    context["namespaces"] = rslv.namespaces
    
    return context