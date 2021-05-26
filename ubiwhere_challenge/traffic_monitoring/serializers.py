from django.contrib.auth.models import User, Group
from rest_framework import serializers
#from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Road, RoadSpeed
from django_filters import rest_framework as filters






class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'groups',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        #user.group.set(Group.objects.get(name=user.role))
        user.save()
        return user

class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields =  '__all__'


class RoadSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSpeed
        fields = '__all__'


class RoadSpeedFilter(filters.FilterSet):

        class Meta:
            model = RoadSpeed
            fields = {
                'caracterization' : ['exact'] #create a filter for speed readings based on the caracterization field
            }
