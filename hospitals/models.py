from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)

    def __str__(self):
       return self.name

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=50)
    sickness = models.CharField(max_length=50,null=True)

    def __str__(self):
       return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField()
    time1 = models.TimeField()

    def __str__(self):
       return f"{self.doctor.name}--{self.patient.name}"

class Prescription(models.Model):
    serial_number = models.CharField(max_length=50, unique=True)
    current_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self):
       return f"{self.serial_number}--{self.current_patient.name}"

class MedicalReport(models.Model):
    report_number = models.CharField(max_length=50, unique=True)
    current_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
       return f"{self.report_number}"

class Cashier(models.Model):
    name = models.CharField(max_length=255)
    cnic = models.CharField(max_length=15, unique=True)
    employee_id = models.CharField(max_length=50, unique=True)
    bill = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
       return f"{self.name}--{self.employee_id}"

class Test(models.Model):
    blood_group = models.CharField(max_length=10)
    current_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
       return f"{self.current_patient.name}--{self.blood_group}"
class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10,null=True)

    def __str__(self):
        return str(self.id)


class Reception(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()

    def __str__(self):
        return self.name
    
class Pharmacist(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()

    def __str__(self):
        return self.name
    
class Drugs(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    exp_date=models.DateField()
    stock=models.IntegerField()

    def __str__(self):
        return self.name

class Bill(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    