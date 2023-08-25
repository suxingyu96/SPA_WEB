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
        user.student_id = self.cleaned_data.get('student_id')
        user.course_id = self.cleaned_data.get('course_id')
        user.is_student = True
        user.last_login = datetime.now()
        user.save()
        student = Student.objects.create(user=user)
        return user


class SupervisorSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    capacity = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.capacity = self.cleaned_data.get('capacity')
        user.is_supervisor = True
        user.last_login = datetime.now()
        user.save()
        supervisor = Supervisor.objects.create(user=user)
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