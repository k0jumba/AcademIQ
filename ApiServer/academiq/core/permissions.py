from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        is_student = hasattr(request.user, "student")
        return is_student


class IsEducator(permissions.BasePermission):
    def has_permission(self, request, view):
        is_educator = hasattr(request.user, "educator")
        return is_educator


class IsSubscribed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "student"):
            student = request.user.student
            is_subscribed = obj.students.filter(id=student.id).exists()
        elif hasattr(request.user, "educator"):
            educator = request.user.educator
            is_subscribed = obj.educators.filter(id=educator.id).exists()
        return is_subscribed


class IsStudentAndSubmissionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        student_permission = IsStudent()
        return student_permission.has_permission(request, view) and (
            obj.author == request.user.student
        )


class IsSubmissionOwnerOrEducator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_permission = IsStudentAndSubmissionOwner()
        educator_permission = IsEducator()
        return owner_permission.has_object_permission(
            request, view, obj
        ) or educator_permission.has_permission(request, view)