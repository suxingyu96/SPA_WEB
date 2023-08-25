from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model
from django_mysql.models import ListCharField




class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    # preference_list =  ListCharField(
    #     base_field=CharField(max_length=10),
    #     size=5,
    #     max_length=(5 * 11), 
    # )
    # preference_list = models.OneToOneField(ProjectList, on_delete=models.CASCADE, primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
    	return self.user.username   
        



class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)
    capacity = models.CharField(max_length=100)


    def __str__(self):
    	return self.user.username
    

class DecisionMaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
    	return self.user.username