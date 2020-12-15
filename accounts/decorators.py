from django.http import HttpResponse
from django.shortcuts import redirect

"""
decorator: is a function that takes another function as a parameter and allows extra functional to be 
added before the parent/original function is called.
"""


def unauthenticated_user(view_func):
    """
    stops an authenticated user from viewing the registration and login page
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff and request.user.is_authenticated:  # if user is logged in
            return redirect('/')  # redirect to home
        elif request.user.is_authenticated:
            return redirect('user_page')
        else:
            return view_func(request, *args,
                             **kwargs)  # call the original function(views.login_user, views.register_user)

    return wrapper_func


def allowed_users(allowed_roles=None):
    """
    shows different pages based on the users role(group) such as admin, customer
    """

    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  # grab the users group

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Oops, you are not authorized to view this page.')

        return wrapper_func

    return decorator


def admin_only(view_func):
    """
    checks the group of the user and returns a view accordingly
    if the user is in the admin, return the original view('home');
    otherwise if the user is in the 'customer' group redirect the user to the 'user-page'
    """

    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user_page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
