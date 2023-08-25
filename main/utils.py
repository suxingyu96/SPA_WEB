from django.db.models import Max
from main.models import Project, ProjectList
from algo.project import Project as algo_project
from algo.supervisor import Supervisor as algo_supervisor
from algo.student import Student as algo_student
from users.models import Supervisor, Student


def get_max_order(student) -> int:
    existing_projects = ProjectList.objects.filter(student=student)
    if not existing_projects.exists():
        return 1
    else:
        current_max = existing_projects.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1

def get_current_order(supervisor) -> int:
    uploaded_projects = Project.objects.filter(supervisor=supervisor)
    num = len(uploaded_projects)
    return num+1

def sup_reorder(supervisor):
    existing_projects = Project.objects.filter(supervisor=supervisor)
    if not existing_projects.exists():
        return
    number_of_projects = existing_projects.count()
    new_ordering = range(1, number_of_projects+1)
    
    for order, project in zip(new_ordering, existing_projects):
        project.order = order
        project.save()



def reorder(student):
    existing_projects = ProjectList.objects.filter(student=student)
    if not existing_projects.exists():
        return
    number_of_projects = existing_projects.count()
    new_ordering = range(1, number_of_projects+1)
    
    for order, project in zip(new_ordering, existing_projects):
        project.order = order
        project.save()

def get_projects_list() -> list:
    projects = Project.objects.all()
    projects_list = {}
    for project in projects:
        project_id = project.id
        sup = project.supervisor.user_id
        new_project = algo_project(project_id, sup)
        # projects_list.append(new_project)
        projects_list.update({project_id:new_project})
    return projects_list


def get_supervisors_list() -> list:
    supervisors = Supervisor.objects.all()
    supervisors_list = {}
    for supervisor in supervisors:
        sup_name = supervisor.user.username
        sup_id = supervisor.user_id
        sup_cap = int(supervisor.capacity)
        projects = Project.objects.filter(supervisor=supervisor)
        project_list=[]
        for project in projects:
            project_list.append(project.id)
        sup = algo_supervisor(sup_name, sup_id, project_list, sup_cap)
        supervisors_list.update({sup_id: sup})
    return supervisors_list

def get_students_list() -> list:
    students = Student.objects.all()
    student_list = []
    for student in students:
        stu_id = student.user_id
        stu_prefereces = ProjectList.objects.filter(student=student)
        preferences = []
        for project in stu_prefereces:
            project_id = project.project_id
            preferences.append(project_id)
        stu = algo_student(stu_id, stu_id, preferences)
        student_list.append(stu)
    
    return student_list