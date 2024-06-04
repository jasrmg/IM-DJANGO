from django.dispatch import receiver
from django.shortcuts import render, redirect

from gradeCalculator.models import Grade, DeansLister
from . forms import StudentInfoForm, GradeForm
from django.contrib import messages

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.
def studentInfo_view(request):
  if request.method == "POST":
    form = StudentInfoForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Student added!')
      return redirect('studentInfo')
    else:
      messages.error(request, 'There is an error in submitting the form!')
  else:
    form = StudentInfoForm()

  context = {
    'title': 'Student Info',
    'form': form
  }
  return render(request, 'gradeCalculator/studentInfo.html', context)

def grades_view(request):
  if request.method == 'POST':
    form = GradeForm(request.POST)
    if form.is_valid():
      student_id = form.cleaned_data['student'].studentID
      try:
        grade_entry = Grade.objects.get(student_id=student_id)
        #update or create a new grade entry
        grade_entry.ap3 = form.cleaned_data['ap3']
        grade_entry.cc225 = form.cleaned_data['cc225']
        grade_entry.cc225L = form.cleaned_data['cc225L']
        grade_entry.gec_tcw = form.cleaned_data['gec_tcw']
        grade_entry.pelec3 = form.cleaned_data['pelec3']
        grade_entry.pc223 = form.cleaned_data['pc223']
        grade_entry.pc224 = form.cleaned_data['pc224']
        grade_entry.pe4 = form.cleaned_data['pe4']
        grade_entry.save()
        messages.success(request, 'Grades updated!')
        
      except Grade.DoesNotExist:
        form.save()
        messages.success(request, 'Grades added!')
      DeansLister.update_dl()
      return redirect('grade')
  else:
    form = GradeForm()
  context = {
    'title': 'Grades',
    'form': form
  }
  return render(request, 'gradeCalculator/grade.html', context)


def dl_view(request):
    deans_list = DeansLister.objects.all().order_by('average_grade')

    context = {
        'title': 'Deans Lister',
        'deans_list': deans_list
    }
    return render(request, 'gradeCalculator/dl.html', context)

