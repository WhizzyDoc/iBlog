from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
from account.models import *
import datetime
from django.views.decorators.http import require_POST
import re
import json
import random
import math
from django.db.models import Q
import requests

# Create your views here.
def home_page(request):
    developers = Developer.objects.all()
    try:
        site = MainSite.objects.first()
        return render(request, 'owner/base/home.html', {
            'site': site,
            'developers': developers,
        })
    except:
        return render(request, 'owner/base/home.html', {
            'developers': developers,
        })

def home(request, slug):
    try:
        site = Site.objects.get(slug=slug)
        profile = site.owner
        if site is not None:
            if site.template:
                latest_posts = Blog.objects.filter(author=profile, status="Published")[:4]
                featured_posts = Blog.objects.filter(author=profile, status="Published")[:5]
                return render(request, f"{site.template.title}/index.html", {
                    'site': site,
                    'profile': profile,
                    'latest_posts': latest_posts,
                    'featured_posts': featured_posts
                })
            else:
                return render(request, f"error_build.html", {
                    'site': site
                })
        else:
            return render(request, f"error_404.html")
    except:
        return render(request, f"error_404.html")
                

def blog_list(request, slug, page=1):
    try:
        site = Site.objects.get(slug=slug)
        profile = site.owner
        if site is not None:
            if site.template:
                per_page = 5
                if page is None:
                    page = 1
                else:
                    page = int(page)
                start = (page - 1) * per_page
                stop = page * per_page
                blogs = None
                total_items = 0
                q = request.GET.get('q')
                query = ""
                if q:
                    query = q
                total_items = Blog.objects.filter(author=profile, status="Published").filter(Q(title__icontains=query) |
                                                                                             Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, status="Published").filter(Q(title__icontains=query) |
                                                                                        Q(post__icontains=query))[start:stop]
                total_pages = math.ceil(total_items/per_page)
                if blogs.exists():
                    return render(request, f"{site.template.title}/blogs.html", {
                        'site': site,
                        'profile': profile,
                        'blogs': blogs,
                        'page': page,
                        'total_pages': total_pages,
                        'total_blogs': total_items,
                        'query': query
                    })
                else:
                    return render(request, f"{site.template.title}/blogs.html", {
                        'site': site,
                        'profile': profile,
                        'page': page,
                        'total_pages': total_pages,
                        'total_blogs': total_items,
                        'query': query
                    })
            else:
                return render(request, f"error_build.html", {
                    'site': site
                })
        else:
            return render(request, f"error_404.html")
    except:
        return render(request, f"error_404.html")

def filter_blogs(request, slug, type, type_slug, page=1):
    try:
        site = Site.objects.get(slug=slug)
        profile = site.owner
        if site is not None:
            if site.template:
                per_page = 5
                if page is None:
                    page = 1
                else:
                    page = int(page)
                start = (page - 1) * per_page
                stop = page * per_page
                blogs = None
                total_items = 0
                q = request.GET.get('q')
                query = ""
                if q:
                    query = q
                if type == 'categories':
                    category = BlogCategory.objects.get(slug=type_slug, owner=profile)
                    total_items = Blog.objects.filter(author=profile, category=category, status="Published").filter(Q(title__icontains=query) |
                                                                                             Q(post__icontains=query)).count()
                    blogs = Blog.objects.filter(author=profile, category=category, status="Published").filter(Q(title__icontains=query) |
                                                                                        Q(post__icontains=query))[start:stop]
                elif type == 'tags':
                    tag = Tag.objects.get(slug=type_slug, owner=profile)
                    total_items = Blog.objects.filter(author=profile, tags=tag, status="Published").filter(Q(title__icontains=query) |
                                                                                             Q(post__icontains=query)).count()
                    blogs = Blog.objects.filter(author=profile, tags=tag, status="Published").filter(Q(title__icontains=query) |
                                                                                        Q(post__icontains=query))[start:stop]
                total_pages = math.ceil(total_items/per_page)
                if blogs.exists():
                    return render(request, f"{site.template.title}/blogs.html", {
                        'site': site,
                        'profile': profile,
                        'blogs': blogs,
                        'page': page,
                        'total_pages': total_pages,
                        'total_blogs': total_items,
                        'query': query,
                        'type': type,
                        'type_slug': type_slug
                    })
                else:
                    return render(request, f"{site.template.title}/blogs.html", {
                        'site': site,
                        'profile': profile,
                        'page': page,
                        'total_pages': total_pages,
                        'total_blogs': total_items,
                        'query': query,
                        'type': type,
                        'type_slug': type_slug
                    })
            else:
                return render(request, f"error_build.html", {
                    'site': site
                })
        else:
            return render(request, f"error_404.html")
    except:
        return render(request, f"error_404.html")

@csrf_protect
def blog_detail(request, slug, post_slug):
    site = Site.objects.get(slug=slug)
    profile = site.owner
    if site is not None:
        if site.template:
            blog = Blog.objects.get(slug=post_slug, author=profile, site=site)
            similar_posts = Blog.objects.exclude(slug=post_slug).filter(category=blog.category)[:5]
            if request.method == 'POST':
                name = request.POST.get('name')
                comment = request.POST.get('comment')
                new_comment = Comment(name=name, comment=comment, blog=blog)
                new_comment.save()
                return redirect('blog_detail', slug, post_slug)
            return render(request, f"{site.template.title}/blog-details.html", {
                'site': site,
                'profile': profile,
                'post': blog,
                'similar_posts': similar_posts    
            })
        else:
            return render(request, f"error_build.html")
    else:
        return render(request, f"error_404.html")

@csrf_protect
def contact(request, slug):
    site = Site.objects.get(slug=slug)
    profile = site.owner
    if site is not None:
        if site.template:
            if request.method == 'POST':
                name = request.POST.get('name')
                email = request.POST.get('email')
                message = request.POST.get('message')
                new_contact = Contact(name=name, email=email, message=message, site=site)
                new_contact.save()
                messages.success(request, "Your message has been submitted!")
                return redirect('contact', slug)
            return render(request, f"{site.template.title}/contact.html", {
                'site': site,
                'profile': profile, 
            })
        else:
            return render(request, f"error_build.html")
    else:
        return render(request, f"error_404.html")

def about(request, slug):
    site = Site.objects.get(slug=slug)
    profile = site.owner
    if site is not None:
        if site.template:
            return render(request, f"{site.template.title}/about.html", {
                'site': site,
                'profile': profile, 
            })
        else:
            return render(request, f"error_build.html")
    else:
        return render(request, f"error_404.html")

        
