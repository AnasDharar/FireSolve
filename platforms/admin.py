from django.contrib import admin

from platforms.models import Platform, Problem, POTDStatus

# Register your models here.
admin.site.register(Platform)
admin.site.register(Problem)
admin.site.register(POTDStatus)