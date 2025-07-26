from rest_framework import serializers
from .models import Company, Employee 

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    company_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Company
        # fields = ['id', 'name', 'location', 'about', 'type', 'date', 'active']     #this is for the seperate fields 
        fields = "__all__"    #This is for the all fields in the model

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    employee_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Employee
        fields = "__all__"    #This is for the all fields in the model
