from django.contrib import admin
from .models import Question, Choice, Comment
from profiles.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User




class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['user__username', 'user__email']
    list_editable = ['is_verified'] 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

class CommentAdmin(admin.TabularInline):
    model = Comment
    list_display = ["comment_text", "pub_date"]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    list_display = ["question_text", "pub_date", "was_published_recently"]

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
        ("Likes", {"fields": ["likes"]}),
    ]
    inlines = [ChoiceInline, CommentAdmin]
    list_display = ["question_text", "pub_date", "was_published_recently", "likes"]
    list_filter = ["pub_date"]


admin.site.register(Question, QuestionAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin) 
