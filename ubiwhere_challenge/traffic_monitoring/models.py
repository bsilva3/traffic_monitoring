#from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


# Create your models here.


class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]

class Road(models.Model):
    id = models.IntegerField(primary_key=True)
    coord_start = models.PointField()
    coord_end = models.PointField()
    length = models.DecimalField(max_digits=15, decimal_places=7)
    


class RoadSpeed(models.Model):
    road_id = models.ForeignKey(Road, on_delete=models.CASCADE)
    time = models.DateTimeField()
    speed = models.FloatField()
    intensity = models.IntegerField()
    caracterization = models.CharField(max_length=8)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['time', 'road_id'], name="unique-reading") #one speed reading at a given time for a given road
            ]
    
    #def save(self, *args, **kwargs):
        
    #    super(RoadSpeed, self).save(*args, **kwargs)

