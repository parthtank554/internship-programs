from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer    #this is for the importing the user table for the serializer
from rest_framework.renderers import JSONRenderer     #this is for the rendering the data in json format
from django.http import HttpResponse, JsonResponse

# Models Objects - single Student Data 
# creating the function base View

# this is the Queryset for the student table for seperate records
def student_detail(request, pk):
    stu = Student.objects.get(id = pk)  # Assuming you want to get the student with id=1
    serializer = StudentSerializer(stu)  # Serializing the student object

    json_data = JSONRenderer().render(serializer.data)  # Rendering the serialized data to JSON
    return HttpResponse(json_data, content_type='application/json')  # Returning the JSON response

    # return JsonResponse(serializer.data, safe=True)  # Returning the JSON response using JsonResponse

# this Query - Set for the student table for all records
# this is the Queryset for the student table for seperate records
def student_list(request):
    stu = Student.objects.all()  # Fetching all student records
    serializer = StudentSerializer(stu, many=True)  # Serializing the student object

    json_data = JSONRenderer().render(serializer.data)  # Rendering the serialized data to JSON
    return HttpResponse(json_data, content_type='application/json')  # Returning the JSON response
    # return JsonResponse(serializer.data, safe=False)  # Returning the JSON response using JsonResponse