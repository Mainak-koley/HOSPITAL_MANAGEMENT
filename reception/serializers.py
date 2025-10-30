from rest_framework import serializers
from .models import User, PatientProfile

class Userserializer(serializers.ModelSerializer):
    class Meta : 
        model = User 
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

 
class Patientserializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"