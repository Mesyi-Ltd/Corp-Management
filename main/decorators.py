from django.http import HttpResponse
from django.shortcuts import redirect


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            perms = None
            if request.user.staff.position.perms:
                perms = request.user.staff.position.perms
                all_pass = True
                for role in allowed_roles:
                    if not perms.__dict__[role]:
                        all_pass = False
                if all_pass:

                    return view_func(request, *args, **kwargs)

                else:

                    return redirect('login')
            return HttpResponse("连接出错， 请联系网站管理员")
        return wrapper_func
    return decorator
