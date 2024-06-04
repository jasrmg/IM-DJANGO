from django import forms
from . models import StudentInfo, Grade, DeansLister

class StudentInfoForm(forms.ModelForm):
  class Meta:
    model = StudentInfo
    fields = '__all__'
    widgets = {
      'studentID': forms.TextInput(attrs={'type': 'number', 'step': '1', 'min': '0', 'style': 'appearance: textfield;'})
    }

class GradeForm(forms.ModelForm):
  class Meta:
    model = Grade
    exclude = ['average']

class DeansListerForm(forms.ModelForm):
  class Meta:
    model = DeansLister
    fields = '__all__'