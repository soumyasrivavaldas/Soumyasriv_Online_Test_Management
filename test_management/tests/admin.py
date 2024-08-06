from django.contrib import admin
from .models import User, Test, Question, Answer, Result

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('username', 'email')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'text')
    search_fields = ('text',)
    list_filter = ('test',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    search_fields = ('text',)
    list_filter = ('question', 'is_correct')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'score')
    list_filter = ('user', 'test')
    search_fields = ('user__username', 'test__title')
