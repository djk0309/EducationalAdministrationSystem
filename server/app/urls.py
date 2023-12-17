import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('grade/<str:module>/', app.views.GradesView.as_view()),
    path('project/<str:module>/', app.views.ProjectsView.as_view()),
    path('student/<str:module>/', app.views.StudentsView.as_view()),
    path('teacher/<str:module>/', app.views.TeachersView.as_view()),
    path('work/<str:module>/', app.views.WorksView.as_view()),
    path('select/<str:module>/', app.views.SelectsView.as_view()),
    path('score/<str:module>/', app.views.ScoresView.as_view()),
]