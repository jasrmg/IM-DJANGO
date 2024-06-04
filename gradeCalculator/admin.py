from django.contrib import admin
from . models import StudentInfo, Grade, DeansLister
# Register your models here.

class StudentInfoAdmin(admin.ModelAdmin):
  list_display = ['studentID', 'firstName', 'lastName', 'gender', 'section']

class GradeAdmin(admin.ModelAdmin):
  list_display = ['student_firstName', 'student_lastName', 'ap3', 'cc225', 'cc225L', 'gec_tcw', 'pelec3', 'pc223', 'pc224', 'pe4', 'gpa']
  readonly_fields = ['average']

  def student_firstName(self, obj):
    return obj.student.firstName
  student_firstName.short_description = 'First Name'

  def student_lastName(self, obj):
    return obj.student.lastName
  student_lastName.short_description = 'Last Name'

admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(DeansLister)