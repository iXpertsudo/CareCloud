from django.db import models

# Create your models here.

class Patient(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=50)
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    dateregistered = models.DateTimeField()
    medicalhistory = models.TextField(blank=True)

    def __str__(self):
        return self.firstname+ " "  +self.lastname
    


class Doctor(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=15)
    profession = models.CharField(max_length=50)
    email = models.EmailField(unique=True,  default="example@example.com")
    years_of_experience = models.PositiveIntegerField(default=0)


    
    def __str__(self):
      return self.firstname + " " + self.lastname + " - " + self.profession
    


class MyAppointments(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    date = models.DateTimeField()
    department = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    message= models.TextField()



    def _str_(self):
        return self.name 








class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"
















