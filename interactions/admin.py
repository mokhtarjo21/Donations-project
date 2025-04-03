from django.contrib import admin
from .models import *  
# Register your models here
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(Donation)
admin.site.register(Comment)
