from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE_REGEX = re.compile(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email=postData["email"])
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be entered and should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must be entered and should be at least 2 characters"
        if not EMAIL_REGEX.match(postData["email"]): 
            errors["email"] = "Not a valid email address" 
        if len(check_email) > 0: 
            errors["email"] = "This email address already exists in the system" 
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be more than 8 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match"
        return errors

    def user_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email=postData["email"])
        if not EMAIL_REGEX.match(postData["email"]): 
            errors["email"] = "Not a valid email address" 
        if len(postData['email']) <= 0: 
            errors["email"] = "You must enter an email address" 
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be entered and needs to be more than 8 characters"
        return errors

class OrganizationManager(models.Manager):
    def organization_validator(self, postData):
        errors = {}
        if len(postData['name']) < 6: 
            errors['name'] = "Organization name must be provided and should be more than 5 characters"
        if len(postData['description']) < 11: 
            errors['description'] = "Description must be provided and should be more than 10 characters" 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_organizations")
    joined_by = models.ManyToManyField(User, related_name="joined_organizations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrganizationManager()