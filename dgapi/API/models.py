from django.db import models

# Crating Models for the application

# Company Model
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    about = models.TextField()  
    type = models.CharField(
        max_length=50,
        choices=(
            ('IT', 'Information Technology'),
            ('Finance', 'Finance'),
            ('Healthcare', 'Healthcare'),
            ('Education', 'Education'),
            ('Retail', 'Retail'),
            ('Manufacturing', 'Manufacturing'),
            ('Other', 'Other'),
    )),
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Employee Model

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    about = models.TextField()
    position = models.CharField(max_length=50, choices=(
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Analyst', 'Analyst'),
        ('Other', 'Other'),
    ))
    active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
