from django.contrib import admin
from .models import Question, Choice

# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "published_recently"]
    search_fields = ["question_text"]
    list_filter = ["pub_date"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
