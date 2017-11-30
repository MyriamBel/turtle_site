from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth

@csrf_protect
def reg(request):
    args = {}
    args['form'] = UserCreationForm()
    if request.method == "POST":
        newuser_form = UserCreationForm(data=request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            username = newuser_form.cleaned_data['username']
            password = newuser_form.cleaned_data['password2']
            newuser = auth.authenticate(username=username, password=password)
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
            return render(request, 'register.html', args)
    else:
        return render(request, 'register.html', args)
