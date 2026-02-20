# Container Orchestration with Docker Swarm

---
## About me
### Frederik Mogensen

<div class="left-col-big">
Software Pilot at Trifork
<br>
<i>Focus on Docker, orchestration and ci/cd</i>
</div>
<div class="right-col-small">
![Image](assets/images/me.jpeg)
</div>

---
# Running `N` containers on `M` machines ?

---
## Independent Docker hosts

- Deployment on M machines ?
- Updating N containers ?
- Scheduling N on M ?
- Possible solutions
  - Chef
  - Puppet
  - Ansible

---
## Containers manually allocated on multiple nodes

- Non-linear resources usage
- No service discovery, hardcoded configurations
- Manual reaction to failures

- Possible solutions 
  - Manually monitor nodes and reschedule containers
  - Maintain list of services on nodes

---
## Storage for containers

- Store on node?
- Manually integrate to network storage

---
## Pets VS Cattle



![Image](assets/images/cattle_no_text.png)


|    |    |
| -- | -- |
| - Unique systems that can never be down, build and managed manually | ” When one of them gets sick, you shoot 'em in the head and replace 'em with a new one.”  |

<small>https://www.slideshare.net/zhurbilo/artem-zhurbilo-some-ways-to-set-up-the-server-highload-strategy-meetup</small>

---
## The Monolith Retirement
![Image](assets/images/monolithcomic.png)

<small>http://turnoff.us/geek/monolith-retirement/</small>

---
# Orchestration

---
## What is Container Orchestration


<div class="left-col">
  <ul>
    <li>Cluster management</li>
    <li>Scaling</li>
    <li>Service discovery</li>
    <li>Load balancing</li>
    <li>Networking</li>
    <li>Security</li>
  </ul>
</div>
<div class="right-col">
  <ul>
    <li>Rolling updates</li>
    <li>Storage</li>
    <li>Configuration</li>
    <li>Secrets</li>
    <li>…</li>
  </ul>
</div>

---
## What is Container Orchestration

![Image](assets/images/swarm.png)
![Image](assets/images/kubernetes.png)
![Image](assets/images/mesos.png)

---
## Desired state

![Image](assets/images/desired_state.png)

<small>https://www.slideshare.net/Docker/container-orchestration-from-theory-to-practice</small>

---
## Scaling Services

<div class="clearfix">
<div class="left-col">
  <ul>
    <li>Declare the number of services</li>
    <li>Scale up or down</li>
  </ul>
</div>
<div class="right-col">
![Image](assets/images/microservice_architecture.png)
</div>
</div>

<small>https://martinfowler.com/articles/microservices.html</small>

---
## Service Discovery

<div class="clearfix">
<div class="left-col">
  <ul>
    <li>Allow for services in the cluster to locate other services
    <ul>
      <li>DNS</li>
      <li>API</li>
      <li>Load balancing
      <ul>
        <li>Running containers</li>
        <li>Not dead containers</li>
      </ul>
      </li>
      </ul>
    </li>
  </ul>
</div>
<div class="right-col">
![Image](assets/images/microservice_architecture.png)
</div>
</div>

<small>https://martinfowler.com/articles/microservices.html</small>

---
## Load Balancing

- Expose services to external users
- Distribution of workloads across multiple computing resources
- Optimize resource usage
- Maximize throughput
- Avoid overload of any single resource
- Increase reliability and availability through redundancy

---
# Docker Swarm

---
## Core concepts

<div class="clearfix">
  <div class="left-col">
    <ul>
      <li>Swarm</li>
      <li>Node</li>
      <li>Service</li>
      <li>Tasks</li>
      <li>Secrets</li>
    </ul>
  </div>
  <div class="right-col">

![Image](assets/images/swarm.png)

  </div>
</div>

---
## How nodes work

![Image](assets/images/swarm_architecture.png)

<small>https://docs.docker.com/engine/swarm</small>

---
## How services work

<div class="clearfix">
  <div class="left-col">

  <ul>
    <li>In a service we specify
    <ul>
      <li>Image</li>
      <li>Exposing external ports</li>
      <li>Overlay network for connecting to other services</li>
      <li>CPU and memory limits and reservations</li>
      <li>Update policy</li>
      <li>Number of replicas</li>
    </ul>
    </li>
  </ul> 

  </div>
  <div class="right-col">

![Image](assets/images/swarm_service.png)

  </div>
</div>

<small>https://docs.docker.com/engine/swarm</small>

---
## Services modes

<div class="clearfix">
  <div class="left-col">
  <ul>
    <li>Replicated
      <ul>
        <li>Specify the number of identical tasks you want</li>
      </ul>
    </li>
    <li>Global services
      <ul>
        <li>Service that runs one task on every node</li>
      </ul>
    </li>
  </ul>

  </div>
  <div class="right-col">

![Image](assets/images/swarm_service_mode.png)

  </div>
</div>

<small>https://docs.docker.com/engine/swarm</small>

---
## Configuration

#### Environment variables

```yaml
  web:
    environment:
      - DEBUG
```
#### Environment files

```yaml
  web:
    env_file:
      - web-variables.env
```

---
## Networks

<div class="left-col">
Developer-edition

![Image](assets/images/swarm_network_simple.png)
</div>
<div class="right-col">
Network-guy-edition

![Image](assets/images/swarm_network_advanced.png)
</div>

<small>http://blog.nigelpoulton.com/demystifying-docker-overlay-networking/</small>

Note:

We will learn about the CNM (Container Network Model).

At the end of this lesson, you will be able to:

* Create a private network for a group of containers.
* Use container naming to connect services together.
* Dynamically connect and disconnect containers to networks.
* Set the IP address of a container.

We will also explain the principle of overlay networks and network plugins.

---

## The Container Network Model

The CNM was introduced in Engine 1.9.0 (November 2015).

The CNM adds the notion of a *network*, and a new top-level command to manipulate and see those networks: `docker network`.

```bash
$ docker network ls
NETWORK ID          NAME                DRIVER
6bde79dfcf70        bridge              bridge
8d9c78725538        none                null
eb0eeab782f4        host                host
4c1ff84d6d3f        blog-dev            overlay
228a4355d548        blog-prod           overlay
```

---
## What's in a network?

* A network is a virtual switch.
  - Local, to a single Engine, or global, spanning multiple hosts.
* A network has an IP subnet associated to it.
* Containers connected to a network gets an IP address.
* Containers can be 
 - connected to multiple networks.
 - given per-network names and aliases.

---
## Network implementation details

* A network is managed by a *driver*.
* All normal docker drivers are available.
* A new multi-host driver, *overlay*, is available out of the box.
* More drivers can be provided by plugins (OVS, VLAN...)
* A network can have a custom IPAM (IP allocator).

---
## Secrets

```shell
$ echo "This is a secret" \
  | docker secret create my_secret –


$ docker service create --name redis \
  --secret my_secret redis:alpine


$ docker exec redis \
  cat /run/secrets/my_secret
This is a secret
```

---
## Secrets

![Image](assets/images/swarm_secrets.png)

<small>https://blog.docker.com/2017/02/docker-secrets-management/</small>


---
## The first Swarm

>  ```bash
>  docker swarm init
>  ```

- This should be executed on a first, seed node
- _Warning:_ DO NOT execute `docker swarm init` on multiple nodes!
  - You would have multiple disjoint clusters.

---
## IP address to advertise

- Each node *advertises* its address
  - *"you can contact me on 10.1.2.3:2377"*

- If the node has only one IP address, it is used automatically
- If the node has multiple IP addresses, you **must** specify which one to use
- Specify an IP address or an interface name (`eth0`)
- You can also specify a port number
  - default port is 2377

---
## Using a non-default port number

- Changing the *advertised* port does not change the *listening* port
  - If you only pass `--advertise-addr eth0:7777`, Swarm will still listen on port 2377
  - You will probably need to pass `--listen-addr eth0:7777` as well
- This is to accommodate scenarios where these ports *must* be different
  - port mapping, load balancers...

Example to run Swarm on a different port:

```bash
docker swarm init --advertise-addr eth0:7777 --listen-addr eth0:7777
```

---
## Which IP to use?

- If your nodes have only one IP address, it's safe to let autodetection do the job
  - <small>(Except if your instances have different private and public addresses, e.g.
on EC2, and you are building a Swarm involving nodes inside and outside the
private network: then you should advertise the public address.)</small>

- If you have multiple IPs, pick one which is reachable *by every other node*

- If you are using [play-with-docker](http://play-with-docker.com/), use the IP
address shown next to the node name
  - Or just `docker swarm init --advertise-addr eth0` 

---
## Separate interface for the data path

- You can use different interfaces (or IP addresses) for control and data

_control plane path_

`--advertise-addr` and `--listen-addr`

_data plane path_

`--data-path-addr`

Note:

  This will be used for SwarmKit manager/worker communication, leader election, etc.
  This will be used for traffic between containers

- Both flags can accept either an IP address, or an interface name

  When specifying an interface name, Docker will use its first IP address

---

## Token generation

  ```
  docker swarm init

  Swarm initialized: current node (8jud...) is now a manager.
  ```

- Docker generated two security tokens for our cluster
- Output shows the command to use on other nodes

  ```
    To add a worker to this swarm, run the following command:
      docker swarm join \
      --token SWMTKN-1-59fl4ak4nqjmao1ofttrc4eprhrola2l87... \
      172.31.4.182:2377
  ```

---

## Checking that Swarm mode is enabled

> - Run the traditional `docker info` command:
>  ```bash
>  docker info
>  ```

The output should include:

```
Swarm: active
 NodeID: 8jud7o8dax3zxbags3f8yox4b
 Is Manager: true
 ClusterID: 2vcw2oa9rjps3a24m91xhvv0c
 ...
```

---
## Running our first Swarm mode command

> - List the nodes (well, the only node) of our cluster:
>  ```bash
>  docker node ls
>  ```

The output should look like the following:
```
ID             HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
8jud...ox4b *   node1     Ready   Active        Leader
```

---

## Adding nodes to the Swarm

- A cluster with one node is not a lot of fun
- Let's add more!
- We need the token that was shown earlier
- You wrote it down, right?
- Don't panic, we can easily see it again 😏|

---
## Adding nodes to the Swarm

> - Show the token again
>
> ```bash
> $ docker swarm join-token worker
> docker swarm join --token SWMTKN-1-56at..bz 192.168.0.17:2377
> ```

- Go to second machine

- Copy-paste the `docker swarm join ...` command

---
## Is node in a swarm?

- Stay on `node2` for now!

- We can still use `docker info` to verify

```bash
$ docker info | grep ^Swarm
```
- However, Swarm commands will not work

```bash
$ docker node ls
```

- This is because the node that we added is currently a *worker*
- Only *managers* can accept Swarm-specific commands

---
## View our two-node cluster

- Let's go back to `node1` and see what our cluster looks like
- View the cluster from `node1`, which is a manager:

```bash
docker node ls
ID             HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
8jud...ox4b *  node1     Ready   Active        Leader
ehb0...4fvx    node2     Ready   Active
```

---
## Under the hood: docker swarm init

When we do `docker swarm init`:

- a keypair is created for the root CA of our Swarm
- a keypair is created for the first node
- a certificate is issued for this node
- the join tokens are created

---
## Under the hood: join tokens

- There is one token to *join as a worker*, and another to *join as a manager*.

- The join tokens have two parts:
  - a secret key (preventing unauthorized nodes from joining)
  - a fingerprint of the root CA certificate (preventing MITM attacks)

- If a token is compromised, it can be rotated instantly with

```
docker swarm join-token --rotate <worker|manager>
```

---
## Under the hood: docker swarm join

When a node joins the Swarm:

- it is issued its own keypair, signed by the root CA

- if the node is a manager:

  - it joins the Raft consensus
  - it connects to the current leader
  - it accepts connections from worker nodes

- if the node is a worker:

  - it connects to one of the managers (leader or follower)

---
## Under the hood: cluster communication

- *control plane* is encrypted with AES-GCM; keys are rotated every 12 hours
- Authentication is done with mutual TLS; certificates are rotated every 90 days
- The *data plane* (communication between containers) is not encrypted by default


Note:

- `docker swarm update` allows to change this delay or to use an external CA
- but this can be activated on a by-network basis, using IPSEC,
leveraging hardware crypto if available


---
## Docker Swarm Cheat Sheet

Swarm

```shell
$ docker swarm init --advertise-addr $IP/$NET_INTERFACE
$ docker swarm join --token SWMTKN-1-49n… $MANAGER_IP:2377
$ docker swarm leave
```

Node

```shell
$ docker node ls
$ docker node update --availability drain $NODE_ID
$ docker node update --availability active $NODE_ID
$ docker node promote $NODE_ID
```

---
## Docker Swarm Cheat Sheet

Services

```shell
$ docker service create --name=$SERVICE_ID $IMAGE
$ docker service rm $SERVICE_ID
$ docker service ls
```

Stacks

```shell
$ docker stack deploy --compose-file myComposeFile.yml $NAME
$ docker stack ls
$ docker stack ps
$ docker stack rm
```

---
## Hands On

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/3-Docker-swarm/Exercises.md)

---
## How many managers do we need?

- 2N+1 nodes can (and will) tolerate N failures
  - you can have an even number of managers, but there is no point

- 1 manager = no failure

- 3 managers = 1 failure

- 5 managers = 2 failures (or 1 failure during 1 maintenance)

- 7 managers and more = now you might be overdoing it a little bit

---

## Why not have *all* nodes be managers?

- It's harder to reach consensus in larger groups
- With Raft, writes have to be send to (and be acknowledged by) all nodes
- More nodes = more network traffic
- Bigger network = more latency

---

## What would McGyver do?

---
## How many managers do we need?

- 2N+1 nodes can (and will) tolerate N failures
  - you can have an even number of managers, but there is no point

- 1 manager = no failure

- 3 managers = 1 failure

- 5 managers = 2 failures (or 1 failure during 1 maintenance)

- 7 managers and more = now you might be overdoing it a little bit

---

## Why not have *all* nodes be managers?

- It's harder to reach consensus in larger groups
- With Raft, writes have to be send to (and be acknowledged by) all nodes
- More nodes = more network traffic
- Bigger network = more latency

---

## What would McGyver do?
- If some of your machines are more than 10ms away from each other,
  -  try to break them down in multiple clusters (keeping internal latency low)

- < 9 nodes: all of them are managers
- \> 10 nodes: pick 5 "stable" nodes to be managers
- \> 100 nodes: watch your managers' CPU and RAM
- \> 1000 nodes:

  - if you can afford to have fast, stable managers, add more of them
  - otherwise, break down your nodes in multiple clusters

---

## What's the upper limit?

- We don't know!
- Internal testing at Docker Inc.: 1000-10000 nodes is fine
  - Deployed to a single cloud region
  - One of the main take-aways was *"you're gonna need a bigger manager"*

- Testing by the community: [4700 heterogenous nodes](https://sematext.com/blog/2016/11/14/docker-swarm-lessons-from-swarm3k/)
  - It just works
  - More nodes require more CPU; more containers require more RAM
  - Scheduling of large jobs (70.000 containers) is slow, though (working on it!)