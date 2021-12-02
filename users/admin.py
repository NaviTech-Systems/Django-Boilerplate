from django.contrib import admin
from .models import User, Profile


class ProfileInlne(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = (ProfileInlne,)


admin.site.register(User, UserAdmin)
# Register your models here.
