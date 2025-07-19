from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test




def client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_client,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator




def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is an admin,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator












# from django.http import HttpResponse
# from django.shortcuts import redirect

#
# def client_required(view_func):
#     def wrapper_function(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.is_client:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect('home')
#         else:
#             return redirect('home')
#     return wrapper_function
#
#
#
# def admin_required(view_func):
#     def wrapper_function(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.is_admin:
#                 return view_func(request, *args, **kwargs)
#             elif request.user.is_client:
#                 return redirect('clienthome')
#             else:
#                 return redirect('home')
#         else:
#             return redirect('home')
#     return wrapper_function