from functools import partial
from os import read
from .models import Road, RoadSpeed
from django.http import Http404
from .serializers import RoadSerializer, RoadSpeedSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated  # <-- Here
import csv
from io import StringIO
from django.contrib.gis.geos import Point


# Create your views here.

class RoadList(APIView):
    """
    List all road segments, or create a new road segment.
    """
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        roads = Road.objects.all()
        serializer = RoadSerializer(roads, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoadDetail(APIView):
    """
    Retrieve, update or delete a road segment.
    """
    permission_classes = (IsAuthenticated,) 
    def get_object(self, id):
        try:
            return Road.objects.get(id=id)
        except Road.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        road = self.get_object(id)
        serializer = RoadSerializer(road)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        road = self.get_object(id)
        serializer = RoadSerializer(road, data=request.data, partial=True)#we may not have all fields here (partial update of fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        road = self.get_object(id)
        road.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoadSpeedList(APIView):
    """
    List all road speed readings segments or create a new one
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        road_speeds = RoadSpeed.objects.all()
        serializer = RoadSpeedSerializer(road_speeds, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = RoadSpeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoadSpeedSegmentList(APIView):
    """
    List all road speed readings for a given road segment
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, road_id, format=None):
        try:
            road_speeds = RoadSpeed.objects.filter(road_id=road_id) #we may have multiple speed readings for a single road
        except RoadSpeed.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoadSpeedSerializer(road_speeds, many=True)
        return Response(serializer.data)
    

class RoadSpeedSegmentDetail(APIView):
    """
    Retrieve, update or delete a specific road speed reading (for a given road and time).
    """
    permission_classes = (IsAuthenticated,)
    def get_object(self, road_id, time):
        try:
            return RoadSpeed.objects.get(road_id=road_id, time=time)
        except RoadSpeed.DoesNotExist:
            raise Http404

    def get(self, request, road_id, time, format=None):
        road_speed = self.get_object(road_id, time)
        serializer = RoadSpeedSerializer(road_speed)
        return Response(serializer.data)

    def patch(self, request, road_id, time, format=None):
        road_speed = self.get_object(road_id, time)
        serializer = RoadSpeedSerializer(road_speed, data=request.data,partial=True) #we may not have all fields here (partial update of fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, road_id, time, format=None):
        road_speed = self.get_object(road_id, time)
        road_speed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        file = request.FILES['file'] 
        csvf = StringIO(file.read().decode())
        reader = csv.reader(csvf, delimiter=',')
        roads = []
        roads_speed = []
        for r in reader:
            if (len(r)) == 7 and r[0] != 'ID': #select only rows with content to save
                #print(r)
                road = Road(id=int(r[0]), coord_start=Point(float(r[1]), float(r[2])), coord_end=Point(float(r[3]), float(r[4])), length=float(r[5]))
                roads.append(road)
                roads_speed.append(RoadSpeed(road_id=road, speed=float(r[6])))

        Road.objects.bulk_create(roads, len(roads))
        #RoadSpeed.objects.bulk_create(roads_speed, len(roads_speed))
        # we cannot use bulk create on RoadSpeed because it does not call save(), which is necessary
        for rs in roads_speed:
            rs.save()
        

        return Response(status=204)