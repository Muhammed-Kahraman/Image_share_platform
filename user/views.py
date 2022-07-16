from django.contrib.messages.storage import session
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import RegisterForm, LoginFrom, ResetPasswordForm
import psycopg2
from django.contrib.auth.hashers import check_password, make_password

conn = psycopg2.connect(database="image_db", user='postgres', password='04mint35', host='127.0.0.1', port='5432')
cursor = conn.cursor()


# Create your views here.
def register(request):
    if not request.user.is_authenticated:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()

            login(request, new_user)
            messages.success(request, "You have successfully registered.")
            return redirect("index")
        context = {
            "form": form
        }
        return render(request, "authentication_process/register.html", context)
    else:
        messages.info(request, "For doing to register process first you have to logout!")
        return redirect("index")


def loginUser(request):
    if not request.user.is_authenticated:
        form = LoginFrom(request.POST or None)
        context = {
            "form": form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request, "Username or password is wrong!")
                return render(request, "authentication_process/login.html", context=context)
            messages.success(request, "You have successfully logged in.")
            login(request, user)
            return redirect("index")
        return render(request, "authentication_process/login.html", context=context)
    else:
        messages.info(request, "You already logged in to your account!")
        return redirect("index")


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(
            request, "You have successfully logout.")
        return redirect("index")
    else:
        messages.info(request, "For doing to logout process first you have to login!")


def reset_password(request):
    form = ResetPasswordForm(request.POST or None)
    context = {
        "form": form
    }
    cursor.execute("SELECT username from auth_user")
    usernames = [item[0] for item in cursor.fetchall()]
    print(usernames)
    if len(usernames) > 0:
        if form.is_valid():
            for username in usernames:
                if username == form.cleaned_data.get("username"):
                    cursor.execute("SELECT password from auth_user where username IN (username)")
                    password = [item[0] for item in cursor.fetchall()]
                    old_password = form.cleaned_data.get('old_password')
                    result = check_password(old_password, password[0])
                    print(result)
                    if result:
                        user = User.objects.get(username='{}'.format(form.cleaned_data.get("username")))
                        user.set_password(form.cleaned_data.get("password"))
                        user.save()
                        messages.success(request, "You have successfully reset your password.")
                        return redirect("index")
                    else:
                        messages.error(request, "Your old password is wrong. Enter again please!")
    else:
        messages.info(request, "Username or password is wrong!")
    return render(request, "authentication_process/reset_password.html", context=context)
