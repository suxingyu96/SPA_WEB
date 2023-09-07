from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from datetime import datetime
from .models import DecisionMaker, Student, User, Supervisor

class StudentSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    student_id = forms.CharField(required=True)
    course_id = forms.CharField(required=True)
  
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.student_id = self.cleaned_data.get('student_id')
        student.course_id = self.cleaned_data.get('course_id')
        student.is_student = True
        student.last_login = datetime.now()
        student.save()
        return student


class SupervisorSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    # capacity = forms.CharField(required=True)
    capacity = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.save()
        supervisor = Supervisor.objects.create(user=user)
        supervisor.capacity = self.cleaned_data.get('capacity')
        supervisor.is_supervisor = True
        supervisor.last_login = datetime.now()
        # user.save()
        # supervisor = Supervisor.objects.create(user=user)
        supervisor.save()

        return supervisor
    
class DecisionMakerSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.last_login = datetime.now()
        user.save()
        decision_maker = DecisionMaker.objects.create(user=user)
        decision_maker.save()

        return decision_maker