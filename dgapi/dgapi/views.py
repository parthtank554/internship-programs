from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

# function base View
def home_page(request):
    print("This is the home page view")
    # return HttpResponse("<h1>Welcome to the home page!</h1> " \
    # "<p>This is a simple Django application.</p>")
    friends = ['jay','umang']
    return JsonResponse(friends, safe=False)