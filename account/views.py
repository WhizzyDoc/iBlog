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
from django.utils import timezone


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
                        #print("user created")
                        # create a new profile for user
                        api_key = generate_token()
                        profile = Profile(user=new_user, firstName=firstName, lastName=lastName, email=email, phone_number=phoneNumber, api_key=api_key)
                        profile.save()
                        plan = Plan.objects.get(level=1)
                        profile.plan = plan
                        profile.save()
                        BlogCategory.objects.create(owner=profile, title="Uncategorized", slug="uncategorized")
                        send_new_account_email(email, firstName)
                        #print("profile created")
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
    sites = Site.objects.filter(owner=profile)
    return render(request, "owner/base/index.html", {
        'profile': profile,
        'sites': sites,
    })

@login_required(login_url="login")
@csrf_protect
def pricing(request):
    profile = Profile.objects.get(user=request.user)
    sites = Site.objects.filter(owner=profile)
    plans = Plan.objects.all()
    if request.method == "POST":
        plan_id = request.POST.get('plan_id')
        plan = Plan.objects.get(id=plan_id)
        if profile.plan.level == plan.level:
            messages.warning(request, f"You are already on {plan.title} plan.")
            return redirect('pricing')
        state = ""
        if profile.plan.level < plan.level:
            state = "upgraded"
        elif profile.plan.level > plan.level:
            state = "downgraded"
        profile.plan = plan
        profile.save()
        deadline = '-'
        if plan.level > 1: 
            profile.deadline = timezone.now() + timezone.timedelta(days=30)
            profile.save()
            deadline = profile.deadline.strftime("%Y-%m-%d %H:%M:%S")
        else:
            profile.deadline = None
            profile.save()
        note = f"""
        Your account has been successfully {state} to {plan.title} plan. Your plan expires on {deadline}
        """
        Notification.objects.create(owner=profile, title=f"Account {state}", note=note)
        messages.success(request, f"Your account has been successfully {state} to {plan.title} plan. Your plan expires on {deadline}")
        
        return redirect('pricing')
    return render(request, "owner/base/pricing.html", {
        'profile': profile,
        'sites': sites,
        'plans': plans,
    })

@login_required(login_url="login")
def create_site(request):
    profile = Profile.objects.get(user=request.user)
    sites = Site.objects.filter(owner=profile)
    return render(request, f"owner/site/create_site.html", {
        'sites': sites,
        'profile': profile,
    })
        

@login_required(login_url="login")
def edit_site(request, slug):
    profile = Profile.objects.get(user=request.user)
    sites = Site.objects.filter(owner=profile)
    site = Site.objects.get(owner=profile, slug=slug.lower())
    return render(request, 'owner/site/edit_site.html', {
        'profile': profile,
        'sites': sites,
        'site': site,
    })

@login_required(login_url="login")
def template_list(request):
    profile = Profile.objects.get(user=request.user)
    categories = TemplateCategory.objects.all()
    sites = Site.objects.filter(owner=profile)
    return render(request, "owner/templates/template_list.html", {
        'profile': profile,
        'sites': sites,
        'categories': categories,
    })

@login_required(login_url="login")
def blog_list(request, slug):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug.lower())
    sites = Site.objects.filter(owner=profile)
    return render(request, "owner/blog/blog-list.html", {
        'profile': profile,
        'sites': sites,
        'site': site,
    })

@login_required(login_url="login")
def add_blog(request, slug):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug.lower())
    sites = Site.objects.filter(owner=profile)
    tags = Tag.objects.filter(owner=profile)
    categories = BlogCategory.objects.filter(owner=profile)
    return render(request, "owner/blog/add-blog.html", {
        'profile': profile,
        'site': site,
        'sites': sites,
        'tags': tags,
        'categories': categories
    })

@login_required(login_url="login")
def edit_blog(request, slug, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug.lower())
    sites = Site.objects.filter(owner=profile)
    blog = Blog.objects.get(id=int(id), author=profile, site=site)
    tags = Tag.objects.filter(owner=profile)
    categories = BlogCategory.objects.filter(owner=profile)
    return render(request, "owner/blog/edit-blog.html", {
        'profile': profile,
        'site': site,
        'sites': sites,
        'blog': blog,
        'tags': tags,
        'categories': categories
    })
    
@login_required(login_url="login")
@csrf_protect
def delete_blog(request, slug, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug.lower())
    if request.method == 'POST':
        try:
            blog = Blog.objects.get(id=id, author=profile, site=site)
            blog.delete()
            messages.success(request, f"Post \'{blog.title}\' deleted successfully")
            return redirect('blog_list', site.slug)
        except:
            messages.warning(request, "Post does not exist anymore")
            return redirect('blog_list', site.slug)
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('blog_list', site.slug)


@login_required(login_url="login")
def blog_category_list(request):
    profile = Profile.objects.get(user=request.user)
    sites = Site.objects.filter(owner=profile)
    categories = BlogCategory.objects.filter(owner=profile)
    return render(request, "owner/category/category-list.html", {
        'profile': profile,
        'sites': sites,
        'categories': categories
    })

@login_required(login_url="login")
@csrf_protect
def delete_blog_category(request, id):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            cat = BlogCategory.objects.get(id=id, owner=profile)
            cat.delete()
            messages.success(request, f"Category \'{cat.title}\' deleted successfully")
            return redirect('blog_category_list')
        except:
            messages.warning(request, "Category does not exist anymore")
            return redirect('blog_category_list')
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('blog_category_list')

@login_required(login_url="login")
def blog_tag_list(request):
    profile = Profile.objects.get(user=request.user)
    sites = Site.objects.filter(owner=profile)
    tags = Tag.objects.filter(owner=profile)
    return render(request, "owner/tag/tag-list.html", {
        'profile': profile,
        'sites': sites,
        'tags': tags,
    })
    
@login_required(login_url="login")
@csrf_protect
def delete_blog_tag(request, id):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            tag = Tag.objects.get(id=id, owner=profile)
            tag.delete()
            messages.success(request, f"Tag \'{tag.title}\' deleted successfully")
            return redirect('blog_tag_list')
        except:
            messages.warning(request, "Tag does not exist anymore")
            return redirect('blog_tag_list')
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('blog_tag_list')

@login_required(login_url="login")
def message_list(request, slug):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    sites = Site.objects.filter(owner=profile)
    return render(request, "owner/message/message-list.html", {
        'profile': profile,
        'sites': sites,
        'site': site,
    })

@login_required(login_url="login")
def edit_message(request, slug, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    sites = Site.objects.filter(owner=profile)
    message = Contact.objects.get(id=int(id), site=site)
    return render(request, "owner/message/edit-message.html", {
        'profile': profile,
        'site': site,
        'sites': sites,
        'message': message,
    })
    
@login_required(login_url="login")
@csrf_protect
def delete_message(request, slug, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    if request.method == 'POST':
        try:
            message = Contact.objects.get(id=id, site=site)
            message.delete()
            messages.success(request, f"{message.name}\'s message deleted successfully")
            return redirect('message_list', site.slug)
        except:
            messages.warning(request, "Message does not exist anymore")
            return redirect('message_list', site.slug)
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('message_list', site.slug)

@login_required(login_url="login")
def comment_list(request, slug, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    sites = Site.objects.filter(owner=profile)
    blog = Blog.objects.get(id=int(id))
    return render(request, "owner/comment/comment-list.html", {
        'profile': profile,
        'sites': sites,
        'site': site,
        'blog': blog,
    })

@login_required(login_url="login")
def edit_comment(request, slug, blog_id, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    sites = Site.objects.filter(owner=profile)
    blog = Blog.objects.get(id=int(blog_id))
    comment = Comment.objects.get(id=int(id), blog=blog)
    return render(request, "owner/comment/edit-comment.html", {
        'profile': profile,
        'site': site,
        'sites': sites,
        'comment': comment,
        'blog': blog,
    })
    
@login_required(login_url="login")
@csrf_protect
def delete_comment(request, slug, blog_id, id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(owner=profile, slug=slug)
    blog = Blog.objects.get(id=int(blog_id))
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=int(id), blog=blog)
            comment.delete()
            messages.success(request, f"{comment.name}\'s comment deleted successfully")
            return redirect('comment_list', site.slug, blog.id)
        except:
            messages.warning(request, "Comment does not exist anymore")
            return redirect('comment_list', site.slug, blog.id)
    else:
        messages.warning(request, "Unauthorized request method")
        return redirect('comment_list', site.slug, blog.id)
        
