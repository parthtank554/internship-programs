# from django.shortcuts import render
# import requests
# import io
# from rest_framework.renderers import JSONRenderer
# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# from .models import Student
# from .serializers import StudentSerializer
# import json
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# @api_view(['GET', 'POST'])
# def student_api(request):
#     if request.method == 'GET':
#         # Logic to handle GET request
#         json_data = requests.body
#         stream = io.BytesIO(json_data)
#         python_data = JSONParser().parse(stream)
#         id = python_data.get('id', None)
#         if id is not None: 
#             stu = Student.objects.get(id=id)
#             serializer = StudentSerializer(stu)
#             json_data = JSONRenderer().render(serializer.data)
#             return HttpResponse(json_data, content_type='application/json')
#         stu = Student.objects.all()
#         serializer = StudentSerializer(stu, many=True)
#         json_data = JSONRenderer().render(serializer.data)
#         return HttpResponse(json_data, content_type='application/json')

#     if request.method == 'POST':
#         # data = json.loads(request.body)
#         stream = io.BytesIO(request.body)
#         python_data = JSONParser().parse(stream)
#         serializer = StudentSerializer(data = python_data)    
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data created successfully',}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         json_data = JSONRenderer().render(serializer.errors)
#         return HttpResponse(json_data, content_type='application/json')

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Student
from .serializers import StudentSerializer
import io

@api_view(['GET', 'POST'])
def student_api(request):
    if request.method == 'GET':
        try:
            stream = io.BytesIO(request.body)
            if stream.getbuffer().nbytes != 0:
                python_data = JSONParser().parse(stream)
                student_id = python_data.get('id', None)

                if student_id is not None:
                    try:
                        stu = Student.objects.get(id=student_id)
                        serializer = StudentSerializer(stu)
                        json_data = JSONRenderer().render(serializer.data)
                        return HttpResponse(json_data, content_type='application/json')
                    except Student.DoesNotExist:
                        return JsonResponse({'error': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Invalid GET data: {str(e)}'}, status=400)

        # Return all students if no ID
        stu = Student.objects.all()
        print(stu)
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'POST':
        try:
            stream = io.BytesIO(request.body)
            python_data = JSONParser().parse(stream)

            serializer = StudentSerializer(data=python_data)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'Data created successfully'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        except Exception as e:
            return JsonResponse({'error': f'Invalid POST data: {str(e)}'}, status=400)
