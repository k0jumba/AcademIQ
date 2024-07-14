import json
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from core.enums import AssignmentSubmissionType, LessonContentType


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Course(models.Model):
    students = models.ManyToManyField(Student)
    educators = models.ManyToManyField(Educator)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()


class Content(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()
    content_type = models.CharField(max_length=50, editable=False)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = self.__class__.__name__
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]


class TextContent(Content):
    text = models.TextField()


class QuizContent(Content):
    assignment = models.OneToOneField("Assignment", on_delete=models.CASCADE)


class Question(models.Model):
    quiz = models.ForeignKey(QuizContent, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    text = models.TextField()
    question_type = models.CharField(max_length=50, editable=False)

    def save(self, *args, **kwargs):
        if not self.question_type:
            self.question_type = self.__class__.__name__
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]


class SingleChoiceQuestion(Question):
    options = models.TextField()

    def set_options(self, value):
        self.string_list = json.dumps(value)

    def get_options(self):
        return json.loads(self.string_list)


class MultipleChoiceQuestion(Question):
    options = models.TextField()

    def set_options(self, value):
        self.string_list = json.dumps(value)

    def get_options(self):
        print(self.string_list)
        return json.loads(self.string_list)


class TextFieldQuestion(Question):
    pass


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    weight = models.PositiveIntegerField()
    is_checkpoint = models.BooleanField()
    assignment_type = models.CharField(
        max_length=50, choices=AssignmentSubmissionType.choices()
    )


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created = models.DateTimeField(auto_now=True)


class Submission(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    submission_type = models.CharField(
        max_length=50, choices=AssignmentSubmissionType.choices()
    )
    submission_data = models.TextField()
