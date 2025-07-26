from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


    # URL is companies/<company_id>/employees/
    # This will return all employees of a specific company
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        try:
            company = Company.objects.get(pk = pk)
            employees = Employee.objects.filter(company_id=pk)
            emp_serializer = EmployeeSerializer(employees, many=True,context={'request': request})
            return Response(emp_serializer.data)
        except Company.DoesNotExist as e:
            print(e)
            return Response({"error": "Company might not exists !! try again..."}, status=404)



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
