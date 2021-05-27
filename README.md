# traffic_monitoring

## Installation
Download and install [Docker](https://docs.docker.com/get-docker/).  
Navigate to the root directory of this project and run

    sudo docker-compose run --rm app django-admin startproject app
    
To build and run the project:

    docker-compose up --build

To simply run:

    sudo docker-compose up
The previous command should create a postgresql database with postgis using a docker image and the django project in another container. Migrations and 'run server' are automatically executed on the django project.  

You may need to create a super user to access the django admin panel. To do so run:

    sudo docker exec -it <django container id> python manage.py makemigrations
To get the id of the container use the following command and look for a container named "ubiwhere_traffic_monitoring_app":

    sudo docker container ls
    

## Documentation
- [Swagger](https://app.swaggerhub.com/apis/bsilva3/ubiwhere_traffic_monitoring/1.0.0)
- [Postman](https://www.getpostman.com/collections/f2ee38d58cd868bd17cd) - where it is possible to run the project directly with examples already available (this collection should have a variable 'token' that automatically updates itself when a token is requested, thus updating the token for any request that is made within postman)


## Setting up
If the database is empty, groups need to be added manually using Django's administrator platform. Navigate to 'admin/', select "Group" on the left and add two users in the following order:
- First, a group named 'administrator' with permitions to add, remove, change and view roads and road speeds.
- Second, a group name 'visitor' with permitions to view roads and road speeds.

Next step should be to create users using the 'register user enpoint', as seen in the shared postman collection. Add a username, and password and a choose group (1 - administrator, 2 - visitor). Create two users of each group.  

Finally, to load the database with data use the endpoint 'upload traffic dataset' in postman. Use the [provided csv file](https://github.com/Ubiwhere/traffic_speed/blob/master/traffic_speed.csv) and upload it in postman in the header, field "Content-Disposition', and select the csv file as input. The database will be loaded with the data in that csv

## Implementation

## Database and models
A PosgtreSQL database with postgis is used to save information using [this docker image](https://hub.docker.com/r/kartoza/postgis/).
Two models were created: Road for a road segment, and RoadSpeed for speed readings. Multiple RoadSpeeds can be associated can have many RoadSpeeds associated.  Coordinates are stored by using geodjango's "pointfield". 

## CRUD operations
It is possible to create, read, change (totally or partially) and delete road segments and speed readings.  
Filters were initially being implemented by checking the most recent speed reading accross all road segments, checking its caracterization and getting all road segements whose last speed reading had the same caracterization and then allowing filtering over those roads. However it was not possible to conclude this implementation. Instead, a simple filter accross all roads were implemented.

### User groups, authentication and permissions

User groups and permitions were added using django's admin panel. Must also be manually added if database is empty.  
Authentication is done through a token that should be present in almost all of the endpoints (except the 'register user', 'get token' and 'upload traffic dataset') by providing a token in the header that identifies a user. To get this token a user must be created using 'register user' endpoint and then using the 'get token' endpoint. If using the provided postman collection, a variable 'token' should exist that will automatically update the token variable on all requests to 'get token', no copy past needed!
Permitions are verified depending on the group of the user for each endpoint.

