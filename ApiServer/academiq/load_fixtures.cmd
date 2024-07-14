@echo off
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/educators.json
python manage.py loaddata fixtures/students.json
python manage.py loaddata fixtures/courses.json
python manage.py loaddata fixtures/lessons.json
python manage.py loaddata fixtures/assignments.json
python manage.py loaddata fixtures/grades.json
python manage.py loaddata fixtures/contents.json
python manage.py loaddata fixtures/text_contents.json
python manage.py loaddata fixtures/quiz_contents.json
python manage.py loaddata fixtures/questions.json
python manage.py loaddata fixtures/single_choice_questions.json
python manage.py loaddata fixtures/multiple_choice_questions.json
python manage.py loaddata fixtures/text_field_questions.json
python manage.py loaddata fixtures/submissions.json
