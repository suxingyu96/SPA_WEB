from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView
from .forms import DecisionMakerSignUpForm, StudentSignUpForm,SupervisorSignUpForm
from .models import User,Student

@login_required(login_url="/login")
def home(request):
    if request.user.is_student:
        url = '/dashboard/student'
    elif request.user.is_supervisor:
        url = '/dashboard/supervisor'
    else:
        url = '/dashboard/decision_maker'
    return HttpResponseRedirect(url)
    # return render(request, 'main/home.html')
    # return redirect('/dashboard/student')

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/sign_up.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/dashboard/student')




class SupervisorSignUpView(CreateView):
    model = User
    form_class = SupervisorSignUpForm
    template_name = 'registration/sign_up.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'supervisor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/dashboard/supervisor')

class DecisionMakerSignUpView(CreateView):
    model = User
    form_class = DecisionMakerSignUpForm
    template_name = 'registration/sign_up.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'decisionmaker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/dashboard/decision_maker')