from django.db import models
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.IntegerField()
    city = models.CharField(max_length=100)


# JSON Renderer - this is used to render Serialization data into JSON format which is understandable by the client / front-end.
# import JSONRenderer  # Importing JSONRenderer from rest_framework.renderers
from rest_framework.renderers import JSONRenderer

# jsondata = JSONRenderer().render(serializer.data)