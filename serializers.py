from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll_number = serializers.IntegerField()
    city = serializers.CharField(max_length=100)


# this is a fields to putting the data like as the model or textfields