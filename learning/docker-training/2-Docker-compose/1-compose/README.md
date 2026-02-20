# Docker Compose exercises

## About this exercise set

> To help the users of this exercise to learn how to use docker and where to get help when they are stuck in the real world, I have tried to create exercises that forces the user to look in documentation and experiment.

> **This means, that the exercise set is not a simple copy & paste exercise**

A web application for adding numbers with a centralized hitcounter.

## Files

### `addition-server/addition.py`

```python
# install package web.py from pip
import web

# install package redis from pip
from redis import Redis

urls = (
    '/add/(.*?)/(.*?)', 'add',
    '/stats', 'stats'
)

app = web.application(urls, globals())
# Connect to the redis container
redis = Redis(host= "redis", port=6379)

class add:
    def GET(self, a, b):
        redis.incr('additions')
        return "{0} + {1} = {2}".format(a, b, (int(a) + int(b)))

class stats:
    def GET(self):
        return 'We have calculated {0} additions' . format (redis.get( 'additions' ))

if __name__ == "__main__":
    app.run()
```

Python server that adds two numbers and uses redis as a centralized statistics cache.

## Exercise

### Create `Dockerfile`

First create a dockerfile in the `addition-server` directory that describes how to build an image capable of running the python application.

_Note:_ You should install both the `web.py` and `redis` python packages in the container.

### Create `docker-compose.yml`

Add two services in the `docker-compose.yml` file to run:

 - redis cache in version 3
   - The name of this service should match the hardcoded host name in the python file, as this is how service discovery is implemented
 - the python addition server image.
   - Using `build` and not `image`
   - Remember port mappings from 8080m on the container to 5000 on the host machine

See https://docs.docker.com/compose/compose-file/ for help.
Use version 3 or above.

### Build and start

Standing in the directory where the `docker-compose.yml` file is, we can execute the following

```shell
# Build all services that use the `build` notation
$ docker-compose build

# Start all services that are described in the `docker-compose.yml` file
$ docker-compose up
```

Now you should be able to access the following:

- http://localhost:5000/add/2/32
- http://localhost:5000/stats

_Note:_ You do not actually have to talk to the redis container your self at any point, as this is all handled by the python server.

### Cleanup

```shell
## Stop all services
$ docker-compose stop

# Remove all services
$ docker-compose rm
```

### Playing around

Try to start the docker compose stack and hitting the add endpoint. See that the counter goes up.
Now try to stop the stack without running `rm`. Start the stack again and see how this effected the counter.

Now try stopping and removing the stack. Start it again and observe the counter.

### Publishing to a Docker repository

Follow the official Docker documentation to publish the python addition server to your docker hub account.
_Note_: Create a docker account if you do not already have one.

https://docs.docker.com/docker-cloud/builds/push-images/

Now change your `docker-compose.yml` file to use the published image instead of the locally build version.
Test that it works as expected.

### Host it online

Now it's time to expose our fantastic AaaS (Addition-as-a-Service) to the world!
Go to play-with-docker.com and login with your docker login from docker hub.

Create a new instance of a server in the left hand menu. Drag and drop your `docker-compose.yml` file onto the terminal, to copy it to the server.

Run `docker-compose up` and check that docker downloads the two images needed from docker hub, and starts the containers.

Now you should see a blue port number in the top of the dashboard. Click the port to go to the endpoint for your new hosted docker container.

__Congratulations!__ You now have a distributed, cloud native, container hosted application with all configurations needed expressed as code.
