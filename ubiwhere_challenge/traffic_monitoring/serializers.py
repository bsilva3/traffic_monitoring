from rest_framework import serializers
#from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Road, RoadSpeed
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields =  '__all__'


class RoadSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSpeed
        fields = '__all__'