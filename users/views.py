from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from users.forms import SignUpForm, LoginForm
from users.models import UserProfile


def register_user(request):
    msg = None
    success = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            organization = form.cleaned_data.get("organization")
            user = authenticate(username=username, password=raw_password)

            UserProfile.objects.create(user=user, organization=organization, permission=form.cleaned_data['permission'])
            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/")
            # user = form.save(commit=False)  # Don't save the User instance yet
            # user.set_password(form.cleaned_data['password'])  # Manually set the password
            # user.save()  # Now you can save the User instance
            # return redirect('login')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'pages/sign-up.html', {'form': form, "msg": msg, "success": success})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "pages/sign-in.html", {"form": form, "msg": msg})
