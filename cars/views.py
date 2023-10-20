from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Car,Contact, CarMessage
from .serializers import DetailCarSerializer, SimpleCarSerializer, ContactSerializer, CarMessageSerializer


@api_view(['GET'])
def get_cars_by_query_params(request):
    pagination_class = PageNumberPagination()
    query = request.query_params.get('keyword', None)
    if query == None:
        query = ''
    cars = Car.objects.filter(Q(name__icontains=query) | 
                              Q(model__icontains=query)|
                              Q(location__icontains=query)|
                              Q(color__icontains=query) |
                              Q(year__icontains=query)|
                              Q(owner__icontains=query)|
                              Q(price__icontains=query)).order_by('id')
    
    page = pagination_class.paginate_queryset(cars, request)
    print(page)
    if page is not None:
        serializer = SimpleCarSerializer(page, many=True)
        return pagination_class.get_paginated_response(serializer.data)

    serializer = SimpleCarSerializer(cars, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_cars_by_searching(request):
    query = request.GET.get('keyword', None)
    if query == None:
        query = ''
    cars = Car.objects.filter(Q(name__icontains=query) | 
                              Q(model__icontains=query)|
                              Q(location__icontains=query)|
                              Q(color__icontains=query) |
                              Q(year__icontains=query)|
                              Q(owner__icontains=query)|
                              Q(price__icontains=query))
    serializer = SimpleCarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cars_by_multiple_serach(request):
    model = request.query_params.get('model', None)
    location = request.query_params.get('location', None)
    year = request.query_params.get('year', None)
    price = request.query_params.get('price', None)
    cars = Car.objects.filter(
                              Q(model__icontains=model) &
                              Q(location__icontains=location) &
                              Q(year__icontains=year) &
                              Q(price=price))
    if cars:
        serializer = SimpleCarSerializer(cars, many=True)
        return Response(serializer.data)
    message = {"Detail": "Car with the given information has not found."}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def latest_cars(request):
    cars = Car.objects.filter(year__gte=2010)[0:5]
    serializer = SimpleCarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_car(request, pk):
    car = Car.objects.get(id=pk)
    serializer = DetailCarSerializer(car, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def contact(request):
    data = request.data
    msg = Contact.objects.create(
        full_name=data['full_name'],
        email=data['email'],
        subject=data['subject'],
        number=data['number'],
        message=data['message']
    )
    serializer = ContactSerializer(msg, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, pk):
    data = request.data
    user = request.user.profile
    car = Car.objects.get(id=pk)
    already_exists = car.carmessage_set.filter(user=user).exists()
    if already_exists:
        content = {'details': 'Message for this car already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    message = CarMessage.objects.create(
        user=user,
        car=car,
        city=data['city'],
        state=data['state'],
        comment=data['comment'],
    )
    serializer = CarMessageSerializer(message, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox(request):
    user = request.user.profile
    car_messages = user.message.all()
    serializer = CarMessageSerializer(car_messages, many=True)
    return Response(serializer.data)
