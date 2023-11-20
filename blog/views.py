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
def home(request, slug):
    try:
        site = Site.objects.get(slug=slug)
        profile = site.owner
        if site is not None:
            if site.template:
                latest_posts = Blog.objects.filter(author=profile, status="Published")[:4]
                featured_posts = Blog.objects.filter(author=profile, status="Published", featured=True)
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
                

def blog_list(request, title):
    pass
