from django.contrib.auth.models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from core.models import (
    Assignment,
    Content,
    Course,
    Educator,
    Grade,
    Lesson,
    MultipleChoiceQuestion,
    QuizContent,
    SingleChoiceQuestion,
    Student,
    Submission,
    TextContent,
    TextFieldQuestion,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CustomUserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        user = super().create(validated_data)
        Student.objects.create(user=user)
        return user


class ShortStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name"]


class FullStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "user"]


class StudentProfileSeriailzer(serializers.ModelSerializer):
    student = ShortStudentSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "student"]


class EditStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["first_name", "last_name"]


class ShortEducatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = ["id", "first_name", "last_name"]


class FullEducatorSerilizer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Educator
        fields = ["id", "first_name", "last_name", "user"]


class CoursesListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "slug", "title", "is_subscribed"]

    def get_is_subscribed(self, obj):
        user = self.context["user"]
        if hasattr(user, "student"):
            is_subscribed = obj.students.filter(id=user.student.id).exists()
        elif hasattr(user, "educator"):
            is_subscribed = obj.educators.filter(id=user.educator.id).exists()
        return is_subscribed


class EducatorProfileSerializer(serializers.ModelSerializer):
    educator = ShortEducatorSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "educator"]


class EditEducatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = ["first_name", "last_name"]


class CourseDetailsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "slug", "title", "description", "is_subscribed"]

    def get_is_subscribed(self, obj):
        user = self.context["user"]
        if hasattr(user, "student"):
            is_subscribed = obj.students.filter(id=user.student.id).exists()
        elif hasattr(user, "educator"):
            is_subscribed = obj.educators.filter(id=user.educator.id).exists()
        return is_subscribed


class LessonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "order"]


class LessonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description"]


class ContentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "title", "order", "content_type"]


class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = [
            "id",
            "title",
            "description",
            "content_type",
            "text",
        ]


class SingleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChoiceQuestion
        fields = ["id", "text", "order", "question_type", "options"]


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ["id", "text", "order", "question_type", "options"]


class TextFieldQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextFieldQuestion
        fields = ["id", "text", "order", "question_type"]


class QuizContentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuizContent
        fields = ["id", "title", "description",
                  "content_type", "assignment", "questions"]

    def get_questions(self, obj):
        questions = obj.question_set.all()
        serialized_questions = []
        for question in questions:
            if question.question_type == "SingleChoiceQuestion":
                serialized_question = SingleChoiceQuestionSerializer(
                    question.singlechoicequestion
                ).data
            elif question.question_type == "MultipleChoiceQuestion":
                serialized_question = MultipleChoiceQuestionSerializer(
                    question.multiplechoicequestion
                ).data
            elif question.question_type == "TextFieldQuestion":
                serialized_question = TextFieldQuestionSerializer(
                    question.textfieldquestion
                ).data
            serialized_questions.append(serialized_question)
        return serialized_questions


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "title", "weight", "is_checkpoint", "assignment_type"]


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "description",
            "weight",
            "is_checkpoint",
            "assignment_type",
        ]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "score", "created"]


class AssignmentGradeSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ["id", "title", "description",
                  "weight", "is_checkpoint", "grade"]

    def get_grade(self, obj):
        student = self.context["student"]
        grade = (
            Grade.objects.filter(assignment=obj, student=student)
            .order_by("-created")
            .first()
        )
        serialized_grade = GradeSerializer(grade).data if grade else None
        return serialized_grade


class StudentProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    assignments = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    pass_status = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "user",
            "first_name",
            "last_name",
            "assignments",
            "progress",
            "pass_status",
        ]

    def get_assignments(self, obj):
        course = self.context["course"]
        assignments = Assignment.objects.filter(course=course)
        return AssignmentGradeSerializer(
            assignments, many=True, context={"student": obj}
        ).data

    def get_progress(self, obj):
        course = self.context["course"]
        assignments = Assignment.objects.filter(course=course)
        total_weight = sum(assign.weight for assign in assignments)
        if total_weight == 0:
            return 0
        total_score = sum(
            (
                Grade.objects.filter(assignment=assign, student=obj)
                .order_by("-created")
                .first()
                .score
                if Grade.objects.filter(assignment=assign, student=obj).exists()
                else 0
            )
            * assign.weight
            for assign in assignments
        )
        return total_score / total_weight

    def get_pass_status(self, obj):
        course = self.context["course"]
        assignments = Assignment.objects.filter(course=course)
        progress = self.get_progress(obj)
        if progress < 60:
            return False
        for assign in assignments.filter(is_checkpoint=True):
            grade = (
                Grade.objects.filter(assignment=assign, student=obj)
                .order_by("-created")
                .first()
            )
            if not grade or grade.score < 60:
                return False
        return True


class GradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["assignment", "student", "score"]


class MySubmissionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "assignment", "created", "submission_type"]


class SubmissionsListSerializer(serializers.ModelSerializer):
    author = FullStudentSerializer()

    class Meta:
        model = Submission
        fields = ["id", "author", "created", "submission_type"]


class SubmissionSerializer(serializers.ModelSerializer):
    author = FullStudentSerializer()

    class Meta:
        model = Submission
        fields = [
            "id",
            "author",
            "assignment",
            "created",
            "submission_type",
            "submission_data",
        ]


class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["author", "assignment", "submission_type", "submission_data"]

    def validate(self, data):
        assignment_type = data["assignment"].assignment_type
        submission_type = data["submission_type"]

        if assignment_type != submission_type:
            raise serializers.ValidationError(
                f"Invalid submission type. Expected {assignment_type}, got {submission_type}."
            )

        return data

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)
