from django.test import TestCase, Client
from django.urls import reverse
from .models import *

class SignInRegisterTests(TestCase):
    def setUp(self):
        #set up test data
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'is_teacher': True  # teacher registration
        }
        

    # def tearDown(self):
    #     User.objects.all.delete()

    # Tests that index page is successful which is code 200
    def test_index_page_returns_success(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'elearn/index.html')

    # Test register page returns 200
    def test_register_page_returns_success(self):
        #Test get request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    #test correct teacher registration returns teacher dashboard
    def test_register_page_details(self):
        # Send POST request with self.user_data
        response = self.client.post(reverse('register'), self.user_data, follow=True)

        # Check if the registration was successful and user is redirected
        self.assertEqual(response.status_code, 200)  # Check if the page is rendered after successful registration
        self.assertTemplateUsed(response, 'elearn/teacher_dashboard.html')  # Assuming teacher dashboard after registration

        # Check if the user and teacher objects are created
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        self.assertTrue(Teacher.objects.filter(user__username=self.user_data['username']).exists())
        

    # def test_register_page_fails(self):
    #     # Test POST request with invalid form data (registration failure) as username already exists
    #     response = self.client.post(reverse('register'), self.user_data)
    #     # Assuming registration failure reloads the registration page
    #     self.assertEqual(response.status_code, 302) 
    #     self.assertRedirects(response, 'register')  # redirects to registration page
        
        


class TeacherFunctionsTest(TestCase):
    def setUp(self):
        # Create a teacher user
        self.teacher_user = User.objects.create_user(username='teacher', password='password')
        self.teacher = Teacher.objects.create(user=self.teacher_user, first_name='Test', last_name='Teacher')
        self.client.login(username='teacher', password='password')

    #test creating course by teachers
    def test_course_creation_redirect(self):
        before_course_count = Course.objects.count()
        # Make a POST request to create a new course
        response = self.client.post(reverse('create_course'), {'name': 'New Course', 'description': 'Description of New Course'})
        # Check if the response redirects to the teacher dashboard
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('teacher'))  
        # Check that course count has increased
        self.assertEqual(Course.objects.count(), before_course_count + 1)

    # test editing course by teachers
    def test_edit_course(self):
        course = Course.objects.create(name='Original Course', description='Original Course Description')
        # Update course data
        updated_name = 'Updated Course'
        updated_description = 'Updated Course Description'
        # Make a POST request to edit course
        response = self.client.post(reverse('edit_course', kwargs={'course_id': course.id}), {'name': updated_name, 'description': updated_description})
        # Check if the response redirects to the edit course page
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirection
        self.assertRedirects(response, reverse('edit_course', kwargs={'course_id': course.id}))  # Check if redirected to the edit course page
        # Check if the course data has been updated in the database
        updated_course = Course.objects.get(id=course.id)
        self.assertEqual(updated_course.name, updated_name)
        self.assertEqual(updated_course.description, updated_description)


    

class StudentsFunctionsTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(username='Student', password='password')
        self.student = Student.objects.create(user=self.student_user, first_name='Test', last_name='Student')
        self.client.login(username='Student', password='password')
        self.course = Course.objects.create(name='Test Course', description='Description of Test Course')

    def tearDown(self):
        Student.objects.all.delete()
        Feedback.objects.all.delete()


    # test that student can enrol themselves
    def test_student_self_enrollment(self):
        # Create  course
        course = Course.objects.create(name='New Course', description='Description of New Course')
        # Make  POST request to enroll the student in the course
        response = self.client.post(reverse('student_course_enrollment'), {'course_id': course.id})
        # Check that response redirect to the student dashboard
        self.assertEqual(response.status_code, 302)  # 302 --> status code for redirection
        self.assertRedirects(response, reverse('student'))  # Check if redirected to the student dashboard
        # Check if the student has been enrolled in the course
        enrolled_courses = self.student.courses_taken.all()
        self.assertIn(course, enrolled_courses)

    # Test that student can send feedback form correctly
    def test_feedback_form_saved(self):
        # post request to the student feedback form 
        response = self.client.post(reverse('student_feedback_form', args=[self.course.pk]), {'rating': 5, 'comment': 'Great course!'})
        # Check if the form submission redirects to the feedback confirmation page
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('student_feedback_confirmation'))
        # Check if the feedback was saved
        feedback = Feedback.objects.last()
        self.assertIsNotNone(feedback)
        self.assertEqual(feedback.student, self.student)
        self.assertEqual(feedback.course, self.course)
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comment, 'Great course!')








 





