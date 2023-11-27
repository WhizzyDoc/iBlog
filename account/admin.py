from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Developer)
admin.site.register(Template)
admin.site.register(TemplateCategory)
admin.site.register(Site)
admin.site.register(MainSite)
admin.site.register(Plan)
admin.site.register(Contact)
admin.site.register(Notification)