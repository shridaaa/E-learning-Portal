from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class TeacherProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control'
                   }
                )
            ) 
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user.email:
            self.fields['email'].initial = self.instance.user.email  # Populate email field with existing email in users

    def save(self, commit=True):
        # Save the form instance without committing to the database
        instance = super().save(commit=False)
        # Update the related user's email attribute with the new email value from the form
        instance.user.email = self.cleaned_data['email']
        # Save the related user object
        instance.user.save()
        if commit:
            instance.save()
        return instance

class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(
            widget=forms.EmailInput(
                attrs={'class': 'form-control'
                    }
                    )
                ) 

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user.email:
            self.fields['email'].initial = self.instance.user.email  # Populate email field with existing email in users

    def save(self, commit=True):
        # Save the form instance without committing to the database
        instance = super().save(commit=False)
        # Update the related user's email attribute with the new email value from the form
        instance.user.email = self.cleaned_data['email']
        # Save the related user object
        instance.user.save()
        if commit:
            instance.save()
        return instance
        



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']


class EditStudentForm(forms.Form):
    student = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all students
        all_students = Student.objects.all()
        # Populate the choices for the dropdown menu
        choices = [(student.id, student.user) for student in all_students]
        self.fields['student'].choices = choices


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['name', 'file']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_teacher', 'is_student')