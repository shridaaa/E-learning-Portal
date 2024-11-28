from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import api

urlpatterns = [
    #General
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),


    #Teacher
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('edit_students/<int:course_id>/', views.edit_students_in_course,name='edit_students_in_course'),
    path('search_users/', views.search_users, name='search_users'),
    

    #Student
    path('student/course_material/<int:course_id>/', views.student_course_material, name='student_course_material'),
    path('student_feedback_form/<int:course_id>/', views.student_feedback_form, name='student_feedback_form'),
    path('student_feedback_confirmation/', views.student_feedback_confirmation, name='student_feedback_confirmation'),
    path('student_course_enrollment/', views.student_course_enrollment, name='student_course_enrollment'),


    #API for User data
    path('api/user_list', api.user_list, name='api_user_list'),
    path('api/user/<int:pk>/', api.user_details, name='user_details'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)