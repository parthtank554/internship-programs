# from django.shortcuts import render
# import io
# from rest_framework.parsers import JSONParser
# from .serializers import StudentSerializer 
# from rest_framework.renderers import JSONRenderer
# from django.http import HttpResponse

# # Create your views here.
# def student_create(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)  # Create a stream from the JSON data
#         python_data = JSONParser().parse(stream) # Parse JSON data and convert to Python data
#         serializer = StudentSerializer(python_data)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data created successfully'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         json_data = JSONRenderer().render(serializer.errors)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer

@api_view(['POST'])
def student_create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'Data Created', 'data': serializer.data})
    return Response(serializer.errors)
