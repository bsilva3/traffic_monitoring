import csv
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Road, RoadSpeed
from django.http import Http404
from .serializers import RoadSerializer, RoadFilter, RoadSpeedSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import permission_required
from io import StringIO
from django.contrib.gis.geos import Point
from django_filters import rest_framework as filters


# Create your views here.

class RoadList(APIView):
    """
    List all road segments, or create a new road segment.
    """
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        if not request.user.has_perm('traffic_monitoring.view_road'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        roads = Road.objects.all()
        serializer = RoadSerializer(roads, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.user.has_perm('traffic_monitoring.add_road'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        if not request.user.has_perm('traffic_monitoring.view_road'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road = self.get_object(id)
        serializer = RoadSerializer(road)
        return Response(serializer.data)

    #@permission_required('traffic_monitoring.change_road') 
    def patch(self, request, id, format=None):
        if not request.user.has_perm('traffic_monitoring.change_road'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road = self.get_object(id)
        serializer = RoadSerializer(road, data=request.data, partial=True)#we may not have all fields here (partial update of fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        if not request.user.has_perm('traffic_monitoring.delete_road'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road = self.get_object(id)
        road.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoadSpeedList(APIView):
    """
    List all road speed readings segments or create a new one
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        if not request.user.has_perm('traffic_monitoring.view_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road_speeds = RoadSpeed.objects.all()
        serializer = RoadSpeedSerializer(road_speeds, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        if not request.user.has_perm('traffic_monitoring.change_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        if not request.user.has_perm('traffic_monitoring.view_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        if not request.user.has_perm('traffic_monitoring.view_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road_speed = self.get_object(road_id, time)
        serializer = RoadSpeedSerializer(road_speed)
        return Response(serializer.data)

    def patch(self, request, road_id, time, format=None):
        if not request.user.has_perm('traffic_monitoring.change_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road_speed = self.get_object(road_id, time)
        serializer = RoadSpeedSerializer(road_speed, data=request.data,partial=True) #we may not have all fields here (partial update of fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, road_id, time, format=None):
        if not request.user.has_perm('traffic_monitoring.delete_roadspeed'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        road_speed = self.get_object(road_id, time)
        road_speed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoadSegmentList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    #simply get all roads and filter them
    queryset = Road.objects.all()
    serializer_class = RoadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', 'speed')
    filterset_class = RoadFilter

    ## Initially trying to get roads whose last reading was the same as the last speed reading registered and filter on those roads
    #first get latest inserted caracterization
    #road_speed = RoadSpeed.objects.latest('time')
    #print(road_speed)
    #road_speed_set = RoadSpeed.objects.filter(caracterization=road_speed.caracterization).values_list('road_id') #get list of roads 
    #print(road_speed_set)
    #queryset = Road.objects.filter(id__in=road_speed_set)


class UserCreateAPIView(generics.CreateAPIView):
    '''
    Create a new user and assign a group to it (username, pass and user group id)
    '''
    permission_classes = (AllowAny,) #allow anonymous users to create users
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    '''
    Upload a csv file containing the following columns: ID,Long_start,Lat_start,Long_end,Lat_end,Length,Speed.
    These will load the database with data regarding road segments and road speed readings
    '''
    parser_classes = (FileUploadParser,)
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
        # we cannot use bulk create on RoadSpeed because it does not call save(), which is necessary to create the intensisty, time stamp and caracterization
        for rs in roads_speed:
            rs.save()
        return Response(status=204)