from __future__ import unicode_literals
from django.db import models
import re, bcrypt, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        inLogin = False

        if 'first_name' not in postData:
            inLogin = True
        if inLogin:
            if not EMAIL_REGEX.match(postData['email_address'].strip().lower()):
                errors["email_address"] = "Invalid email address, please try again."
            if len(postData['password'].strip()) < 8:
                errors["password"] = "Invalid password, please try again."

        if len(errors) == 0:
            currentEmail = postData['email_address'].strip()
            savedUser = User.objects.filter(email_address = currentEmail)
            if not savedUser:
                errors['email_address'] = "That email_address is not registered."
            else:
                passToMatch = bcrypt.checkpw(postData['password'].strip().encode(), savedUser.values()[0]['password'].encode())
                if passToMatch:
                    errors['loginsuccess'] = savedUser
        return errors

    def registration_validator(self, postData):
        errors = {}
        inRegistration = False

        if 'first_name' in postData:
            inRegistration = True
        if inRegistration:
            if len(postData['first_name'].strip()) < 2:
                errors["first_name"] = "First name should be at least 2 characters."
            if len(postData['last_name'].strip()) < 2:
                errors["last_name"] = "Last name should be at least 2 characters."
            if not EMAIL_REGEX.match(postData['email_address'].strip().lower()):
                errors['email_address'] = "Invalid email_address. "
            if len(postData['password'].strip()) < 8:
                errors["password"] = "Password should be at least 8 characters."
            if postData['conf_password'].strip() != postData['password'].strip():
                errors['conf_password'] = "Passwords do not match. "

        if len(errors) == 0:
            currentEmail = postData['email_address']
            if User.objects.filter(email_address = currentEmail):
                errors['email_address'] = "That email_address is already registered, please login."
            else:
                tempHash = bcrypt.hashpw(postData['password'].strip().encode(), bcrypt.gensalt())
                tempUser = User.objects.create(first_name=postData['first_name'].strip(), last_name=postData['last_name'].strip(), email_address=postData['email_address'].strip().lower(), password=tempHash)
                errors['success'] = "Successfully registered. "

        return errors

    def validateUpdate(self, postData):
        errors = {}
        inUpdate = False

        if 'first_name' in postData:
            inUpdate = True
        if inUpdate:
            if len(postData['first_name'].strip()) < 2:
                errors["first_name"] = "First name should be at least 2 characters."
            if len(postData['last_name'].strip()) < 2:
                errors["last_name"] = "Last name should be at least 2 characters."
            if not EMAIL_REGEX.match(postData['email_address'].strip().lower()):
                errors['email_address'] = "Invalid email_address. "

        if len(errors) == 0:
            currentEmail = postData['email_address']
            if User.objects.filter(email_address = currentEmail):
                errors['email_address'] = "That email address is already registered, please choose a different email address."
            else:
                errors['success'] = "Successfully updated account details."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # Overidding the objects attribute value
    objects = UserManager()

class TripManager(models.Manager):

    def tripDetails_validator(self, postData):
        errors = {} 
        
        inAddTrip = False

        if 'destination' in postData:
            inAddTrip = True
            
        if inAddTrip:
            currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
            arrivalDate = postData['date_from']
            departureDate = postData['date_to']
            
            try: 
                datetime.datetime.strptime(arrivalDate, '%Y-%m-%d')
            except ValueError:
                errors['arrivalDate'] = "Please type in a valid arrival date."

            try:
                datetime.datetime.strptime(departureDate, '%Y-%m-%d')
            except ValueError: 
                errors['departureDate'] = "Please type in a valid departure date."


            if len(postData['destination'].strip()) < 1:
                errors["destination"] = "Please type in a valid destination."
            if len(postData['description'].strip()) < 1:
                errors["description"] = "Please type in a valid description."

            if arrivalDate < currentDate:
                errors["arrivalDate"] = "Please type in a valid arrival date."
            if departureDate < currentDate:
                errors["departureDate"] = "Please type in a valid departure date."

            if arrivalDate > departureDate:
                errors["arrivalDate"] = "Please type in a valid arrival date."
                errors["departureDate"] = "Please type in a valid departure date."
            
            if not errors:
                errors['success'] = "Trip added successfully. Add another trip?"

        return errors

    def trip_adder(self, postData, id):
        newTrip = Trip.objects.create(destination=postData['destination'].strip(), description=postData['description'].strip(), arrivalDate=postData['date_from'], departureDate=postData['date_to'], created_by=User.objects.get(id=id))
        tripId = newTrip.id
        Trip.objects.get(id=tripId).joined_by.add(User.objects.get(id=id))

    def validateUpdate(self, postData):
        errors = {}
        inUpdate = False

        if 'destination' in postData:
            inUpdate = True

        if inUpdate:
            currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
            arrivalDate = postData['date_from']
            departureDate = postData['date_to']
            
            try: 
                datetime.datetime.strptime(arrivalDate, '%Y-%m-%d')
            except ValueError:
                errors['arrivalDate'] = "Please type in a valid destination."

            try:
                datetime.datetime.strptime(departureDate, '%Y-%m-%d')
            except ValueError: 
                errors['departureDate'] = "Please type in a valid description."

            if len(postData['destination'].strip()) < 1:
                errors["destination"] = "First name should be at least 1 characters."
            if len(postData['description'].strip()) < 1:
                errors["last_name"] = "Last name should be at least 1 characters."

            if arrivalDate < currentDate:
                errors["arrivalDate"] = "Please type in a valid arrival date."
            if departureDate < currentDate:
                errors["departureDate"] = "Please type in a valid departure date."

            if arrivalDate > departureDate:
                errors["arrivalDate"] = "Please type in a valid arrival date."
                errors["departureDate"] = "Please type in a valid departure date."
            

        if len(errors) == 0:
            errors['success'] = "Successfully updated trip details."

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    arrivalDate = models.DateField(auto_now_add = False)
    departureDate = models.DateField(auto_now_add = False)
    created_by = models.ForeignKey(User, related_name = "tripsForThisUser", on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name = "usersJoiningThisTrip")

    # Overidding the objects attribute value
    objects = TripManager()