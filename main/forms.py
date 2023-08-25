from django import forms
from django.forms import ModelForm
from main.models import Project, ProjectList
from users.models import Student

class ProjectForm(ModelForm):
    # project_name = forms.CharField(required=True)
    # project_description = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5}))
    
    class Meta:
        model = Project
        fields = ['project_name', 'description']

class ProjectListForm(forms.ModelForm):
    #  projects = forms.ModelMultipleChoiceField(
    #     # queryset=Project.objects.all(),
    #     # widget=forms.CheckboxSelectMultiple
    # )
     class Meta:
         model = ProjectList
         fields=['project']
         widgets = {'projects': forms.CheckboxSelectMultiple}
     def __init__(self, *args, **kwargs):
        # Form requires a project, so assert it is instantiated with a valid initial value:
        assert 'initial' in kwargs and 'projectList' in kwargs['initial'] and type(kwargs['initial']['projectList'] is ProjectList)
        super(ProjectListForm, self).__init__(*args, **kwargs)
        projectList = kwargs['initial']['projectList']
        self.fields['projects'].queryset = projectList.project.all()
        
