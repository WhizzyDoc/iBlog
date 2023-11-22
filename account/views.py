from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
from blog.models import *
from .utils import *
import datetime
from django.views.decorators.http import require_POST
import re
import json
import random
import math
from django.db.models import Q
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def custom_404(request, exception):
    return render(request, 'user/404.html', status=404)

# Create your views here.
@csrf_exempt
def admin_login(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        username = sterilize(request.POST.get('username'))
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': 'success',})
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': "Your account has been disabled",
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': "Invalid login credentials",
            })
    return render(request, "owner/base/admin-login.html")

@csrf_protect
def register(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if username and email does not exist
        if is_valid_email(email):
            if is_valid_username(username):
                if is_valid_password(password):
                    usernames = []
                    emails = []
                    users = User.objects.all()
                    for user in users:
                        usernames.append(user.username)
                        emails.append(user.email)
                    if username not in usernames and email not in emails:
                        # create new user
                        new_user = User(username=username, email=email, first_name=firstName, last_name=lastName)
                        new_user.set_password(password)
                        new_user.save()
                        print("user created")
                        # create a new profile for user
                        api_key = generate_token()
                        profile = Profile(user=new_user, firstName=firstName, lastName=lastName, email=email, phone_number=phoneNumber, api_key=api_key)
                        profile.save()
                        print("profile created")
                        # return success status
                        return JsonResponse({
                            'status': 'success',
                            'username': username,
                            'email': email,
                        })
                    elif username in usernames:
                        return JsonResponse({
                            'status': 'error',
                            'message': f"Username already exists. Kindly use another username such as {username}123.",
                        })
                    elif email in emails:
                        return JsonResponse({
                            'status': 'error',
                            'message': f"Email {email} has already been used. Kindly use another email.",
                        })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'reason': f"Invalid Password. password must be at least 8 characters long and contain alphabets and digits",
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'reason': f"Invalid Username. Username can only contain letters and numbers",
                })
        else:
            return JsonResponse({
                'status': 'error',
                'reason': f"Invalid Email",
            })
    return render(request, 'owner/base/register.html')

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.warning(request, "You have been logged out, enter your details to log back in")
    return redirect('login')

@login_required(login_url="login")
def index(request):
    profile = Profile.objects.get(user=request.user)
    try:
        site = Site.objects.get(owner=profile)
        return render(request, "owner/base/index.html", {
            'profile': profile,
            'site': site
        })
    except:
        return render(request, "owner/base/index.html", {
            'profile': profile
        })

@login_required(login_url="login")
def create_site(request):
    profile = Profile.objects.get(user=request.user)
    try:
        site = Site.objects.get(owner=profile)
        return render(request, f"error_404.html", {
            'site': site,
        })
    except Site.DoesNotExist:
        return render(request, 'owner/site/create_site.html', {
            'profile': profile,
        })
        

@login_required(login_url="login")
def edit_site(request):
    profile = Profile.objects.get(user=request.user)
    try:
        site = Site.objects.get(owner=profile)
        return render(request, 'owner/site/edit_site.html', {
            'profile': profile,
            'site': site,
        })
    except Site.DoesNotExist:
        return render(request, f"error_404.html")

@login_required(login_url="login")
def template_list(request):
    profile = Profile.objects.get(user=request.user)
    templates = Template.objects.all()
    if request.method == "GET":
        query = request.GET.get('query')
        if query:
            templates = Template.objects.filter(title__icontains=query)
    try:
        site = Site.objects.get(owner=profile)
        return render(request, "owner/templates/template_list.html", {
            'profile': profile,
            'site': site,
            'templates': templates,
        })
    except:
        return render(request, "owner/templates/template_list.html", {
            'profile': profile,
            'templates': templates
        })

@login_required(login_url="login")
def blog_list(request):
    profile = Profile.objects.get(user=request.user)
    try:
        site = Site.objects.get(owner=profile)
        return render(request, "owner/blog/blog-list.html", {
            'profile': profile,
            'site': site
        })
    except:
        return render(request, "owner/blog/blog-list.html", {
            'profile': profile
        })

@login_required(login_url="login")
def add_blog(request):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile)
    tags = Tag.objects.filter(owner=profile)
    categories = BlogCategory.objects.filter(owner=profile)
    return render(request, "owner/blog/add-blog.html", {
        'profile': profile,
        'site': site,
        'tags': tags,
        'categories': categories
    })

@login_required(login_url="login")
def edit_blog(request, id):
    profile = Profile.objects.get(user=request.user)
    blog = Blog.objects.get(id=int(id), author=profile)
    tags = Tag.objects.filter(owner=profile)
    categories = BlogCategory.objects.filter(owner=profile)
    site = Site.objects.get(owner=profile)
    return render(request, "owner/blog/edit-blog.html", {
        'profile': profile,
        'site': site,
        'blog': blog,
        'tags': tags,
        'categories': categories
    })
    
@login_required(login_url="login")
@csrf_protect
def delete_blog(request, id):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            blog = Blog.objects.get(id=id, author=profile)
            blog.delete()
            messages.success(request, f"Post \'{blog.title}\' deleted successfully")
            return redirect('blog_list')
        except:
            messages.warning(request, "Post does not exist anymore")
            return redirect('blog_list')
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('blog_list')
        