from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class StudentInfo(models.Model):
    studentID = models.IntegerField('Student ID', primary_key=True, unique=True)
    firstName = models.CharField('First Name', max_length=100, null=False, blank=False)
    lastName = models.CharField('Last Name', max_length=100, null=False, blank=False) 
    genderChoices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    ]
    gender = models.CharField(max_length=10, choices=genderChoices, null=False, blank=False)
    # statusChoices = [
    #     ('enrolled', 'Enrolled'),
    #     ('not_enrolled', 'Not Enrolled')
    # ]
    # enrollment_status = models.CharField('Enrollment Status', max_length=20, choices=statusChoices)
    section = models.CharField(max_length=25, null=False, blank=False, choices=[
        ('BSIT 2-A Algorithm', 'BSIT 2-A Algorithm'),
        ('BSIT 2-B Pseudocode', 'BSIT 2-B Pseudocode')
    ])

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Grade(models.Model):
    gradeID = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    # subjects:
    ap3 = models.DecimalField('AP 3', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    cc225 = models.DecimalField('CC 225', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    cc225L = models.DecimalField('CC 225 L', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    gec_tcw = models.DecimalField('GEC-TCW', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    pelec3 = models.DecimalField('P-Elec 3', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    pc223 = models.DecimalField('PC 223', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    pc224 = models.DecimalField('PC 224', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)
    pe4 = models.DecimalField('PE 4', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)

    average = models.DecimalField('Average', max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False)

    @property
    def unit_weight(self):
        return {
            'ap3': Decimal('3.0'),
            'cc225': Decimal('2.0'),
            'cc225L': Decimal('3.0'),
            'gec_tcw': Decimal('3.0'),
            'pelec3': Decimal('3.0'),
            'pc223': Decimal('3.0'),
            'pc224': Decimal('3.0'),
            'pe4': Decimal('2.0'),
        }

    @property
    def gpa(self):
        unit_weight = self.unit_weight
        total_units = sum(unit_weight.values())
        total_points = (
            self.ap3 * unit_weight['ap3'] +
            self.cc225 * unit_weight['cc225'] +
            self.cc225L * unit_weight['cc225L'] +
            self.gec_tcw * unit_weight['gec_tcw'] +
            self.pelec3 * unit_weight['pelec3'] +
            self.pc223 * unit_weight['pc223'] +
            self.pc224 * unit_weight['pc224'] +
            self.pe4 * unit_weight['pe4']
        )
        gpa = total_points / total_units
        return round(gpa, 3)

    def save(self, *args, **kwargs):
        self.average = self.gpa
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.student)

class DeansLister(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    average_grade = models.DecimalField(max_digits=5, decimal_places=2)
    section = models.CharField(max_length=25, choices=[
        ('BSIT 2-A Algorithm', 'BSIT 2-A Algorithm'),
        ('BSIT 2-B Pseudocode', 'BSIT 2-B Pseudocode')
    ])

    def __str__(self):
        return str(self.student)

    @classmethod
    def update_dl(cls):
        cls.objects.all().delete()
        for grade in Grade.objects.all():
            gpas = [grade.ap3, grade.cc225, grade.cc225L, grade.gec_tcw, grade.pelec3, grade.pc223, grade.pc224, grade.pe4]
            # Check if the student meets the GPA criteria for being on the Dean's List
            if all(g <= 2.5 for g in gpas) and grade.gpa <= 1.75:
                cls.objects.create(
                    student=grade.student,
                    average_grade=grade.gpa,  # Ensure this is the GPA
                    section=grade.student.section
                )

