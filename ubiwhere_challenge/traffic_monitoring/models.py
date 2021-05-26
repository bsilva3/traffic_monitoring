from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]

#class User(AbstractUser):
#      ADMIN = 1
#      VISITOR = 2
      
#      ROLE_CHOICES = (
#          (ADMIN, 'admin'),
#          (VISITOR, 'visitor'),
#      )
#      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

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
        return self.road_id + ":\n time - " + self.time +", speed - "+ self.speed +", intensity - " + self.intensity + ", caracterization" + self.caracterization
