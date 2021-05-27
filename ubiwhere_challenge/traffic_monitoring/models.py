import logging
from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
#from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions
from django.core.management import call_command

def update_permissions(schema, group):
    call_command('update_permissions')

def add_group_permissions(apps, schema_editor):
    logger = logging.getLogger(__name__)

    for app_config in apps.get_app_configs():
        create_permissions(app_config, apps=apps, verbosity=0)

    Group = apps.get_model("auth","Group")
    Permission = apps.get_model("auth","Permission")

    # create groups on migrate (but does not work, need to be created manually)
    group, created = Group.objects.get_or_create(name='administrator')
    if created:
        permissions_qs = Permission.objects.filter(
            codename__in=['traffic_monitoring.add_road',
                         'traffic_monitoring.change_road',
                         'traffic_monitoring.delete_road',
                         'traffic_monitoring.view_road',
                         'traffic_monitoring.view_roadspeed',
                         'traffic_monitoring.add_roadspeed',
                         'traffic_monitoring.change_roadspeed',
                         'traffic_monitoring.delete_roadspeed',]
        )
        group.permissions = permissions_qs
        group.save()
        logger.info('Group Admin Created')

    # create visitor group
    group, created = Group.objects.get_or_create(name='administrator')
    if created:
        permissions_qs = Permission.objects.filter(
            codename__in=['traffic_monitoring.view_road', 'traffic_monitoring.view_roadspeed',]
        )
        group.permissions = permissions_qs
        group.save()
        logger.info('Group visitor Created')

# Create your models here.

class Migration(migrations.Migration):

    dependencies = [
        ('traffic_monitoring', '0001_initial'),
    ]

    operations = [
        CreateExtension('postgis'),
        #migrations.RunPython(update_permissions, reverse_code=migrations.RunPython.noop),#supposed to create groups, but does not work
        #migrations.RunPython(add_group_permissions),
    ]

#represents a road segment. Coordinates of the beginning and ending of street are represented using 2 PointFields
class Road(models.Model):
    id = models.IntegerField(primary_key=True)
    coord_start = models.PointField()
    coord_end = models.PointField()
    length = models.DecimalField(max_digits=15, decimal_places=7)
    

# This model represents a road segment's speed data and auto fills the time stamp using the current time, and the intensity and caracterization fields
# as specified
class RoadSpeed(models.Model):
    road_id = models.ForeignKey(Road, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    speed = models.FloatField()
    intensity = models.IntegerField(editable=False, validators=[MinValueValidator(0), MaxValueValidator(2)]) # intensity should be between 0 and 2
    CARCT_CHOICES = (
        ('H', 'High'),
        ('M', 'Moderate'),
        ('L', 'Low')
    )
    caracterization = models.CharField(editable=False, max_length=9, choices=CARCT_CHOICES)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['time', 'road_id'], name="unique-reading") #one speed reading at a given time for a given road
            ]
    
    def save(self, *args, **kwargs):
        if self.speed <= 20.0:
            self.intensity = 2
            self.caracterization = 'H'
        elif self.speed > 20.0 and self.speed <= 50.0:
            self.intensity = 1
            self.caracterization = 'M'
        elif self.speed > 50.0:
            self.intensity = 0
            self.caracterization = 'L'
        super(RoadSpeed, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}:\n time - {1}, speed - {2}, intensity - {3}, caracterization".format(self.road_id, self.time, self.speed, self.intensity, self.caracterization)
