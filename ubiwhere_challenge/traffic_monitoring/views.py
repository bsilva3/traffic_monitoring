from .models import Road, RoadSpeed
from django.shortcuts import render
from .serializers import RoadSerializer, RoadSpeedSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.



@api_view(['GET', 'POST'])
def road_segments(request):
    if request.method == 'GET':
        road = Road.objects.all()
        serializer = RoadSerializer(road, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':  # add road segment
        serializer = RoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def road_segment(request, id):
    if request.method == 'GET':
        road = Road.objects.get(id=id)
        serializer = RoadSerializer(road, many=False)
        return Response(serializer.data)
    elif request.method == 'POST':  # add road segment
        serializer = RoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)