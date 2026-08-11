from django.shortcuts import redirect

def role_required(role_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("/vendormis/login/")

            if not request.user.groups.filter(name=role_name).exists():
                return redirect("/vendormis/login/")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator