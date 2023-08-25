from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('student', views.student, name = 'dashboard_student'),
    path('student/project-rank-list', views.student_rank, name = 'student_rank'),
    path('student/selected_projects', views.student_selected_projects, name = 'student_selected_projects'),
    path('student/delete_project/<int:id>', views.student_delete_project, name = 'student_delete_project'),
    path('supervisor', views.supervisor, name = 'dashboard_supervisor'),
    path('supervisor/sort/', views.sup_sort, name = 'sup_sort'),
    path('supervisor/addproject', views.supervisorAddProject, name = 'supervisor_add_project'),
    path('project-delete/<int:id>', views.delete_project, name='delete_project'),
    path('project-update/<int:id>', views.update_project, name='update_project'),
    path('project-select/<int:id>', views.select_project, name='select_project'),
    path('student_delete-project/<int:id>/', views.student_delete_project, name='student_delete-project'),
    path('sort/', views.sort, name='sort'),
    path('decision_maker', views.decision_maker, name='decision_maker'),
    path('allocation', views.allocation, name='allocation'),
    # path('export_result/<list:solution>', views.export_result, name='export_result'),
#     path('home', views.home, name = 'home'),
#     path('sign-up', views.sign_up, name = 'sign_up'),
]
