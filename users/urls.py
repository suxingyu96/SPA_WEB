from django.urls import path
from . import views
# from .views import home, StudentSignUpView,SupervisorSignUpView

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('sign_up/student', views.StudentSignUpView.as_view(), name='student_signup'),
    path('sign_up/supervisor', views.SupervisorSignUpView.as_view(), name='supervisor_signup'),
    ]