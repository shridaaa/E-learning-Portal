from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_admin', 'is_teacher', 'is_student']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description']

class CourseMaterialSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CourseMaterial
        fields = ['name', 'file', 'course']

class TeacherSerializer(serializers.ModelSerializer):
    courses_taught = CourseSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['user', 'first_name', 'last_name', 'profile_photo', 'date_of_birth', 'courses_taught' ]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'first_name', 'last_name', 'profile_photo', 'date_of_birth']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['student', 'course', 'rating', 'comment', 'date_posted']