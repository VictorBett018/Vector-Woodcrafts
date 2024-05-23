from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from django.contrib.auth.hashers import check_password
#User = settings.AUTH_USER_MODEL
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully")
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])

            login(request, new_user)
            return redirect ('index')

    else:
        print("user cannot be registered")
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email = email)
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('index')

            else:
                messages.warning(request, "Invalid email or password")

        except:
            messages.warning (request, f"User with {email} does not exist")

        

    context = {
       
    }

    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    return redirect('index')

def change_password_view(request):
    user = request.user
    if request.method=='POST':
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        if confirm_new_password != new_password:
            messages.error(request,"Passwords does not match")
            return redirect('change_password')

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successully!")
            return redirect('change_password')

        else:
            messages.error(request, "old password is incorrect!")
            return redirect('change_password')

    return render(request, "userauths/change_password.html")
            

