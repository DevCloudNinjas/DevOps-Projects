# Introduction to Docker

---
## About me
### Frederik Mogensen

<div class="left-col-big">
Software Pilot at Trifork
<br>
<i>Focus on Docker, orchestration and ci/cd</i>
</div>
<div class="right-col-small">
![image](assets/images/me.jpeg)
</div>

---
# Containers are not VMs

---
## Containers are NOT VMs

- Easy connection to make
- Fundamentally different architectures
- Fundamentally different benefits

---
## VMs

![image](assets/images/image12.png)

---
## Containers

![image](assets/images/image13.png)

---
## They’re different, not mutually exclusive

![image](assets/images/image14.png)


---
# Build, Ship, and Run

---
## Docker vocabulary

- Docker Image
  - The basis of a Docker container. Represents a full application.
- Docker Container 
  - The standard executing unit
- Docker Engine 
  - Creates, ships and runs Docker containers
- Registry Service
  - Cloud or server based storage and distribution of images

![image](assets/images/image18.png)
![image](assets/images/image17.png)
![image](assets/images/image19.png)
![image](assets/images/image20.png)

---
## Basic Docker Commands

```bash
docker pull mogensen/catweb:1.0
docker images
docker run -d -p 5000:5000 --name catweb mogensen/catweb:1.0
docker ps
docker stop catweb // or <container id>
docker rm catweb // or <container id>
docker rmi mogensen/catweb:1.0 // or <image id>
```

---
## Dockerfile – Linux Example

- Instructions on how to build a Docker image
- Looks very similar to "native" commands

```dockerfile
FROM alpine:latest

RUN apk add --update py-pip

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

EXPOSE 5000

CMD ["python", "/usr/src/app/app.py"]
```

@[1](Our base image)
@[3](Install python and pip)
@[5](Upgrade pip)
@[7-8](Install Python modules needed by the Python app)
@[10-11](Copy files required for the app to run)
@[13](Tell the port number the container should expose)
@[15](How should docker start the application)

---
## Basic Docker Commands

```dockerfile
FROM alpine:latest
RUN apk add --update py-pip
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/
EXPOSE 5000
CMD ["python", "/usr/src/app/app.py"]
```

```shell
docker build –t mogensen/catweb:2.0 .
docker push mogensen/catweb:2.0
```

---
## Put it all together

![image](assets/images/diagram.png)

---
## Demo

Build, Ship, and Run

---
## Now you try it!

- Visit http://docs.docker.com/installation
- Install the right version of Docker for your machine
- Docker for Mac
- Docker for Windows
- After Docker is installed, run Catweb

```shell
$ docker run -p 5000:5000 --name catweb mogensen/catweb:1.0
```

Browse to port 5000 on your machine: http://localhost:5000

---
# Background containers

---

## Objectives

Our first containers were *interactive*.

We will now see how to:

* Run a non-interactive container.
* Run a container in the background.
* List running containers.
* Check the logs of a container.
* Stop a container.
* List stopped containers.

---

## A non-interactive container

We will run a small custom container.

This container just displays the time every second.

```bash
$ docker run jpetazzo/clock
Fri Feb 20 00:28:53 UTC 2015
Fri Feb 20 00:28:54 UTC 2015
Fri Feb 20 00:28:55 UTC 2015
...
```

* This container will run forever.
* To stop it, press `^C`.

Note:

* Docker has automatically downloaded the image `jpetazzo/clock`.
* This image is a user image, created by `jpetazzo`.
* We will hear more about user images (and other types of images) later.

---

## Run a container in the background

Containers can be started in the background, with the `-d` flag (daemon mode):

```bash
$ docker run -d jpetazzo/clock
47d677dcfba4277c6cc68fcaa51f932b544cab1a187c853b7d0caf4e8debe5ad
```

* We don't see the output of the container.
* But don't worry: Docker collects that output and logs it!
* Docker gives us the ID of the container.

---

## List running containers

How can we check that our container is still running?

With `docker ps`, just like the UNIX `ps` command, lists running processes.

```bash
$ docker ps
CONTAINER ID  IMAGE           ...  CREATED        STATUS        ...
47d677dcfba4  jpetazzo/clock  ...  2 minutes ago  Up 2 minutes  ...
```

Note:

Docker tells us:

* The (truncated) ID of our container.
* The image used to start the container.
* That our container has been running (`Up`) for a couple of minutes.
* Other information (COMMAND, PORTS, NAMES) that we will explain later.

---

## Starting more containers

Let's start two more containers.

```bash
$ docker run -d jpetazzo/clock
57ad9bdfc06bb4407c47220cf59ce21585dce9a1298d7a67488359aeaea8ae2a
```

```bash
$ docker run -d jpetazzo/clock
068cc994ffd0190bbe025ba74e4c0771a5d8f14734af772ddee8dc1aaf20567d
```

Check that `docker ps` correctly reports all 3 containers.

---
## View the logs of a container

Docker collects all logs from the containers output.

Let's see that now.

```bash
$ docker logs 068
Fri Feb 20 00:39:52 UTC 2015
Fri Feb 20 00:39:53 UTC 2015
...
```

Note:
* We specified a *prefix* of the full container ID.
* You can, of course, specify the full ID.
* The `logs` command will output the *entire* logs of the container.

---
## View only the tail of the logs

To avoid being spammed with eleventy pages of output,
we can use the `--tail` option:

```bash
$ docker logs --tail 3 068
Fri Feb 20 00:55:35 UTC 2015
Fri Feb 20 00:55:36 UTC 2015
Fri Feb 20 00:55:37 UTC 2015
```

Note:

* The parameter is the number of lines that we want to see.

---

## Follow the logs in real time

Just like with the standard UNIX command `tail -f`, we can
follow the logs of our container:

```bash
$ docker logs --tail 1 --follow 068
Fri Feb 20 00:57:12 UTC 2015
Fri Feb 20 00:57:13 UTC 2015
^C
```

* This will display the last line in the log file.
* Then, it will continue to display the logs in real time.
* Use `^C` to exit.

---
## Docker Container Architecture

---

## What is an image?

- Image = files + metadata
- These files form the root filesystem of our container.
- The metadata can indicate a number of things, e.g.:
  - the author of the image
  - the command to execute in the container when starting it
  - environment variables to be set
  - etc.
* Images are made of *layers*, conceptually stacked on top of each other.
* Each layer can add, change, and remove files and/or metadata.
* Images can share layers to optimize disk usage, transfer times, and memory use.

---
## Differences between containers and images

* An image is a read-only filesystem.
* A container is an encapsulated set of processes running in a
  read-write copy of that filesystem.
* To optimize container boot time, *copy-on-write* is used 
  instead of regular copy.
* `docker run` starts a container from a given image.

---
## Example of Catweb Image Layers

![image](assets/images/catweb-layers.png)

---
## Docker File System

If an image is read-only, how do we change it?

- We don't.
- We create a new container from that image.
- Then we make changes to that container.
- When we are satisfied with those changes, we transform them into a new layer.
- A new image is created by stacking the new layer on top of the old image.

---
## Copy on Write

- Super efficient:
  - Sub second instantiation times for containers
  - New container can take &lt;1 Mb of space

- Containers appears to be a copy of the original image
- But, it is really just a link to the original shared image

- If someone writes a change to the file system, a copy of the affected file/directory is "copied up"

---
## What about data persistence?

- Volumes allow you to specify a directory in the container that exists outside of the
docker file system structure
- Can be used to share (and persist) data between containers
- Directory persists after the container is deleted
  - Unless you explicitly delete it
- Can be created in a Dockerfile or via CLI

---
## Images namespaces

There are three namespaces:

* Official images

    e.g. `ubuntu`, `busybox` ...

* User (and organizations) images

    e.g. `jpetazzo/clock`

* Self-hosted images

    e.g. `registry.example.com:5000/my-private/image`

Let's explain each of them.

---
## Root namespace

The root namespace is for official images. They are put there by Docker Inc.,
but they are generally authored and maintained by third parties.

Those images include:

* Small, "swiss-army-knife" images like busybox.
* Distro images to be used as bases for your builds, like ubuntu, fedora...
* Ready-to-use components and services, like redis, postgresql...

---
## User namespace

The user namespace holds images for Docker Hub users and organizations.

For example:

```bash
jpetazzo/clock
```

The Docker Hub user is:

```bash
jpetazzo
```

The image name is:

```bash
clock
```

---
## Self-Hosted namespace

This namespace holds images which are not hosted on Docker Hub, but on third
party registries.

They contain the hostname (or IP address), and optionally the port, of the
registry server.

For example:

```bash
localhost:5000/wordpress
```

* `localhost:5000` is the host and port of the registry
* `wordpress` is the name of the image

---
## How do you store and manage images?

Images can be stored:

* On your Docker host.
* In a Docker registry.

You can use the Docker client to download (pull) or upload (push) images.

Note:

To be more accurate: you can use the Docker client to tell a Docker Engine
to push and pull images to and from a registry.

---
## One platform - one journey
___For all applications___

1. Containerize Legacy Applications
   - Lift and shift for portability and efficiency
1. Transform Legacy to Microservices
   - Look for shared services to transform
1. Accelerate New Applications
   - Greenfield innovation

---
## Docker Datacenter
_Containers in production_

![image](assets/images/ucp.png)

Note:
- Enterprise container orchestration, management and security for dev and ops
- Available today for Linux environments
- Q4 2016 beta for Windows environments 


---
## Hands On

#### Playing with docker containers

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/1-Intro-to-docker/1-running-containers)
