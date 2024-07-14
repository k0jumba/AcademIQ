from enum import Enum


class LessonContentType(Enum):
    TEXT = "text", "Plain text content"

    @classmethod
    def choices(cls):
        return [(key.value[0], key.value[1]) for key in cls]


class AssignmentSubmissionType(Enum):
    QUIZ = "quiz", "Quiz Assignment/Submission"

    @classmethod
    def choices(cls):
        return [(key.value[0], key.value[1]) for key in cls]
