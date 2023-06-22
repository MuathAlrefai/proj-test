from django.db import models
from django.shortcuts import redirect
import re
import bcrypt
# from halls_app.models import City

class Validator(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        db_emails = User.objects.filter(email = post_data['email'])
        if len(db_emails) > 0:
            errors['email'] = "This Email is already in use!"
        db_usernames = User.objects.filter(username = post_data['username'])
        if len(db_usernames) > 0:
            errors['email'] = "This username is already in use!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.@+_-]+$')
        if not PASSWORD_REGEX.match(post_data['password']):
            errors['password'] = "Password cannot contain these characters!"
        FIRSTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not FIRSTNAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "Name must be in alphabetical letters only!"
        LASTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not LASTNAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Name must be in alphabetical letters only!"
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if len(post_data['password']) < 10 :
            errors['password'] = "Password must be at least 8 characters"
        if post_data['password'] != post_data['confirm_password'] :
            errors['confirm_password'] = "Your password didn't match!"
        return errors
    
    # password validator for changing user password
    def password_validator(self, post_data):
        errors = {}
        PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.@+_-]+$')
        if not PASSWORD_REGEX.match(post_data['password']):
            errors['password'] = "Password cannot contain these characters!"
        if len(post_data['password']) < 10 :
            errors['password'] = "Password must be at least 8 characters"
        if post_data['password'] != post_data['confirm_password'] :
            errors['confirm_password'] = "Your password didn't match!"
        return errors
    
    # def pie_validator(self, post_data):
    #     errors = {}
    #     if len(post_data['pie_name']) < 3:
    #         errors['pie_name'] = "Your pie name must be at least 3 characters"
    #     if len(post_data['pie_filling']) < 5:
    #         errors['pie_filling'] = "Your pie filling must be at least 5 characters"
    #     if len(post_data['pie_crust']) < 5:
    #         errors['pie_crust'] = "Your pie crust must be at least 5 characters"
    #     return errors
    
    def login_validator(self, post_data):
        errors = {}
        db_usernames = User.objects.filter(username = post_data['username'])
        if len(db_usernames) == 0:
            errors['username'] = "This username doesn't exist!"
        if len(post_data['username']) < 1:
            errors['username'] = "You must enter username"
        if len(post_data['log_password']) < 1:
            errors['log_password'] = "you must enter password"
        return errors


class User(models.Model):
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, default=0000000000)
    # city = models.ForeignKey(City, related_name='users')
    # city = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Validator()

def register_model(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    # city = request.POST['city']
    #hash the password before adding it to DB
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email, password = password_hash)
    # #create a session for the user and redirect to profile page
    # user = User.objects.filter(email=request.POST['email'])
    # logged_user = user[0]
    # request.session['userid'] = logged_user.id
    return redirect('/success')
    

def login_model(request):
    user = User.objects.filter(username=request.POST['username'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['log_password'].encode(), logged_user.password.encode()):
            if logged_user.id == 1:
                request.session['adminid'] = logged_user.id
                return redirect('/cities_admin')
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['log_password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/cities')
    return redirect('/sign')

def update_pwd_model(request):
    user = User.objects.get(username = request.POST['username'])
    user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user.save()