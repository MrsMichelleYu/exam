from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
import re
from django.db.models import Count
from .models import User, Organization

def index(request):
    return render(request,"belt_app/index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            new_first_name = request.POST["first_name"]
            new_last_name = request.POST["last_name"]
            new_email = request.POST["email"]
            new_password = request.POST["password"]
            hash1 = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            print(hash1)
            new_user = User.objects.create(first_name=new_first_name, last_name=new_last_name, email=new_email, password=hash1)
            messages.success(request,"You have sucessfully registered. Please Login")
            return redirect("/")

def login(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            user = User.objects.filter(email=request.POST['email'])
            print(user)
            if len(user) == 0: 
                messages.error(request,"Records do not match, please try again")
                return redirect('/')
            else:
                person = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(),person.password.encode()):
                    request.session['id'] = person.id
                    return redirect('/groups')
                else:
                    messages.error(request,"Records do not match, please try again")
                    return redirect('/')

def groups(request):
    if 'id' not in request.session:
        messages.error(request,"You must be logged in first")
        return redirect("/")
    else:
        this_user = User.objects.get(id=request.session['id'])
        sort = Organization.objects.annotate(q_count=Count('joined_by')) \
                                .order_by('-q_count')
        context = {
            "user" : this_user,
            "total_organizations": Organization.objects.all(),
            "sort": sort,
        }
        return render(request,"belt_app/dashboard.html", context)

def create(request):
    errors = Organization.objects.organization_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/groups')
    else:
        if request.method == "POST":
            new_name = request.POST['name']
            new_description = request.POST['description']
            this_user = User.objects.get(id=request.session['id'])
            new_organization = Organization.objects.create(name=new_name, description=new_description, created_by=this_user)
            new_organization.joined_by.add(this_user)
            return redirect('/groups')

def details(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_organization = Organization.objects.get(id=id)
    context = {
        "user" : this_user,
        "this_organization": Organization.objects.get(id=id),
        "all_members": this_organization.joined_by.all(),
    }
    return render(request,"belt_app/views.html", context)

def leave(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_organization = Organization.objects.get(id=id)
    this_organization.joined_by.remove(this_user)
    return redirect(f'/groups/{id}')

def join(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_organization = Organization.objects.get(id=id)
    this_organization.joined_by.add(this_user)
    return redirect(f'/groups/{id}')

def delete(request,id):
    this_organization = Organization.objects.get(id=id)
    this_organization.delete()
    return redirect ('/groups')

def logout(request):
    del request.session['id']
    return redirect("/")