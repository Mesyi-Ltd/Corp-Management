from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            perms = None
            if request.user.staff.position.perms:
                perms = request.user.staff.position.perms
                perm_pass = False
                for role in allowed_roles:
                    if perms.__dict__[role]:
                        perm_pass = True
                if perm_pass:

                    return view_func(request, *args, **kwargs)

                else:
                    messages.error(request, '权限不足')
                    return redirect('home')
            return HttpResponse("连接出错， 请联系网站管理员")
        return wrapper_func
    return decorator
