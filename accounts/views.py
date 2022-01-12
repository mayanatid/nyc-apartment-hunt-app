from django.contrib import auth
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# registration
def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")

    # if they are not logged in
    else:
        if request.method == "POST":
            form = RegistrationFrom(request.POST or None)
            # check if form is valid
            if form.is_valid():
                user = form.save()

                # get raw password
                raw_password = form.cleaned_data.get('password1')

                # authenticate the user
                user = authenticate(username=user.username, password=raw_password)

                # Login the user
                login(request, user)

                return redirect("main:home")
        else:
            form = RegistrationFrom()
        return render(request, "accounts/register.html", {"form": form})

# login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    
    else:
        # if they are not logged in
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            # check credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main:home')
                else:
                    return render(request, 'accounts/login.html', {'error': "You have been logged out"})
            else:
                return render(request, 'accounts/login.html', {'error': "Invalid user name or password"})

        return render(request, 'accounts/login.html')

# logout
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("accounts:login")
    else:    
        return redirect("accounts:login")
    
