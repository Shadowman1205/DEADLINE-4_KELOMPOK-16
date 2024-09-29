from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return func(request,*args,**kwargs)
            else:
                return render(request, "404.html")
            
        return wrap
    return decorator