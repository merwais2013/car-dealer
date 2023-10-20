from rest_framework import serializers
from .models import Car, Contact, CarMessage
from accounts.serializers import SimpleProfileSerializer

class SimpleCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name','location', 'fuel_type', 'model', 'price', 'body_style', 'image', 'color' ,'year']



class DetailCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = ['user']

class SimplestCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'model', 'price', 'image']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class CarMessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    car = serializers.SerializerMethodField()
    class Meta:
        model = CarMessage
        fields = ['id', 'user', 'car', 'city', 'state', 'comment']

    def get_user(self, obj):
        user = obj.user
        serializer = SimpleProfileSerializer(user, many=False)
        return serializer.data
    
    def get_car(self, obj):
        serializer = SimplestCarSerializer(obj.car, many=False)
        return serializer.data