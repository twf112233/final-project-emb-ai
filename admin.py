from django.contrib import admin
# Requirement: Import the 7 model classes
from .models import Course, Instructor, Learner, Lesson, Question, Choice, Submission


# 1. ChoiceInline to allow adding choices directly inside Question
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


# 2. QuestionInline to allow viewing/managing questions inside Lesson
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# 3. QuestionAdmin with ChoiceInline included
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade', 'lesson']
    search_fields = ['question_text']


# 4. LessonAdmin with QuestionInline included
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    inlines = [QuestionInline]


# LessonInline for CourseAdmin (if needed for the Course model)
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register models to Django Admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
