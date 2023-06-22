from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

######################## ANY USER PAGES ########################

# render the landing page
def landing(request):
    return render(request, 'landing.html')

# render cities page
def cities_all(request):
    context = {
        "cities": models.get_cities_model(request),
    }
    return render(request, 'no_user/cities_all.html', context)

# render all halls
def halls_all(request):
    context = {
        "halls": models.get_halls_model(),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'no_user/halls_all.html', context)

# render a single city's halls
def city_halls_all(request, city_name):
    context = {
        "city": models.get_city_by_name_model(city_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'no_user/city_halls_all.html', context)

# render a single hall's info for all users
def hall_info_all(request, city_name, hall_name):
    context = {
        "city": models.get_city_by_name_model(city_name),
        "hall": models.get_hall_by_name_model(hall_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'no_user/city_hall_info_all.html', context)

# render about us page for all
def about_all(request):
    return render(request, 'no_user/about_all.html')

# render help page for all
def help_all(request):
    return render(request, 'no_user/help_all.html')


######################## LOGGED USER PAGES ########################

# render user cities
def cities(request):
    context = {
        "user": models.get_user_session(request),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'user/cities.html', context)

# render about us page
def about(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'about.html', context)

# render help page
def help(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'help.html', context)

# render all halls
def halls(request):
    context = {
        "user": models.get_user_session(request),
        "halls": models.get_halls_model(),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'user/halls.html', context)

# render a single city's halls
def city_halls(request, city_name):
    context = {
        "user": models.get_user_session(request),
        "city": models.get_city_by_name_model(city_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'user/city_halls.html', context)

# render a single hall's info
def hall_info(request, city_name, hall_name):
    context = {
        "user": models.get_user_session(request),
        "city": models.get_city_by_name_model(city_name),
        "hall": models.get_hall_by_name_model(hall_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'user/city_halls_info.html', context)

# render the user profile page
def profile(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'user/profile.html', context)

# render edit profile page
def edit_profile(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'user/edit_profile.html', context)

# update profile and redirect to updated profile
def update_profile(request):
    models.update_profile_model(request)
    return redirect('/profile')

# render change user password form
def change_password(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'user/change_password.html', context)

# update user password and redirect back to profile page
def update_password(request):
    errors = models.User.objects.password_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/change_password')
    else:
        models.update_password_model(request)
        return redirect('/profile')

# book a specific hall from the info page
def book_hall(request):
    models.book_hall_model(request)
    return redirect('/book_success')

# render a successful booking (purchase) for a hall
def book_success(request):
    context = {
        "user": models.get_user_session(request),
    }
    return render(request, 'user/book_success.html', context)


######################## ADMIN PAGES ########################

# render the admin route
def cities_admin(request):
    context = {
        "admin": models.get_admin_session(request),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'admin/admin_cities.html', context)

# add a new city
def add_city(request):
    models.add_city_model(request)
    return redirect('/cities_admin')

# render the admin profile page
def profile_admin(request):
    context = {
        "admin": models.get_admin_session(request),
    }
    return render(request, 'admin/admin_profile.html', context)

# render admin edit profile page
def edit_profile_admin(request):
    context = {
        "admin": models.get_admin_session(request),
    }
    return render(request, 'admin/admin_edit_profile.html', context)

# update admin profile and redirect to updated profile
def update_profile_admin(request):
    models.update_profile_admin_model(request)
    return redirect('/profile_admin')

# delete a city
def delete_city(request):
    city = models.City.objects.get(id = request.POST['city_id'])
    city.delete()
    return redirect('/cities_admin')

# delete a hall
def delete_hall(request):
    city = models.Hall.objects.get(id = request.POST['hall_id'])
    city.delete()
    return redirect('/halls_admin')

# render all halls
def halls_admin(request):
    context = {
        "admin": models.get_admin_session(request),
        "halls": models.get_halls_model(),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'admin/admin_halls.html', context)

# add a new hall
def add_hall(request):
    models.add_hall_model(request)
    return redirect('/halls_admin')

# render a single city's halls
def city_halls_admin(request, city_name):
    context = {
        "admin": models.get_admin_session(request),
        "city": models.get_city_by_name_model(city_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'admin/admin_city_halls.html', context)

# render a single hall's info
def hall_info_admin(request, city_name, hall_name):
    context = {
        "admin": models.get_admin_session(request),
        "city": models.get_city_by_name_model(city_name),
        "hall": models.get_hall_by_name_model(hall_name),
        "cities": models.get_cities_model(request),
    }
    return render(request, 'admin/admin_city_halls_info.html', context)


