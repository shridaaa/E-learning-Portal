from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','first_name', 'last_name','email', 'last_login')

class TeacherAdmin(admin.ModelAdmin):     
    list_display = ('first_name', 'last_name', 'profile_photo', 'date_of_birth')   


class StudentAdmin(admin.ModelAdmin):     
    list_display = ('first_name', 'last_name', 'profile_photo', 'date_of_birth')   


class CourseAdmin(admin.ModelAdmin):     
    list_display = ('name', 'description')  


class CourseMaterialAdmin(admin.ModelAdmin):     
    list_display = ('name', 'file')  

admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)