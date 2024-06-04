from . import views
from django.urls import path

urlpatterns = [
  path('', views.studentInfo_view, name='studentInfo'),
  path('grade/', views.grades_view, name='grade'),
  path('dl/', views.dl_view, name='dl'),
]
