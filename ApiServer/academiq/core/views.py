from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from core.models import Assignment, Content, Course, Lesson, Submission
from core.permissions import (
    IsEducator,
    IsStudent,
    IsSubmissionOwnerOrEducator,
    IsSubscribed,
)
from core.serializers import (
    AssignmentListSerializer,
    AssignmentSerializer,
    CreateSubmissionSerializer,
    EditEducatorSerializer,
    EditStudentSerializer,
    EducatorProfileSerializer,
    FullEducatorSerilizer,
    StudentProfileSeriailzer,
    FullStudentSerializer,
    SubmissionsListSerializer,
    ContentsListSerializer,
    CoursesListSerializer,
    CourseDetailsSerializer,
    GradeCreateSerializer,
    LessonDetailsSerializer,
    LessonsListSerializer,
    MySubmissionsListSerializer,
    QuizContentSerializer,
    StudentProgressSerializer,
    SubmissionSerializer,
    TextContentSerializer,
)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsEducator]

    def get(self, request):
        if hasattr(request.user, "student"):
            serializer = StudentProfileSeriailzer(request.user)
        elif hasattr(request.user, "educator"):
            serializer = EducatorProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        if hasattr(request.user, "student"):
            serializer = EditStudentSerializer(
                data=request.data, instance=request.user.student
            )
        elif hasattr(request.user, "educator"):
            serializer = EditEducatorSerializer(
                data=request.data, instance=request.user.educator
            )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoursesListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsEducator]
    
    def get(self, request):
        queryset = Course.objects.all()
        serializer = CoursesListSerializer(queryset, many=True, context={"user": request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyCoursesListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsEducator]
    
    def get(self, request):
        if hasattr(request.user, "student"):
            queryset = request.user.student.course_set
        elif hasattr(request.user, "educator"):
            queryset = request.user.educator.course_set
        serializer = CoursesListSerializer(queryset, many=True, context={"user": request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsEducator]

    def get(self, request, course_slug):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, slug=course_slug)
        serializer = CourseDetailsSerializer(course, context={"user": request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeCourseView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    def post(self, request, course_slug):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, slug=course_slug)
        student = request.user.student
        course.students.add(student)
        return Response(status=status.HTTP_200_OK)


class UnsubscribeCourseView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
        IsSubscribed,
    ]

    def post(self, request, course_slug):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        student = request.user.student
        course.students.remove(student)
        return Response(status=status.HTTP_200_OK)


class LessonsListView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        lessons_queryset = course.lesson_set
        serializer = LessonsListSerializer(lessons_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug, lesson_order):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)

        self.check_object_permissions(request, course)

        lessons_queryset = course.lesson_set
        lesson = get_object_or_404(lessons_queryset, order=lesson_order)

        serializer = LessonDetailsSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContentsListView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug, lesson_order):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        lessons_queryset = course.lesson_set
        lesson = get_object_or_404(lessons_queryset, order=lesson_order)
        contents_queryset = lesson.content_set
        serializer = ContentsListSerializer(contents_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContentDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug, lesson_order, content_order):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        lessons_queryset = course.lesson_set
        lesson = get_object_or_404(lessons_queryset, order=lesson_order)
        contents_queryset = lesson.content_set
        content = get_object_or_404(contents_queryset, order=content_order)

        if content.content_type == "TextContent":
            serializer = TextContentSerializer(content.textcontent)
        elif content.content_type == "QuizContent":
            serializer = QuizContentSerializer(content.quizcontent)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentListView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        assignment_queryset = Assignment.objects.filter(course=course)
        serializer = AssignmentListSerializer(assignment_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug, assignment_id):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        assignment = get_object_or_404(
            Assignment.objects.filter(course=course), pk=assignment_id
        )
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GradesTableView(APIView):
    permission_classes = [IsAuthenticated, IsSubscribed]

    def get(self, request, course_slug):
        courses_queryset = Course.objects.all()
        course = get_object_or_404(courses_queryset, slug=course_slug)
        self.check_object_permissions(request, course)
        students = course.students
        serializer = StudentProgressSerializer(
            students, many=True, context={"course": course}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateGradeView(APIView):
    permission_classes = [IsAuthenticated, IsEducator, IsSubscribed]

    def post(self, request, course_slug):
        course = get_object_or_404(Course.objects.all(), slug=course_slug)
        self.check_object_permissions(request, course)

        serializer = GradeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MySubmissionsListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent, IsSubscribed]

    def get(self, request, course_slug):
        course = get_object_or_404(Course.objects.all(), slug=course_slug)
        self.check_object_permissions(request, course)

        submissions_queryset = Submission.objects.filter(
            assignment__course=course
        ).filter(author=request.user.student)
        serializer = MySubmissionsListSerializer(submissions_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentSubmissionsListView(APIView):
    permission_classes = [IsAuthenticated, IsEducator, IsSubscribed]

    def get(self, request, course_slug, assignment_id):
        course = get_object_or_404(Course.objects.all(), slug=course_slug)
        self.check_object_permissions(request, course)

        assignment = get_object_or_404(
            Assignment.objects.filter(course=course), pk=assignment_id
        )
        serializer = SubmissionsListSerializer(assignment.submission_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_slug, submission_id):
        course = get_object_or_404(Course.objects.all(), slug=course_slug)
        self.check_object_permissions(request, course)
        submission = get_object_or_404(
            Submission.objects.filter(assignment__course=course), pk=submission_id
        )
        self.check_object_permissions(request, submission)
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_object_permissions(self, request, obj):
        if isinstance(obj, Course):
            permission = IsSubscribed()
        elif isinstance(obj, Submission):
            permission = IsSubmissionOwnerOrEducator()
        else:
            return

        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(
                request, message=getattr(permission, "message", None)
            )


class CreateSubmissionView(APIView):
    permission_classes = [IsAuthenticated, IsStudent, IsSubscribed]

    def post(self, request, course_slug, assignment_id):
        course = get_object_or_404(Course.objects.all(), slug=course_slug)
        self.check_object_permissions(request, course)

        assignment = get_object_or_404(course.assignment_set, pk=assignment_id)
        author = request.user.student

        data = request.data.copy()
        data["assignment"] = assignment.id
        data["author"] = author.id

        serializer = CreateSubmissionSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
