from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        inLogin = False

        if 'first_name' not in postData:
            inLogin = True
        if inLogin:
            if not EMAIL_REGEX.match(postData['email_address'].strip().lower()):
                errors["email_address"] = "Invalid email address, please try again. "
            if len(postData['password'].strip()) < 8:
                errors["password"] = "Invalid password, please try again. "

        if len(errors) == 0:
            currentEmail = postData['email_address'].strip()
            savedUser = User.objects.filter(email_address = currentEmail)
            if not savedUser:
                errors['email_address'] = "That email_address is not registered. "
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
                errors["first_name"] = "First name should be at least 2 characters. "
            if len(postData['last_name'].strip()) < 2:
                errors["last_name"] = "Last name should be at least 2 characters. "
            if not EMAIL_REGEX.match(postData['email_address'].strip().lower()):
                errors['email_address'] = "Invalid email_address. "
            if len(postData['password'].strip()) < 8:
                errors["password"] = "Password should be at least 8 characters. "
            if postData['conf_password'].strip() != postData['password'].strip():
                errors['conf_password'] = "Passwords do not match. "

        if len(errors) == 0:
            currentEmail = postData['email_address']
            if User.objects.filter(email_address = currentEmail):
                errors['email_address'] = "That email_address is already registered, please login. "
            else:
                tempHash = bcrypt.hashpw(postData['password'].strip().encode(), bcrypt.gensalt())
                tempUser = User.objects.create(first_name=postData['first_name'].strip(), last_name=postData['last_name'].strip(), email_address=postData['email_address'].strip().lower(), password=tempHash)
                errors['success'] = "Successfully registered. "

        return errors

    def validateUpdate(self, postData):
        errors = {}
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

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {} 
        if len(postData['author'].strip()) < 1:
            errors["author"] = "Please type in a valid author name. "
        if len(postData['new_quote'].strip()) < 1:
            errors["new_quote"] = "Please type in a valid quote. "
        if len(errors) == 0:
            errors['success'] = "Successfully created and added. "
        return errors

    def quote_adder(self, postData, id):
        newQuote = Quote.objects.create(author=postData['author'].strip(), quote_content=postData['new_quote'].strip(), created_by=User.objects.filter(id=id)[0])

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, related_name = "quotesByUser", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name = "likesByUser")

    # Overidding the objects attribute value
    objects = QuoteManager()