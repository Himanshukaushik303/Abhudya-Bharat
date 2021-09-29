from django.http import HttpResponse
from django.shortcuts import redirect


def allowed_users():
    def decorataor(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                if request.user.groups.all()[0].name in ["active_bps"]:
                    return redirect("productsdash")
                elif request.user.groups.all()[0].name in ["active_ents"]:
                    return redirect("ent_dash")
                elif request.user.groups.all()[0].name in ["admin"]:
                    return redirect("admin_dash")
                else:
                    return redirect("conf")
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorataor


def allowed_roles(roles=[]):
    def decorataor(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                if request.user.groups.all()[0].name in roles:
                    return view_func(request, *args, **kwargs)
                elif request.user.groups.all()[0].name in ["active_ents"]:
                    return redirect("ent_dash")
                elif request.user.groups.all()[0].name in ["admin"]:
                    return redirect("admin_dash")
                else:
                    return redirect("conf")
            else:
                return redirect("regAs")

        return wrapper_func

    return decorataor


def logindirect():
    def decorataor(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect("homepage")
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorataor
