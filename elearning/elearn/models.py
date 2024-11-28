from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_teacher = models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)


class Status(models.Model):
    user = models.CharField(max_length=100)
    status_message = models.TextField (null=False, default="Type in your status")
    date_posted = models.DateTimeField(auto_now_add=True ) 

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="Description of Course")

    def __str__(self):
        return self.name

class CourseMaterial(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/')
    course= models.ForeignKey(Course, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    courses_taught = models.ManyToManyField(Course, related_name='teachers')
    profile_photo=models.ImageField(upload_to='profile_photo/',blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return self.user.username
    
   
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    courses_taken = models.ManyToManyField(Course, related_name='students')
    profile_photo=models.ImageField(upload_to='profile_photo/',blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return self.user.username

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 5)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)  
    

