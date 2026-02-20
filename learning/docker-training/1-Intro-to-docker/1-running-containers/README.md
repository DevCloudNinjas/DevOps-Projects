# My first Docker Exercises

## About this exercise set

> To help the users of this exercise to learn how to use docker and where to get help when they are stuck in the real world, I have tried to create exercises that forces the user to look in documentation and experiment.
>
> **This means, that the exercise set is not a simple copy & paste exercise**

### Credits
The exercises are build on exercises from the following workshop:
https://github.com/christian-posta/docker-kubernetes-workshop


## Table of content

* [About this exercise set](#about-this-exercise-set)
  + [Credits](#credits)
* [Your First Docker](#your-first-docker)
  + [Pull a docker image](#pull-a-docker-image)
  + [List locally, installed images](#list-locally--installed-images)
  + [Running the Docker container](#running-the-docker-container)
  + [Destroy all the stuff](#destroy-all-the-stuff)
* [Deploy Apache Tomcat](#deploy-apache-tomcat)
* [Exploring the Apache Tomcat Container](#exploring-the-apache-tomcat-container)
  + [Playing with flags](#playing-with-flags)
  + [Stop and Remove container](#stop-and-remove-container)

<!-- https://ecotrust-canada.github.io/markdown-toc/ -->

## Your First Docker

### Pull a docker image

Lets start by pulling Centos from DockerHub (http://hub.docker.com)

Go to DockerHub and find the newest major version of the officiel centos image.
When you have the newest version number you can run the following:

```shell
$ docker pull centos:{version number}
```

This should result in something matching the following

```shell
Pulling from library/centos

fa5be2806d4c: Pull complete
0cd86ce0a197: Pull complete
e9407f1d4b65: Pull complete
c9853740aa05: Pull complete
e9fa5d3a0d0e: Pull complete
Digest: sha256:def5c79bc29849815dec7dddc8f75530a9115c94d5b17e0e6807f929902fab62
Status: Downloaded newer image for centos:...
```

### List locally, installed images

To list the local use the docker images command:

```
$ docker images

ceposta@postamac(~) $ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos              x                   e9fa5d3a0d0e        2 days ago          172.3 MB
```

This only shows pulled or build image.

### Running the Docker container

Let's start by asking docker to run the centos image we have pulled, and to run the ```echo``` command inside it.


```shell
$ docker run --rm centos:{version from above} echo "Hello from the docker world"

Hello from the docker world
```

Woah, what happened? It just printed out "hello, world"? So what?

Next let's ask docker to run an interactive shell inside a docker container:

__Exercise__: Use `docker run --help` to figure out what `-it` and `--rm` does. These two are very importaint when testing and developing new containers.

```
$ docker run -it --rm centos:{version} bash

[root@25fc15aa1cb9 /]# _
```

Cool! We have a bash shell, and a minimal distro of Centos!
Did you see how fast that booted up?

Typing `cat /etc/os-release` from the new bash prompt shows us all info about the distro:

```shell
[root@25fc15aa1cb9 /]# cat /etc/os-release
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="https://www.centos.org/"
BUG_REPORT_URL="https://bugs.centos.org/"

CENTOS_MANTISBT_PROJECT="CentOS-7"
CENTOS_MANTISBT_PROJECT_VERSION="7"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="7"
```

Run some other commands from within the container:

```shell
$ hostname -f         ## Get the name of the machine
$ ps aux              ## List all processes on the machine
$ yum -y install vim  ## Install vim
```

A real linux distro right? Did you notice that *`ps aux`* didn't show too many processes?

### Destroy all the stuff

> :warning: **_ WARNING:_ Make sure that you are IN the docker container and NOT in your local machines terminal !**

Let's do some destructive stuff:

```shell
$ rm -fr /usr/sbin
```

Wuh? you deleted all of the sacred system tools!?

Let's delete some user tools too

```shell
$ rm -fr /usr/bin
```

```shell
[root@25fc15aa1cb9 /]# ls
  bash: /usr/bin/ls: No such file or directory
```

Whoops... cannot *`ls`* or do anything useful anymore. What have we done!?

No worries! Just *`exit`* the container and fire up a new one:

```
$ docker run -it --rm centos:{version number} bash
```

Everything is back! Phew....

We now have all the tools again. But not vim.

__Exercise__: Consider why we have all tools avaible again, except vim.

## Deploy Apache Tomcat

Now let's run a JVM based application like Apache Tomcat:

```
$ docker run --rm -p 8888:8080 tomcat:8.0
```

Since the Tomcat 8.0 docker image doesn't exist, Docker will try to automatically pull it from the registry.
Give it a moment, and you should see tomcat start successfully:

```
11-Jan-2018 14:49:02.302 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /usr/local/tomcat/webapps/ROOT has finished in 36 ms
11-Jan-2018 14:49:02.302 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory /usr/local/tomcat/webapps/examples
11-Jan-2018 14:49:02.729 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /usr/local/tomcat/webapps/examples has finished in 427 ms
11-Jan-2018 14:49:02.755 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-apr-8080"]
11-Jan-2018 14:49:02.836 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-apr-8009"]
11-Jan-2018 14:49:02.841 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 1422 ms
```

__Exercise__: Use `docker run --help` to figure out what `-p` does.

Now we should be able to connect to *`http://localhost:{some port}`* and see that tomcat is running.

__Exercise__: Figure out the port and access the url in a browser.

_If this did not work, you may be running docker in a virtual machine on your mac or windows machine. Then we need to mapped the Docker Host ports properly._

## Exploring the Apache Tomcat Container

We have a running container that has tomcat in it! WooHoo! Let's explore the tomcat container really quick.
Fire up a new shell window (separate than the running tomcat docker container from previous)

```
docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
c2c059a3baab        tomcat:8.0          "catalina.sh run"   36 minutes ago      Up 36 minutes       0.0.0.0:8888->8080/tcp   dreamy_kowalevski
```

Instad of asking docker to run a new container with an interactive terminal attached, we can ask docker to run `bash` with an interactive terminal in a _running container_.

_Exercise_: Goto  [docker exec](https://docs.docker.com/engine/reference/commandline/exec/) and try to figure out how.

We should now have a bash prompt inside the tomcat container. Feel free to explore around a bit.

__Exercise__: Figure out which linux distro the tomcat image is build on, using the `cat /etc/os-release` command.

Now exit out of the tomcat container using `exit`

Switch back to the other window where we ran tomcat. Let's *`CTR+C`* that window and exit the docker container.

We should have no containers running:

__Exercise__: Use the `docker` commandline to check that there are no running docker containers.
*Note*: Dependent on which terminal you are using it can sometime detach from the container without killing it when using *`CTR+C`*.

Also check that we dont have any stopped containers!

This is because we used the *`--rm`* command when we started the tomcat container, so docker will automatically remove the container.

Here are some other useful `docker run` flags:

|    |    |
| -- | -- |
| `--name`| Give your container a unique name |
| `-d`| Run your container in daemon mode (in the background) |
| `--dns`| Give your container a different nameserver from the host |
| `-it`| Interactive with tty (wouldn't use this with `-d`) |
| `-e`| Pass in environment variables to the container |
| `--expose`| Expose ports from the docker container |
| `-P`| Expose all published ports on the container |
| `-p`| Map a specific port from the container to the host `host:container` |

We will look at *`--link`* and *`--volume`* later today.

### Playing with flags

Let's use some of those previous `run` command-line flags and start tomcat in the background:

```
docker run -d --name="tomcat8" -p 8888:8080 tomcat:8.0
```

Note, we also gave this container a name, so we can refer to it by name instead of container id.

__Exercise__: Find the docker command to get logs from a container, and get a stream of logs from the new container named __"tomcat8"__

```shell
11-Jan-2018 14:49:02.729 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /usr/local/tomcat/webapps/examples has finished in 427 ms
11-Jan-2018 14:49:02.755 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-apr-8080"]
11-Jan-2018 14:49:02.836 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-apr-8009"]
11-Jan-2018 14:49:02.841 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 1422 ms
```
Let's use a couple of interesting docker commands with our `tomcat8` container:

```
docker top tomcat8
```

I know, a little misnamed -- instead of the normal linux `top` container, it just displays the processes running in the container:

```
PID                 USER                TIME                COMMAND
13111               0                   0:07                /docker-java-home/jre/bin/java -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties {...} org.apache.catalina.startup.Bootstrap start
```

What about this one:

```
$ docker inspect tomcat8
```

Wow... that's a lot of information about the container! We can also use a `--format` template to pick out specific info
from that output (see `https://docs.docker.com/engine/reference/commandline/inspect/`)

```
docker inspect --format='{{.NetworkSettings.IPAddress}}' tomcat8
```

or

```
docker inspect --format='{{.Config.Env}}' tomcat8
```

__Exercise__: Write a command that uses `docker inspect` and `--format` to figure out when the tomcat container was "StartedAt". 


### Looking at the tomcat image

An image usally consists of mulitple layers of images. Lets try to find out that layers the tomcat:8.0 image consists of.

__Exercise__: Figure out how to make docker cli to display the history of an image, and there by listing all layers of a specific image

```shell
$ docker ?? tomcat:8.0
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
8bfd42907609        31 hours ago        /bin/sh -c #(nop)  CMD ["catalina.sh" "run"]    0B
<missing>           31 hours ago        /bin/sh -c #(nop)  EXPOSE 8080/tcp              0B
<missing>           31 hours ago        /bin/sh -c set -e  && nativeLines="$(catalin…   0B
...
<missing>           11 days ago         /bin/sh -c apt-get update && apt-get install…   41.2MB
<missing>           2 weeks ago         /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:3e6141c0c9cb74b14…   127MB
```

### Stop and Remove container

Feel free to play around with the container a little bit more. When finished, stop the container:

```
$ docker stop tomcat8
```

If you run `docker ps` you shouldn't see the container running any more. However, `docker run -a` will show all containers even the stopped ones.
We can remove a container with:

```
$ docker rm tomcat8
```

Then neither `docker ps` nor `docker ps -a` should show the container.
