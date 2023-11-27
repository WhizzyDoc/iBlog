from rest_framework import generics, viewsets
from ..models import *
from blog.models import *
from .serializers import *
from ..utils import *
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate, logout
import secrets
import re
import json
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
import random
import decimal
import math
import string

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False,
            methods=['get'])
    def get_user_sites(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        try:
            sites = Site.objects.filter(owner=profile)
            if sites.exists():
                return Response({
                    'status': 'success',
                    'message': 'sites found',
                    'data': [SiteSerializer(s).data for s in sites]
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'You do not have any active site'
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error occured! please try again'
            })
    @action(detail=False,
            methods=['post'])
    def activate_site_template(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        site_id = request.POST.get('site_id')
        temp_id = request.POST.get('template_id')
        if site_id is not None and temp_id is not None:
            site = Site.objects.get(id=int(site_id), owner=profile)
            template = Template.objects.get(id=int(temp_id))
            if template.plan.level > profile.plan.level:
                return Response({
                    'status': 'error',
                    'message': f"{template.title} cannot be activated for your current plan. Kindly upgrade to {template.plan.title} Plan to activate",
                })
            site.template = template
            site.save()
            return Response({
                'status': 'success',
                'message': f"{template.title} successfully activated for {site.title}.",
            })
        else:
            return Response({
                'status': 'error',
                'message': f"{template.title} cannot be activated for your current plan. Kindly upgrade to {template.plan.title} Plan to activate",
            })
    @action(detail=False,
            methods=['post'])
    def edit_site(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('site_id')
        title = request.POST.get('title')
        tagline = request.POST.get('tagline')
        logo = request.FILES.get('logo')
        icon = request.FILES.get('icon')
        about = request.POST.get('about')
        description = request.POST.get('description')
        #tag_slugs = request.POST.getlist('tag_slugs', [])
        site = Site.objects.get(id=int(id), owner=profile)
        try:
            site.title = title
            site.tagline = tagline
            site.about = about
            site.description = description
            site.save()
            if logo is not None:
                site.logo = logo
                site.save()
            if icon is not None:
                site.icon = icon
                site.save()
            return Response({
                'status': 'success',
                'message': f"Site Info edited successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while editing site info"
            })
    @action(detail=False,
        methods=['post'])
    def create_site(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        title = request.POST.get('title')
        slug = slugify(title)
        tagline = request.POST.get('tagline')
        logo = request.FILES.get('logo')
        icon = request.FILES.get('icon')
        about = request.POST.get('about')
        description = request.POST.get('description')
        try:
            sites = Site.objects.filter(owner=profile)
            if sites.exists():
                if sites.count() >= profile.plan.site_number:
                    return Response({
                        'status': 'error',
                        'message': f"You cannot create more than {profile.plan.site_number}!"
                    })
            # check if the title does not exists
            for s in profile.site.all():
                if s.slug == slug:
                    return Response({
                        'status': 'error',
                        'message': f"title \'{title}\' already exists!"
                    })
                else:
                    pass
            #tags = Tag.objects.filter(slug__in=tag_slugs)
            new_site = Site(owner=profile, title=title, slug=slug, tagline=tagline,
                            description=description, about=about, logo=logo, icon=icon)
            new_site.save()
            Notification.objects.create(owner=profile, title=f"Site Creation", note=f"You created a new site \'{title}\'")
            return Response({
                'status': 'success',
                'message': f"New site created successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while creating site"
            })

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False,
            methods=['get'])
    def get_messages(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        query = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort_by')
        site_slug = self.request.query_params.get('site_slug')
        profile = Profile.objects.get(user=request.user)
        try:
            site = Site.objects.get(owner=profile, slug=site_slug)
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 10
            else:
                per_page = int(per_page)
            if query is None:
                query = ""
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = Contact.objects.filter(site=site).filter(Q(name__icontains=query) | Q(message__icontains=query) |
                                                Q(email__icontains=query) | Q(reply__icontains=query)).count()
            messages = Contact.objects.filter(site=site).filter(Q(name__icontains=query) | Q(message__icontains=query) |
                                                Q(email__icontains=query) | Q(reply__icontains=query)).order_by(sort)[start:stop]
            total_pages = math.ceil(total_items/per_page)
            if messages.exists():
                return Response({
                    'status': 'success',
                    'data': [ContactSerializer(m).data for m in messages],
                    'message': 'message list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No message found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting message list'
            })
    @action(detail=False,
            methods=['post'])
    def edit_message(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('message_id')
        site_id = request.POST.get('site_id')
        reply = request.POST.get('reply')
        site = Site.objects.get(id=int(site_id))
        msg = Contact.objects.get(id=int(id), site=site)
        try:
            msg.reply = reply
            msg.save()
            send_reply_email(profile.email, msg.email, msg.name, msg.reply, site.title)
            return Response({
                'status': 'success',
                'message': f"Replied to \'{msg.name}\'s message successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while sending reply"
            })

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False,
            methods=['get'])
    def get_blogs(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        query = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        sort = self.request.query_params.get('sort_by')
        cat_id = self.request.query_params.get('category_id')
        site_slug = self.request.query_params.get('site_slug')
        profile = Profile.objects.get(user=request.user)
        try:
            site = Site.objects.get(owner=profile, slug=site_slug)
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 10
            else:
                per_page = int(per_page)
            if query is None:
                query = ""
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = 0
            blogs = None
            category = None
            if status == 'all' and cat_id == 'all':
                total_items = Blog.objects.filter(author=profile, site=site).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, site=site).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).order_by(sort)[start:stop]
            elif status != 'all' and cat_id == 'all':
                total_items = Blog.objects.filter(author=profile, site=site, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, site=site, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).order_by(sort)[start:stop]
            elif status == 'all' and cat_id != 'all':
                category = BlogCategory.objects.get(id=int(cat_id))
                total_items = Blog.objects.filter(author=profile, site=site, category=category).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, site=site, category=category).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).order_by(sort)[start:stop]
            elif status != 'all' and cat_id != 'all':
                category = BlogCategory.objects.get(id=int(cat_id))
                total_items = Blog.objects.filter(author=profile, site=site, category=category, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, site=site, category=category, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).order_by(sort)[start:stop]
            total_pages = math.ceil(total_items/per_page)
            if blogs.exists():
                return Response({
                    'status': 'success',
                    'data': [BlogSerializer(blog).data for blog in blogs],
                    'message': 'blog list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No blogs found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting blog list'
            })
    @action(detail=False,
            methods=['get'])
    def get_blog_categories(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            cats = BlogCategory.objects.filter(owner=profile)
            if cats.exists():
                return Response({
                    'status': 'success',
                    'message': 'categories found',
                    'data': [BlogCategorySerializer(c).data for c in cats]
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'no category found'
                })
        except:
            return Response({
                'status': 'error',
                'message': 'error occured'
            })
    @action(detail=False,
            methods=['get'])
    def get_blog_tags(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            tags = Tag.objects.filter(owner=profile)
            if tags.exists():
                return Response({
                    'status': 'success',
                    'message': 'tags found',
                    'data': [TagSerializer(t).data for t in tags]
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'no tag found'
                })
        except:
            return Response({
                'status': 'error',
                'message': 'error occured'
            })
    
    @action(detail=False,
            methods=['post'])
    def edit_blog(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('blog_id')
        title = request.POST.get('title')
        slug = slugify(title)
        status = request.POST.get('status')
        image = request.FILES.get('image')
        post = request.POST.get('post')
        keywords = request.POST.get('keywords')
        description = request.POST.get('description')
        cat_id = request.POST.get('category_id')
        comm = request.POST.get('allow_comments')
        tags_ids = request.POST.getlist('tag_ids', [])
        blog = Blog.objects.get(id=int(id), author=profile)
        try:
            site = blog.site
            for b in site.site_blogs.all():
                if b.slug == slug and b.id != int(id):
                    return Response({
                        'status': 'error',
                        'message': f"A blog with title {title} already exists on your site!"
                    })
                else:
                    pass
            category = BlogCategory.objects.get(id=int(cat_id))
            #tags = Tag.objects.filter(slug__in=tag_slugs)
            blog.title = title
            blog.slug = slug
            blog.status = status
            blog.post = post
            blog.meta_keywords = keywords
            blog.meta_description = description
            blog.category = category
            if comm == 'true':
                comm = True
            elif comm == 'false':
                comm = False
            else:
                comm = True
            blog.allow_comments = comm
            blog.save()
            if image is not None:
                blog.image = image
                blog.save()
            tag_ids = [int(tag_id) for tag_id in tags_ids]
            tags = Tag.objects.filter(id__in=tag_ids)
            for t in blog.tags.all():
                blog.tags.remove(t)
                blog.save()
            for t in tags:
                blog.tags.add(t)
                blog.save()
            return Response({
                'status': 'success',
                'message': f"post \'{blog.title}\' edited successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while editing post"
            })
    @action(detail=False,
        methods=['post'])
    def add_blog(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        title = request.POST.get('title')
        slug = slugify(title)
        status = request.POST.get('status')
        image = request.FILES.get('image')
        post = request.POST.get('post')
        keywords = request.POST.get('keywords')
        description = request.POST.get('description')
        cat_id = request.POST.get('category_id')
        comm = request.POST.get('allow_comments')
        site_slug = request.POST.get('site_slug')
        tags_ids = request.POST.getlist('tag_ids', [])
        try:
            category = BlogCategory.objects.get(id=int(cat_id), owner=profile)
            site = Site.objects.get(owner=profile, slug=site_slug)
            # check if the title does not exists
            for b in site.site_blogs.all():
                if b.slug == slug:
                    return Response({
                        'status': 'error',
                        'message': f"title \'{title}\' already exists!"
                    })
                else:
                    pass
            #tags = Tag.objects.filter(slug__in=tag_slugs)
            if comm == 'true':
                comm = True
            elif comm == 'false':
                comm = False
            else:
                comm = True
            new_blog = Blog(author=profile, site=site, title=title, slug=slug, post=post, meta_keywords=keywords, image=image,
                            meta_description=description, category=category, status=status, allow_comments=comm)
            new_blog.save()
            tag_ids = [int(tag_id) for tag_id in tags_ids]
            tags = Tag.objects.filter(id__in=tag_ids)
            for t in tags:
                new_blog.tags.add(t)
                new_blog.save()
            return Response({
                'status': 'success',
                'message': f"post \'{new_blog.title}\' created successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while creating post"
            })
    @action(detail=False,
        methods=['post'])
    def create_blog_category(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        title = request.POST.get('title')
        slug = slugify(title)
        #tag_slugs = request.POST.getlist('tag_slugs', [])
        try:
            # check if the title does not exists
            for c in profile.blog_categories_created.all():
                if c.slug == slug:
                    return Response({
                        'status': 'error',
                        'message': f"title \'{title}\' already exists!"
                    })
                else:
                    pass
            new_cat = BlogCategory(owner=profile, title=title, slug=slug)
            new_cat.save()
            return Response({
                'status': 'success',
                'message': f"category \'{new_cat.title}\' created successfully",
                'data': BlogCategorySerializer(new_cat).data,
                'type': 'category',
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while creating category"
            })
    @action(detail=False,
            methods=['post'])
    def edit_blog_category(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('id')
        title = request.POST.get('title')
        slug = slugify(title)
        #tag_slugs = request.POST.getlist('tag_slugs', [])
        cat = BlogCategory.objects.get(id=int(id), owner=profile)
        try:
            for c in profile.blog_categories_created.all():
                if c.slug == slug and c.id != int(id):
                    return Response({
                        'status': 'error',
                        'message': f"A category with title {title} already exists on your site!"
                    })
                else:
                    pass
            cat.title = title
            cat.slug = slug
            cat.save()
            return Response({
                'status': 'success',
                'message': f"category \'{cat.title}\' edited successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while editing category"
            })
    @action(detail=False,
        methods=['post'])
    def create_blog_tag(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        title = request.POST.get('title')
        slug = slugify(title)
        #tag_slugs = request.POST.getlist('tag_slugs', [])
        try:
            # check if the title does not exists
            for t in profile.blog_tags.all():
                if t.slug == slug:
                    return Response({
                        'status': 'error',
                        'message': f"title \'{title}\' already exists!"
                    })
                else:
                    pass
            new_tag = Tag(owner=profile, title=title, slug=slug)
            new_tag.save()
            return Response({
                'status': 'success',
                'message': f"tag \'{new_tag.title}\' created successfully",
                'data': TagSerializer(new_tag).data,
                'type': 'tag',
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while creating tag"
            })
    @action(detail=False,
            methods=['post'])
    def edit_blog_tag(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('id')
        title = request.POST.get('title')
        slug = slugify(title)
        #tag_slugs = request.POST.getlist('tag_slugs', [])
        tag = Tag.objects.get(id=int(id), owner=profile)
        try:
            for t in profile.blog_tags.all():
                if t.slug == slug and t.id != int(id):
                    return Response({
                        'status': 'error',
                        'message': f"A tag with title {title} already exists on your site!"
                    })
                else:
                    pass
            tag.title = title
            tag.slug = slug
            tag.save()
            return Response({
                'status': 'success',
                'message': f"tag \'{tag.title}\' edited successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while editing tag"
            })
    @action(detail=False,
            methods=['get'])
    def get_blog_comments(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        query = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort_by')
        blog_id = self.request.query_params.get('blog_id')
        profile = Profile.objects.get(user=request.user)
        try:
            blog = Blog.objects.get(author=profile, id=int(blog_id))
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 10
            else:
                per_page = int(per_page)
            if query is None:
                query = ""
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = Comment.objects.filter(blog=blog).filter(Q(name__icontains=query) | Q(comment__icontains=query) |
                                                Q(reply__icontains=query)).count()
            comments = Comment.objects.filter(blog=blog).filter(Q(name__icontains=query) | Q(comment__icontains=query) |
                                                Q(reply__icontains=query)).order_by(sort)[start:stop]
            total_pages = math.ceil(total_items/per_page)
            if comments.exists():
                return Response({
                    'status': 'success',
                    'data': [CommentSerializer(m).data for m in comments],
                    'message': 'comment list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No comment found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting comment list'
            })
    @action(detail=False,
            methods=['post'])
    def edit_comment(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        id = request.POST.get('comment_id')
        blog_id = request.POST.get('blog_id')
        reply = request.POST.get('reply')
        active = request.POST.get('active')
        blog = Blog.objects.get(id=int(blog_id), author=profile)
        com = Comment.objects.get(id=int(id), blog=blog)
        try:
            if active.lower() == "true":
                active = True
            elif active.lower() == "false":
                active = False
            com.reply = reply
            com.active = active
            com.save()
            return Response({
                'status': 'success',
                'message': f"Replied to \'{com.name}\'s comment successfully"
            })
        except:
            return Response({
                'status': 'error',
                'message': f"Error occured while sending reply"
            })

class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False,
            methods=['get'])
    def get_templates(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        query = self.request.query_params.get('search')
        plan = self.request.query_params.get('plan')
        cat_id = self.request.query_params.get('category_id')
        profile = Profile.objects.get(user=request.user)
        try:
            per_page = 20
            if page is None:
                page = 1
            else:
                page = int(page)
            if query is None:
                query = ""
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = 0
            templates = None
            category = None
            #print('hi')
            if plan == 'all' and cat_id == 'all':
                total_items = Template.objects.filter(Q(title__icontains=query)).count()
                templates = Template.objects.filter(Q(title__icontains=query))[start:stop]
            elif plan != 'all' and cat_id == 'all':
                if plan == 'free':
                    total_items = Template.objects.filter(plan__level=1).filter(Q(title__icontains=query)).count()
                    templates = Template.objects.filter(plan__level=1).filter(Q(title__icontains=query))[start:stop]
                elif plan == 'paid':
                    total_items = Template.objects.exclude(plan__level=1).filter(Q(title__icontains=query)).count()
                    templates = Template.objects.exclude(plan__level=1).filter(Q(title__icontains=query))[start:stop]
            elif plan == 'all' and cat_id != 'all':
                category = TemplateCategory.objects.get(id=int(cat_id))
                total_items = Template.objects.filter(category=category).filter(Q(title__icontains=query)).count()
                templates = Template.objects.filter(category=category).filter(Q(title__icontains=query))[start:stop]
            elif plan != 'all' and cat_id != 'all':
                category = TemplateCategory.objects.get(id=int(cat_id))
                if plan == 'free':
                    total_items = Template.objects.filter(plan__level=1, category=category).filter(Q(title__icontains=query)).count()
                    templates = Template.objects.filter(plan__level=1, category=category).filter(Q(title__icontains=query))[start:stop]
                elif plan == 'paid':
                    total_items = Template.objects.exclude(plan__level=1, category=category).filter(Q(title__icontains=query)).count()
                    templates = Template.objects.exclude(plan__level=1, category=category).filter(Q(title__icontains=query))[start:stop]
            total_pages = math.ceil(total_items/per_page)
            if templates.exists():
                return Response({
                    'status': 'success',
                    'data': [TemplateSerializer(t).data for t in templates],
                    'message': 'template list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No templates found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting template list'
            })
    @action(detail=False,
        methods=['get'])
    def get_template(self, request, *args, **kwargs):
        id = self.request.query_params.get('template_id')
        profile = Profile.objects.get(user=request.user)
        plan = profile.plan
        if id:
            try:
                template = Template.objects.get(id=int(id))
                if template is not None:
                    return Response({
                        'status': 'success',
                        'data': TemplateSerializer(template).data,
                        'plan': PlanSerializer(plan).data,
                        'message': 'template details retrieved'
                    })
                else:
                    return Response({
                        'status': 'error',
                        'message': 'template does not exist'
                    })
            except:
                return Response({
                    'status': 'error',
                    'message': 'template does not exist'
                })
        else:
            return Response({
                'status': 'error',
                'message': 'template does not exist'
            })

    """
    @action(detail=False,
            methods=['post'])
    def create_category(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        title = request.POST.get('title')
        slug = slugify(title)
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                # check if category does not exist
                category = NewsCategory.objects.get(slug=slug)
                if category is not None:
                    return Response({
                        'status': "error",
                        "message": "category already exists!"
                    })
                else:
                    new_cat = NewsCategory(title=title, slug=slug)
                    new_cat.save()
                    Log.objects.create(user=profile, action=f"created a news category {title}")
                    return Response({
                        'status': "success",
                        "message": "category created sucessfully",
                        "data": NewsCategorySerializer(new_cat).data,
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })
    
    @action(detail=False,
            methods=['post'])
    def delete_category(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    category = NewsCategory.objects.get(id=id)
                    category.delete()
                    Log.objects.create(user=profile, action=f"deleted category {category.title}")
                    return Response({
                        'status': "success",
                        "message": f"category \'{category.title}\' deleted sucessfully",
                    })
                except:
                    return Response({
                        "status": "error",
                        "message": f"category  with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False,
            methods=['get'])
    def filter_news(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        active_filter = self.request.query_params.get('active')
        verify_filter = self.request.query_params.get('verified')
        #cat_filter = self.request.query_params.get('category_id')
        try:
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 20
            else:
                per_page = int(per_page)
            if active_filter is None:
                active_filter = True
            elif active_filter.lower() == 'true':
                active_filter = True
            elif active_filter.lower() == 'false':
                active_filter = False
            else:
                active_filter = True
            if verify_filter is None:
                verify_filter = True
            elif verify_filter.lower() == 'true':
                verify_filter = True
            elif verify_filter.lower() == 'false':
                verify_filter = False
            else:
                verify_filter = True
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = News.objects.filter(active=active_filter, verified=verify_filter).count()
            total_pages = math.ceil(total_items/per_page)
            news = News.objects.filter(active=active_filter, verified=verify_filter)[start:stop]
            if news.exists():
                return Response({
                    'status': 'success',
                    'data': [NewsSerializer(ne).data for ne in news],
                    'message': 'news list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No news found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting news list'
            })
    @action(detail=False,
        methods=['get'])
    def get_news(self, request, *args, **kwargs):
        id = self.request.query_params.get('news_id')
        if id:
            try:
                news = News.objects.get(id=int(id))
                if news is not None:
                    return Response({
                        'status': 'success',
                        'data': NewsSerializer(news).data,
                        'message': 'news details retrieved'
                    })
                else:
                    return Response({
                        'status': 'success',
                        'message': 'Invalid news ID'
                    })
            except:
                return Response({
                    'status': 'error',
                    'message': 'Invalid news ID'
                })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid news ID'
            })
    @action(detail=False,
            methods=['post'])
    def create_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        title = request.POST.get('title')
        slug = slugify(title)
        post = request.POST.get('post')
        active = request.POST.get('active')
        verified = request.POST.get('verified')
        cat_id = int(request.POST.get('category_id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    category = NewsCategory.objects.get(id=cat_id)
                    try:
                        news = News(author=profile, title=title, slug=slug, post=post,
                                        category=category, active=active, verified=verified)
                        news.save()
                        Log.objects.create(user=profile, action=f"created a new post {title}")
                        create_action(profile, "added a news post", news)
                        return Response({
                            'status': "success",
                            "message": "news created sucessfully",
                            "data": NewsSerializer(news).data,
                        })
                    except:
                        return Response({
                            'status': "error",
                            "message": "error while creating news"
                        })
                except:
                    return Response({
                        "status": "error",
                        "message": f"category with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "invalid API token"
            })

    @action(detail=False,
            methods=['post'])
    def edit_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('news_id'))
        title = request.POST.get('title')
        post = request.POST.get('post')
        active = request.POST.get('active')
        verified = request.POST.get('verified')
        cat_id = int(request.POST.get('category_id'))

        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    news = News.objects.get(id=id)
                    try:
                        if cat_id:
                            try:
                                category = NewsCategory.objects.get(id=cat_id)
                                news.category = category
                                news.save()
                            except:
                                return Response({
                                    "status": "error",
                                    "message": f"category  with id \'{id}\' does not exist"
                                })
                        if title:
                            news.title = title
                            slug = slugify(title)
                            news.slug = slug
                            news.save()
                        if post:
                            news.post = post
                            news.save()
                        if active:
                            news.active = active
                            news.save()
                        if verified:
                            news.verified = verified
                            news.save()
                        Log.objects.create(user=profile, action=f"edited a news post {title}")
                        return Response({
                            'status': "success",
                            "message": f"\'{news.title}\' edited sucessfully",
                            "data": NewsSerializer(news).data,
                        })
                    except:
                        return Response({
                            'status': "error",
                            "message": "error while saving news"
                        })
                except:
                    return Response({
                        'status': "error",
                        "message": "invalid news id"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "invalid API token"
            })
    @action(detail=False,
            methods=['post'])
    def delete_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    news = News.objects.get(id=id)
                    news.delete()
                    Log.objects.create(user=profile, action=f"deleted a news post {news.title}")
                    return Response({
                        'status': "success",
                        "message": f"news \'{news.title}\' deleted sucessfully",
                    })
                except:
                    return Response({
                        "status": "error",
                        "message": f"news with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })
    """