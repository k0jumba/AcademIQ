from django.contrib import admin
from core.models import (
    Student,
    Educator,
    Course,
    Lesson,
    Content,
    TextContent,
    QuizContent,
    Question,
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    TextFieldQuestion,
    Assignment,
    Grade,
    Submission
)

# Register your models here.
admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(TextContent)
admin.site.register(QuizContent)
admin.site.register(Question)
admin.site.register(SingleChoiceQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(TextFieldQuestion)
admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(Submission)
