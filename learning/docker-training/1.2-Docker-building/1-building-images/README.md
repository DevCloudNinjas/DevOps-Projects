#  Creating your first Images with Docker

## About this exercise set

> To help the users of this exercise to learn how to use docker and where to get help when they are stuck in the real world, I have tried to create exercises that forces the user to look in documentation and experiment.
>
> **This means, that the exercise set is not a simple copy & paste exercise**

This folder contains a very small docker container, capable of adding two numbers.

## Files

### `addition.sh`

Shell script that takes two commandline parameters, adds them together, and prints the calculation.

```shell
#!/bin/sh

RESULT=$(($1+$2))
echo "$1 + $2 = $RESULT"
```

_Note:_ alpine linux does NOT like scripts with windows carriage returns in.
Make sure that the file ONLY has unix line breaks in it.

### `dockerfile`

```dockerfile
FROM alpine

# Add shell script
COPY addition.sh /

# Which script to execute when running the container
ENTRYPOINT ["/addition.sh"]

# Default values to the ENTRYPOINT
CMD ["0", "0"]
```

## Build the app

Start by moving into the correct directory with a terminal.
Here’s what ls should show:

Now we will use the `docker run` command to build a docker image.
We will also use the `-t` flag to give it has a friendly name.

```shell
$ docker build -t add-a-tron .
```

Unlike other build systems, the image is not an artifact in an `./out` folder.
But is located in your machine’s local Docker image registry. To list all images run the folowing:

```shell
$ docker images

REPOSITORY            TAG                 IMAGE ID
add-a-tron            latest              d0490b0746d2
```

## Run the `add-a-tron`

To start up a container from the image run the following:

```shell
docker run add-a-tron

0 + 0 = 0
```

Now that's a bit boring. Try to give the container some parameters:

```shell
docker run add-a-tron 321 123

321 + 123 = 444
```

Cool! You have now build a container capable of taking commandline inputs, and returning a result based on the inputs.

__Exercise__: Extend the application to take a arbitrary number of arguments. See for example https://stackoverflow.com/a/255913

### Create a web server that adds

Now, everything is more fun as a service. Let's create a python webserver that can add the two numbers instead of a commandline tool.

Here is a small python webserver that are capable the same job as the `addition.sh` script.

```python
import web

urls = (
    '/add/(.*?)/(.*?)', 'add'
)
app = web.application(urls, globals())

class add:        
    def GET(self, a, b):
        return "{0} + {1} = {2}".format(a, b, (int(a) + int(b)))

if __name__ == "__main__":
    app.run()
```

#### New Dockerfile for python server

We need to do the following things:

 - Extend a base image that has python in the correct version; _python 2.7_
 - Install the python package called `web.py` that we use in the server, using the python package installer: `pip`
 - Add our new python server script
 - Define the command that docker needs to run to start the server.

##### 1. Base image
Rename the old `Dockerfile` to something else and create a new `Dockerfile`.
 _Note: you can create a new `Dockerfile` with a name that is not exatly `Dockerfile`, but then you need to specify it as a parameter to `docker build`_.

As this is a python server we need to start from a base image that are capable of running python. Go to the official python repo on Docker Hub: https://hub.docker.com/r/_/python/ and choose a python image that comes from **alpine linux**, and has a python `2.7` version.

##### 2. Install `web.py`

See http://webpy.org/install for how to install the package. Find a way to do this in the dockerfile.

##### 3. Add `addition.py` to the container

This can be done in the same way as we do in the `Dockerfile` for the shell version.

##### 4. Tell Docker how to start the server

Use the dockerfile command called `ENTRYPOINT` to tell docker to start the server using the python executable. 

#### Build and run

Now build the new docker images with a tag called `add-a-tron-server`.

After building the image, start a container running the `add-a-tron-server` image. 
`web.py` will automatically listen on port `8080`. So when we start the container we need to map this port to a port on the local machine to be able to access the endpoint.
For fun try to map the port to `12000`.

Now we should be able to access the following endpoint:
`http://localhost:12000/add/2/32` and see the calculation: `2 + 32 = 34`.

If this does not work, run `docker ps` to validate that a container is running with:

 - The correct image
 - A Port mapping from `0.0.0.0:8080->12000/tcp`
 - The command running is python and with our server as argument.
