from django.shortcuts import render, redirect
from . import models
from halls_app.models import City
from django.contrib import messages

# render the login page
def sign_page(request):
    return render(request, 'login.html')

def register(request):
    errors = models.User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/sign')
    else:
        return models.register_model(request)

def success (request):
    return render(request, 'success.html')

def login(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/sign')
    else:
        return models.login_model(request)


def logout_user(request):
    del request.session['userid']
    return redirect('/')

def logout_admin(request):
    del request.session['adminid']
    return redirect('/')

# render password reset request if you forgot
def forgot(request):
    return render(request, 'forgot.html')

# redirect to change password page
def forgot_reset(request):
    return redirect('/change_pwd')

def change_pwd(request):
    return render(request, 'change_pwd.html')

def update_pwd(request):
    errors = models.User.objects.password_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/change_pwd')
    else:
        models.update_pwd_model(request)
        return redirect('/sign')