from django.contrib import admin

from . import models


@admin.register(models.Model)
class Model(admin.ModelAdmin):
    pass


@admin.register(models.Job)
class Job(admin.ModelAdmin):
    pass


@admin.register(models.Machine)
class Machine(admin.ModelAdmin):
    pass
