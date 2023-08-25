from django.contrib import admin
from users.models import DecisionMaker, User,Student,Supervisor


admin.site.register(User)

admin.site.register(Student)

admin.site.register(Supervisor)

admin.site.register(DecisionMaker)
