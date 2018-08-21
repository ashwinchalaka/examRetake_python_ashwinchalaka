from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *

def index(request):
    if 'loggedIn_id' in request.session:
        return redirect(reverse('go_dashboard'))
    return render(request, 'examRetake_python/index.html')

def login(request):
    if 'loggedIn_id' in request.session:
        return redirect(reverse('go_dashboard'))
    return render(request, 'examRetake_python/login.html')

def register(request):
    if 'loggedIn_id' in request.session:
        return redirect(reverse('go_dashboard'))
    return render(request, 'examRetake_python/register.html')

def processRegistration(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_register'))

def processLogin(request):
    errors = User.objects.login_validator(request.POST)
    if 'loginsuccess' in errors:
        savedUser = errors['loginsuccess']
        request.session['loggedIn_id'] = savedUser.values()[0]['id']
        return redirect(reverse('go_dashboard'))
    else:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_login'))

def dashboard(request):
    if 'loggedIn_id' in request.session:
        context = {
            'usr': User.objects.get(id=request.session['loggedIn_id']),
            'qts': Quote.objects.all()
        }
        return render(request, 'examRetake_python/quoteDashboard.html', context)
    else:
        return redirect('go_login')

def processLogout(request):
    request.session.clear()
    return redirect(reverse('go_startpage'))

def processQuote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if 'success' in errors:
        Quote.objects.quote_adder(request.POST, request.session['loggedIn_id'])
    for key, value in errors.items():
        messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_login'))

def deleteQuote(request, id):
    quoteToDelete = Quote.objects.get(id = id)
    quoteToDelete.delete()
    return redirect(reverse('go_login'))

def showUser(request, id):
    if 'loggedIn_id' in request.session:
        context = {
            'qts': Quote.objects.filter(created_by=id),
            'author': User.objects.get(id=id),
        }
        return render(request, 'examRetake_python/userQuotes.html', context)
    else:
        return redirect(reverse('go_login'))

def editUser(request, id):
    if 'loggedIn_id' in request.session:
        context = User.objects.values().get(id=id)
        return render(request, 'examRetake_python/editUser.html', context)
    else:
        return redirect(reverse('go_login'))

def processUpdate(request, id):
    temp = User.objects.get(id=id)
    if 'first_name' in request.POST:
        temp.first_name = request.POST['first_name']
    if 'last_name' in request.POST:
        temp.last_name = request.POST['last_name']
    if 'email_address' in request.POST:
        temp.email = request.POST['email_address']
    temp.save()
    return redirect(reverse('editUser', kwargs={'id': id }))

def addLike(request, id):
    Quote.objects.get(id=id).liked_by.add(User.objects.get(id=request.session['loggedIn_id']))
    return redirect(reverse('go_dashboard'))