from django.db import models

from users.models import Student, Supervisor

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='projects', through='ProjectList')
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
    	return self.project_name
    
    
    


class ProjectList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']
    
    def __str__(self):
    	return str(self.project.project_name)
    