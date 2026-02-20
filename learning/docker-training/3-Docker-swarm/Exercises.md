# Docker Swarm exercises

## About this exercise set

> To help the users of this exercise to learn how to use docker and where to get help when they are stuck in the real world, I have tried to create exercises that forces the user to look in documentation and experiment.
>
> **This means, that the exercise set is not a simple copy & paste exercise**

## Table of content

* [About this exercise set](#about-this-exercise-set)
* [Table of content](#table-of-content)
* [Setup a Docker Swarm Cluster](#setup-a-docker-swarm-cluster)
  + [Create machine instances](#create-machine-instances)
  + [Create cluster](#create-cluster)
* [Deploy your first service](#deploy-your-first-service)
  + [Create a visualizer stack](#create-a-visualizer-stack)
    - [Exercise - Creating a docker-compose file](#exercise---creating-a-docker-compose-file)
* [Create a complete Docker Swarm stack](#create-a-complete-docker-swarm-stack)
* [Scaling the frontend service](#scaling-the-frontend-service)
    - [Exercise - Scaling with the Docker CLI](#exercise---scaling-with-the-docker-cli)
    - [Exercise - Scaling in the docker-compose file](#exercise---scaling-in-the-docker-compose-file)
* [Network security](#network-security)
  + [Exercise - Setting up network separation](#exercise---setting-up-network-separation)
* [Playing with node failure](#playing-with-node-failure)
* [Specify placement for the services](#specify-placement-for-the-services)
  + [Exercise - Placing services](#exercise---placing-services)
* [Setting limits for the application containers](#setting-limits-for-the-application-containers)
  + [Exercise - Limiting CPU and memory](#exercise---limiting-cpu-and-memory)
* [Log aggregation](#log-aggregation)
  + [Exercise - Sending logs to a central service](#exercise---sending-logs-to-a-central-service)
* [References](#references)

## Setup a Docker Swarm Cluster

In this part we use Play With Docker as a free provider of Alpine Linux Virtual MachineS in the cloud. These can be used to build and run Docker containers and to play around with clusters in Swarm Mode.

This can be found at: [http://play-with-docker.com/](http://play-with-docker.com/)

### Alternative text editor

The only editor available on play with docker is vim.
If you do not feel at home in vim, you have some other options.

#### 1. You can install another.

Such as nano:

    $ apk update
    $ apk add nano

#### 2. Use the browser editor

In the top of the window on Play With Docker there is a button labled "Editor".
This allows you to edit filed that are on the different machine instances.

To use the editor you need to create a file in the terminal in order to see it there.
First you do a `touch docker-compose.yaml` and then open the editor (or use the refresh button in the editor window) you'll see the file
there.

#### 3. Install the docker-machine driver for Play With Docker

Or install the [docker-machine driver for Play With Docker](https://github.com/play-with-docker/docker-machine-driver-pwd), to be able to edit files locally on your own machine.

### Create machine instances

Start by creating three machines using the "+Add New Instance" button.

### Create cluster

Chose a machine to be the manager and initiate the Docker Swarm cluster on this machine.

    $ docker swarm init --advertise-addr eth0

In the output of this command, we get the command that can be used to join workers to the cluster

    $ docker swarm join --token SWMTKN-1-2ypam... {ip}:2377

Run this command on the two other machines.
Now we can validate that we have a cluster by going to the manager note and run the following command.

    $ docker node ls
    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    3kkk6vvth1gu5hi3v93q2har3 *   node1               Ready               Active              Leader
    207qifbk21o6h05afa4ypabk3     node2               Ready               Active
    dne037y5lvndl37kccj2028dk     node3               Ready               Active

## Deploy your first service

### Create a visualizer stack

To be able to see whats running on our cluster in a graphical interface we use the docker services called Visualizer.

Create a service stack with the visualizer container.

    docker service create --name=viz \
        -p=8081:8080 \
        --constraint=node.role==manager \
        --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
        dockersamples/visualizer:stable

Check the new endpoint on the manager node (port 8081) to see our cluster and the visualizer container.

#### Exercise - Creating a docker-compose file

Delete the service we created above.

    $ docker service ls
    ID                  NAME                MODE                REPLICAS            IMAGE                             PORTS
    rjvz7l1tzoal        viz                 replicated          1/1                 dockersamples/visualizer:stable   *:8081->8080/tcp
    
    $ docker service rm viz

Change the command we just ran to a docker-compose file with the name _docker-visualize.yml_. Looking something like this:

**[Note]** The volume mapping does not have quite the same format in the command line as it does in the docker-compose file.
And make sure to choose a docker-compose version that are supported by your docker version.

    version: "3"
    services:
      visualizer:
        image: {that image we want to use}
        ports:
          - {port stuff}
        volumes:
          - {volume mapping}
        deploy:
          placement:
            constraints:
             - {constraints}

[Docker Compose documentation](https://docs.docker.com/compose/compose-file/)

Redeploy the visualizer with the yaml file, and validate that it works!

    $ docker stack deploy --compose-file docker-visualize.yml viz

**[Note]** This command is used BOTH for deploying a stack first time and for updating the desired state of the stack.

## Create a complete Docker Swarm stack

We will now look at an example application called VotingApp from one the Docker Labs.

![Architecture diagram](https://raw.githubusercontent.com/dockersamples/example-voting-app/master/architecture.png)

* A Python webapp which lets you vote between two options
* A Redis queue which collects new votes
* A .NET worker which consumes votes and stores them in...
* A PostgreSQL database backed by a Docker volume
* A Node.js webapp which shows the results of the voting in real time

We can deploy the stack with this description.

    version: "3"
    services:
    
      redis:
        image: redis:alpine
        ports:
          - "6379"
    
      db:
        image: postgres:9.4
        volumes:
          - db-data:/var/lib/postgresql/data
    
      vote:
        image: dockersamples/examplevotingapp_vote:before
        ports:
          - 5000:80
        depends_on:
          - redis
    
      result:
        image: dockersamples/examplevotingapp_result:before
        ports:
          - 5001:80
        depends_on:
          - db
    
      worker:
        image: dockersamples/examplevotingapp_worker
        depends_on:
          - db
          - redis
    
    volumes:
      db-data:

Start by creating a yml file with the data above and deploy it to our cluster as in the last exercise.
Check that you can see all five containers in the visualizer and that they turn green. You should also check that you can see the two frontends at port 5000 and 5001.

__Try voting.__

## Scaling the frontend service

News has spread like wildfire about our new awesome voting app and we need to have more services available for voting.

#### Exercise - Scaling with the Docker CLI

Call the _docker service_ command line with a _--help_ param to figure out how to scale the _vote_ service to 5 instances.

    $ docker service --help

Once you have scaled the service:

 - Check that you can see all five containers in the visualizer.
 - Check that the vote page is now handled by different containers.
     * The container handling a request is shown on the vote page.


#### Exercise - Scaling in the docker-compose file

Update the yml file with the new deployment info, stating that we want to have 5 replicas of the vote service.
[Docker Compose deploy documentation](https://docs.docker.com/compose/compose-file/#deploy)

**[Consider!]** Take a moment to consider what will happen if you scale the redis cache instead of the vote application.

**Hint:** The worker connects to the redis by using the redis service dns name.
This results in that the worker only connection to a random instance of redis, and not to a redis cluster or to all redis instances.
The same is the case for the PostgreSQL database.
The votes may end in one redis cache, but the result app could be looking in another instance.

## Network security

The next step in making our voting application more production ready is to make sure that the services only has access to what they need.

More specifically, we want the services in the voting application to be on different networks. So that the public application _vote_ only has access to the redis cache and not to the PostgreSQL database or the result application.

We also need the _worker_ service to have access to both networks, because it is the one responsible for moving votes from the redis cache to the PostgreSQL database.


### Exercise - Setting up network separation

Create the following two networks in the yml file and specify the networks on the services.

#### public_vote

* vote
* redis
* worker

#### private_result

* worker
* db
* result

Note that this is something that docker has changed a lot over time.
Newest documentation is here: [Docker compose endpoint mode](https://docs.docker.com/compose/compose-file/#endpoint_mode)

_Note: When changing the network configuration in swarm, you may need to delete the entire stack and deploy it again!_

### Exercise - Inspect the network separation

Try to verify that the two new networks contain exactly the expected containers, using the docker cli.

## Playing with node failure

To simulate a failing node (bloody hardware failing all the time) try deleting one of the worker nodes (*not the only master you have!*) in the Play With Docker interface.
When doing this keep an eye on the visualizer and see how all the containers are redeployed on the remaining node.

Try creating two new nodes and joining them to the cluster. By default docker swarm will not move running containers to the new nodes.
No need to kill and move containers that are already working as expected.
Try scaling up the _vote_ or _worker_ services and see how the containers are placed.

## Specify placement for the services

Next task on the production list is to make sure that our result database are only running on machines that have ssd.
Add a label called _disk_ to all our worker nodes, with _disk=hdd_ for two of them and _disk=ssd_ on the last worker
See [documentation](https://docs.docker.com/engine/swarm/manage-nodes/#add-or-remove-label-metadata) for adding labels.

### Exercise - Placing services

Update the yml file with conditions on the _db_ service that specify that it can only be deployed on _disk=ssd_. Validate by looking in the visualizer.

You can also change the other services to make sure that only the database is the only sevice running on machines with ssd.

Try setting the manager as _drained_ so no containers are scheduled on the manager.

## Setting limits for the application containers

The next important thing to make our new awesome voting application more production ready is to limit the _cpu_ of all the services.
This will help prevent a situation where on single service goes crazy and consumes all the resources on the host machine.
An example of setting the limits from command line could look like this:

    docker service deploy \
      --limit-cpu 0.25 \
      --reserve-cpu 0.1 \
      webapp

The _reserve-cpu_ parameter tells docker how much it can pack the container on a host, so that each container will always have at least the reserved cpu amount available. _limit-cpu_ tells docker when the container is no longer behaving as expected, and should be killed.

### Exercise - Limiting CPU and memory

Update the yml file with conditions on all services that specify a cpu limit and a reserved cpu amount.

You can also look at limiting the services on memory.

## Log aggregation

When we run many services on may machines, it becomes very important to have centralized logging.
You should try to setup central logging of your Docker Swarm and send the logs from the different services to that service.

There are plenty applications for central logging

- Splunk
- Humio
- Logstash, ElasticSearch and Kibana
- PaperTrail
- Graylog2
- ...

For all containers that logs to standard out docker can collect the logs for us.

### Exercise - Sending logs to a central service

Create a free account at PaperTrails and setup a logspout container on each Docker Swarm node to send the data to PaperTrails

Remember that Docker Swarm has the notion of _mode_ for a service that can either be replicated or global.

    https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-docker/

Because the logspout container gets all the logs from the Docker socket, and not by actually talking to any of the other containers, it does not need to know anything about them, or be able to send them requests.

Create a new .yml stack file with the logspout container in and deploy the stack to the cluster.

## References
1. [Play With Docker on github](https://github.com/play-with-docker/play-with-docker)
2. [Deploy the Voting App on a Docker Swarm using Compose version 3](https://medium.com/lucjuggery/deploy-the-voting-apps-stack-on-a-docker-swarm-4390fd5eee4)
3. [Example voting app](https://github.com/dockersamples/example-voting-app)
