from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *

def go_index(request):
    if 'loggedIn_id' in request.session:
        return redirect(reverse('go_dashboard'))
    return render(request, 'examRetake_python/index.html')

def go_login(request):
    if 'loggedIn_id' in request.session:
        return redirect(reverse('go_dashboard'))
    return render(request, 'examRetake_python/login.html')

def go_register(request):
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

def go_dashboard(request):
    if 'loggedIn_id' in request.session:
        usr_id = request.session['loggedIn_id']
        context = {
            'usr': User.objects.get(id=usr_id),
            'usr_trps': Trip.objects.filter(joined_by=usr_id),
            'notUsr_trps': Trip.objects.all().exclude(joined_by=usr_id)
        }
        return render(request, 'examRetake_python/tripDashboard.html', context)
    else:
        return redirect('go_login')

def processLogout(request):
    request.session.clear()
    return redirect(reverse('go_startpage'))

def go_addTrip(request):
    if 'loggedIn_id' in request.session:
        usr_id = request.session['loggedIn_id']
        context = User.objects.values().get(id=usr_id)
        return render(request, 'examRetake_python/addaTrip.html', context)
    else:
        return redirect(reverse('go_login'))

def go_tripDetails(request, id):
    if 'loggedIn_id' in request.session:
        usr_id = request.session['loggedIn_id']
        trp_id = id
        context = {
            'usr': User.objects.get(id=usr_id),
            'trp': Trip.objects.filter(id=trp_id)[0],
            'trp_usrs': User.objects.filter(usersJoiningThisTrip=trp_id).exclude(id=Trip.objects.get(id=trp_id).created_by.id)
        }
        return render(request, 'examRetake_python/tripDetails.html', context)
    else:
        return redirect(reverse('go_login'))

def processNewTrip(request):
    errors = Trip.objects.tripDetails_validator(request.POST)
    if 'success' in errors:
        Trip.objects.trip_adder(request.POST, request.session['loggedIn_id'])
        return redirect('go_dashboard')
    for key, value in errors.items():
        messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_addTrip'))

def processDeleteTrip(request, id):
    tripToDelete = Trip.objects.get(id = id)
    tripToDelete.delete()
    return redirect(reverse('go_dashboard'))

def processCancelTrip(request, id):
    joinToDelete = Trip.objects.get(id=id).joined_by.remove(User.objects.get(id=request.session['loggedIn_id']))
    return redirect(reverse('go_dashboard'))

def processJoinTrip(request, id):
    Trip.objects.get(id=id).joined_by.add(User.objects.get(id=request.session['loggedIn_id']))
    return redirect(reverse('go_dashboard'))

def go_editUser(request, id):
    if 'loggedIn_id' in request.session:
        usr_id = id
        context = {
            'usr': User.objects.get(id=usr_id)
        }
        return render(request, 'examRetake_python/editUser.html', context)
    else:
        return redirect(reverse('go_login'))

def processUserUpdate(request, id):
    errors = User.objects.validateUpdate(request.POST)
    if 'success' in errors:
        temp = User.objects.get(id=id)
        if 'first_name' in request.POST:
            temp.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            temp.last_name = request.POST['last_name']
        if 'email_address' in request.POST:
            temp.email_address = request.POST['email_address']
        temp.save()
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    else:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_editUser', kwargs={'id': id }))

def go_editTrip(request, id):
    if 'loggedIn_id' in request.session:
        usr_id = request.session['loggedIn_id']
        context = {
            'usr': User.objects.get(id=usr_id),
            'trp': Trip.objects.get(id=id)
        }
        return render(request, 'examRetake_python/editTrip.html', context)
    else:
        return redirect(reverse('go_login'))

def processTripUpdate(request, id):
    errors = Trip.objects.validateUpdate(request.POST)
    if 'success' in errors:
        temp = Trip.objects.get(id=id)
        if 'destination' in request.POST:
            temp.destination = request.POST['destination']
        if 'description' in request.POST:
            temp.description = request.POST['description']
        if 'date_from' in request.POST:
            temp.date_from = request.POST['date_from']
        if 'date_to' in request.POST:
            temp.date_to = request.POST['date_to']
        temp.save()
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    else:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    return redirect(reverse('go_editTrip', kwargs={'id': id }))