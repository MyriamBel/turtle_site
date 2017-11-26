# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse

@csrf_protect
def login(request):
    args = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')