from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Max
from django.db.models import Q
from django.urls import reverse
import logging



from .models import *
from .forms import *

# Create a logger instance for feeback later
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'elearn/index.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if the user is registering as a teacher
            if form.cleaned_data.get('is_teacher'):
                Teacher.objects.create(user=user)
                login(request, user)
                return redirect('teacher')
            # Check if the user is registering as a student
            elif form.cleaned_data.get('is_student'):
                Student.objects.create(user=user)
                login(request, user)
                return redirect('student')
    else:
        form = SignUpForm()

    register_url = reverse('register')
    print("the printed statement is: " + register_url) 
    return render(request, 'elearn/register.html', {'form': form})


#logic for logging in 
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            # clean data from form for username and password fields
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # If authentication successful and user is teacher, or student, log them in and redirect
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student')
            # If authentication fails, send error message
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'elearn/login.html', {'form': form, 'msg': msg})


def logout_view(request):
    #logs out user
    logout(request)
    # Redirect to the index page
    return redirect(index)


def profile(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'teacher'):
            user_type = 'teacher'
            profile_info = user.teacher
            profile_photo = profile_info.profile_photo
            courses = profile_info.courses_taught.all()
            form_class = TeacherProfileForm
        elif hasattr(user, 'student'):
            user_type = 'student'
            profile_info = user.student
            profile_photo = profile_info.profile_photo
            courses = profile_info.courses_taken.all()
            form_class = StudentProfileForm
        else:
            # Handle cases where the user is neither a teacher nor a student
            user_type = None
            profile_info = None
            profile_photo = None
            courses = None
            form_class = None
        if request.method == 'POST':
            if 'photo_upload' in request.POST:
                # Process profile photo upload
                if 'profile_photo' in request.FILES:
                    profile_info.profile_photo = request.FILES['profile_photo']
                    profile_info.save()
            else:
                # Process form data (first_name and last_name)
                form = form_class(request.POST, instance=profile_info)
                if form.is_valid():
                    form.save()
            return redirect('profile')
        else:
            form = form_class(instance=profile_info)
        return render(request, 'elearn/profile.html', {
            'user_type': user_type,
            'profile_info': profile_info,
            'profile_photo': profile_photo,
            'courses': courses,
            'form': form
            })
    else:
    # Handle the case where the user is not authenticated
        return render(request, 'elearn/error.html', {'message': 'You must be logged in as a teacher to access this page.'})
  


def admin(request):
    return render(request,'elearn/admin.html')


#teacher_dashboard
@login_required(login_url='login_view')
def teacher(request):
    if request.user.is_authenticated:
        try:
            teacher = Teacher.objects.get(user=request.user)
            courses = teacher.courses_taught.all()  # Retrieve the courses taught by the teacher
            context = {
                'teacher': teacher,
                'courses': courses,  # Pass the courses to the template
            }
            return render(request, 'elearn/teacher_dashboard.html', context)
        except Teacher.DoesNotExist:
            return render(request, 'elearn/error.html', {'message': 'You are not registered as a teacher in the system.'})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'elearn/error.html', {'message': 'You must be logged in as a teacher to access this page.'})


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)  
        if form.is_valid():
            course = form.save()  # Save the course
            # Associate the course with the current teacher
            try:
                #course added to corse_taught field
                teacher = Teacher.objects.get(user=request.user)
                teacher.courses_taught.add(course)
            except Teacher.DoesNotExist:
                #case - teacher does not exist i.e logged out
                # redirect to  error page
                return render(request, 'elearn/error.html', {'message': 'You are not registered as a teacher in the system.'})
            return redirect('teacher')  # Redirect to teacher dashboard after course creation
    else:
        form = CourseForm()
    
    context = {
        'course_form': form
    }

    return render(request, 'elearn/create_course.html', context)



def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_materials = CourseMaterial.objects.filter(course_id=course)  # Retrieve all course materials for the course
    form = CourseMaterialForm()  # Initialize an empty form for adding new course materials
    
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)  # Populate CourseForm with existing course data
        if course_form.is_valid():
            course_form.save()  # Save the updated course data
            return redirect('edit_course', course_id=course.id)  # Redirect to refresh the page
        form = CourseMaterialForm(request.POST, request.FILES)  # Create a CourseMaterialForm instance with uploaded data
        if form.is_valid():
            course_material = form.save(commit=False)  # Save the course material but don't commit to database yet
            course_material.course = course  # Associate the course material with the current course
            course_material.save()  # Save the course material to the database
            return redirect('edit_course', course_id=course.id)  # Redirect to refresh the page
    else:
        course_form = CourseForm(instance=course)  # Populate CourseForm with existing course data
    
    context = {
        'course': course,
        'course_materials': course_materials,
        'course_form': course_form,
        'form': form,
    }
    return render(request, 'elearn/edit_course.html', context)


def edit_students_in_course(request, course_id):
    # Get the course  using its ID
    course = get_object_or_404(Course, pk=course_id)
    enrolled_students = Student.objects.filter(courses_taken__id=course_id)

    if request.method == 'POST':
        # Check if the form is submitted to remove a student
        if 'remove_student' in request.POST:
            # Get the student ID to be removed from the course
            student_id = request.POST.get('remove_student')
            # Remove the student from the course
            student = get_object_or_404(Student, pk=student_id)
            course.students.remove(student)
            return redirect('edit_students_in_course', course_id=course_id)

        # If adding a student 
        form = EditStudentForm(request.POST)
        if form.is_valid():
            # Get the selected student from the form
            student_id = form.cleaned_data['student']
            # Add the student to the course
            student = get_object_or_404(Student, pk=student_id)
            course.students.add(student)
            return redirect('edit_students_in_course', course_id=course_id)
    else:
        form = EditStudentForm()

    # Pass the course and enrolled students to the template
    context = {
        'course': course,
        'enrolled_students': enrolled_students,
        'form': form,
    }
    return render(request, 'elearn/edit_students.html', context)





#students_dashboard
@login_required(login_url='login_view')
def student(request):
    student_profile = request.user.student
    student_courses = student_profile.courses_taken.all()
    return render(request, 'elearn/student_dashboard.html', {'student_courses': student_courses, 'student' : student_profile})

def student_course_material(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_materials = course.coursematerial_set.all()
    return render(request, 'elearn/student_course_material.html', {'course': course, 'course_materials': course_materials})

def student_feedback_form(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user.student
            feedback.course = course
            feedback.save()
            return redirect('student_feedback_confirmation')  # Redirect to feedback confirmation page
    else:
        form = FeedbackForm()
    return render(request, 'elearn/student_feedback_form.html', {'form': form, 'course' :course})


def student_feedback_confirmation(request):
    # Get previous feedback for the current student
    previous_feedback = Feedback.objects.filter(student=request.user.student)
    context = {
        'previous_feedback': previous_feedback
    }
    return render(request, 'elearn/student_feedback_confirmation.html', context)

def student_course_enrollment(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        student = request.user.student
        student.courses_taken.add(course)
        return redirect('student')
    else:
        available_courses = Course.objects.exclude(students__user=request.user)
        return render(request, 'elearn/student_course_enrollment.html', {'available_courses': available_courses})



###search for users
@user_passes_test(lambda user: user.is_teacher, login_url='/login/')  # only allow search access to teachers 
def search_users(request):
    # Get all users who are students and teachers to search
    students = User.objects.filter(is_student=True)
    teachers = User.objects.filter(is_teacher=True)

    query = request.GET.get('query')
    if query:
        # Filter students and teachers based on the query by user
        students = students.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        teachers = teachers.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

    print("Students:", students)
    print("Teachers:", teachers)

    return render(request, 'elearn/search_users.html', {'students': students, 'teachers': teachers})

