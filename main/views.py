import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
# from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from main.forms import ProjectForm, ProjectListForm
import json
from django.contrib import messages

from main.models import Project, ProjectList
from main.utils import get_max_order, get_projects_list, reorder, get_supervisors_list, get_students_list, get_current_order, sup_reorder
from users.models import Student, Supervisor
from django.views.decorators.http import require_http_methods
from algo.SPA_genetic_algorithm import SPA_genetic_algorithm

# Create your views here.
@login_required(login_url="/login")
def student(request):
    project_list = Project.objects.all()
    student = Student.objects.get(user=request.user)
    return render(request, 'dashboards/student.html',{'project_list':project_list})

@login_required(login_url="/login")
def supervisor(request):
    project_list = Project.objects.filter(supervisor=Supervisor.objects.get(user=request.user))
    return render(request, 'dashboards/supervisor.html',{'project_list':project_list})

@login_required(login_url="/login")
def decision_maker(request):
    students = Student.objects.all()
    students_and_selected_projects = {}
    for student in students:
        preferences = ProjectList.objects.filter(student=student)
        students_and_selected_projects.update({student.user_id: preferences})
    return render(request, 'dashboards/decision_maker.html',{'students_and_selected_projects': students_and_selected_projects})

@login_required(login_url="/login")
def supervisorAddProject(request):
    
    form = ProjectForm

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            supervisor = Supervisor.objects.get(user=request.user)
            project.supervisor = supervisor
            project.order = get_current_order(supervisor)
            project.save()
            return redirect('/')
    else:
        context = {'form': form}
    return render(request, 'dashboards/supervisor_add_project.html', context)

@login_required(login_url="/login")
def delete_project(request, id):
    supervisor = Supervisor.objects.get(user=request.user)
    project = Project.objects.get(id=id)
    project.delete()
    sup_reorder(supervisor)
    project_list = Project.objects.filter(supervisor=supervisor)
    return render(request, 'dashboards/partials/sup_projects_rank.html', {'project_list':project_list})
    


@login_required(login_url="/login")
def sup_sort(request):
    project_ids_order = request.POST.getlist('project_order')
    projects = []
    for idx, project_id in enumerate(project_ids_order, start=1):
        project = Project.objects.get(id=project_id)
        project.order = idx
        project.save()
        projects.append(project)

    return render(request, 'dashboards/partials/sup_projects_rank.html', {'project_list': projects})


@login_required(login_url="/login")
def update_project(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)


    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        print(request.POST)
        if form.is_valid():
            project.project_name=request.POST['project_name']
            project.description=request.POST['description']
            project.save()
            return redirect('dashboard_supervisor')

    return render(request,'dashboards/supervisor_update_project.html', {'form': form})

@login_required(login_url="/login")
def select_project(request, id):
    student = Student.objects.get(user=request.user)
    selected_project = Project.objects.get(id=id)
    # if the there are already 5 projects in the list 
    existing_projects = ProjectList.objects.filter(student=student)
    if len(existing_projects) >= 5:
        return HttpResponse("You have already selected 5 projects!")
    # if not in the list
    if not ProjectList.objects.filter(project=id, student=student).exists():
        ProjectList.objects.create(
            project = selected_project,
            student = student,
            order = get_max_order(student)
        )
    selected_projects = ProjectList.objects.filter(student=student)
    return render(request, 'dashboards/student_selected_projects.html',{'preference_list':selected_projects})

@login_required(login_url="/login")
def student_selected_projects(request):
    student = Student.objects.get(user=request.user)
    if not ProjectList.objects.filter(student=student).exists():
        return HttpResponse('You haven\'t select any project!')
    project_list = ProjectList.objects.filter(student=student)
    if request.method == 'POST':
        projects_rank=request.POST.getlist('project_order')
        project_list.projects.clear()
        for project_id in projects_rank:
            project = Project.objects.get(id=project_id)
            print(projects_rank)
            project_list.projects.add(project)
            print('reset the ordering..')
        project_list.save()
    # preference_list = project_list.projects.all()
    return render(request, 'dashboards/student_selected_projects.html',{'preference_list':project_list})
    

@login_required(login_url="/login")
def sort(request):
    project_ids_order = request.POST.getlist('project_order')
    print("print here",project_ids_order)
    projects = []
    for idx, project_id in enumerate(project_ids_order, start=1):
        projectList = ProjectList.objects.get(id=project_id)
        projectList.order = idx
        projectList.save()
        projects.append(projectList)

    return render(request, 'dashboards/partials/projects_rank.html', {'preference_list': projects})

@login_required(login_url="/login")
def student_rank(request):
    # get selected projects
    projects_rank=request.POST.getlist('project_order')
    print(projects_rank)
    student = Student.objects.get(user=request.user)
    projects_list = ProjectList.objects.get(student=student)
    form = ProjectListForm(instance=projects_list)
    preference_list = projects_list.projects.all()

    return render(request,'dashboards/student_selected_projects.html', {'form': form})


@require_http_methods(['DELETE'])
@login_required
def student_delete_project(request, id):
    ...
    student = Student.objects.get(user=request.user)
    ProjectList.objects.get(id=id).delete()
    reorder(student)
    project_list = ProjectList.objects.filter(student=student)
    return render(request, 'partials/projects_rank.html', {'preference_list':project_list})

@login_required
def allocation(request):
    students = Student.objects.all()
    students= {}
    for student in students:
        preferences = ProjectList.objects.filter(student=student)
        students.update({student: preferences})

    projects = get_projects_list()
    
    students = get_students_list()
    for stu in students:
        print(stu.getStudentID())
        print(stu.getProjectList())

    supervisors = get_supervisors_list()

    pool_size = 200
    mutate_rate = 0.01
    crossover_rate = 0.8
    res = SPA_genetic_algorithm(students, projects, supervisors,pool_size, mutate_rate, crossover_rate).run(False)
    res_list = {}
    count = 1
    for individual in res:
        print("res: ", individual)
        result = {}
        solution = []
        genes = individual.getGenes()
        for i in range(len(students)):
            student = students[i].getStudentID()
            project = genes[i]
            result.update({student: project})
            supervisors = individual.SelectedSupervisorsAndProjects
        solution.append(result)
        solution.append(individual)
        solution.append(supervisors)
        res_list.update({count: solution})
        count += 1
    print('len of res:', len(res_list))

    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="results.csv"'  
    writer = csv.writer(response)
    for order,solution in res_list.items():
        writer.writerow(['Solution', order ])
        writer.writerow (['Student', 'Project'])
        result = solution[0]
        for student,project in result.items():
             writer.writerow ([student, project])
        statistics = solution[1]
        writer.writerow(['Students Satisfaction:', statistics])    
        supervisors = solution[2]
        writer.writerow (['Supervisors', 'Num of assigned students'])
        for sup, projects in supervisors.items():
            writer.writerow ([sup, len(projects)])
        writer.writerow ([])

    return response


    return render(request, 'dashboards/allocation_page.html',{'results': res_list})

def export_result(request):
    pass 