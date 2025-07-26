from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) # Assuming 'id' is the primary key and it is shows in the UI
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
