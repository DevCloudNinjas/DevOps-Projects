# Operating the Swarm

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
## Troubleshooting overlay networks
We want to run tools like ab or httping on the internal network

Ah, if only we had created our overlay network with the --attachable flag ...

Oh well, let's use this as an excuse to introduce New Ways To Do Things

---
## Breaking into an overlay network

- create dummy service on our network

- use `docker exec` to run more processes in this container

```
docker service create --network backend --name debug --mode global \
       alpine sleep 1000000000
```

- Why am I using global scheduling here? Because I'm lazy! 
I'm guaranteed to have an instance on the local node. 

---
## Entering the debug container

Once our container is started we can enter it 

Locate the container and enter it:

``` 
$ docker ps
$ docker exec -ti <containerID> sh
```

---
## Labels

- We can also be fancy and find the ID of the container automatically
- Get the ID of the container and enter it:

```
$ CID=$(docker ps -q --filter label=com.docker.swarm.service.name=debug)
$ docker exec -ti $CID sh
```

---
## Installing our debugging tools

- Ideally, you create your own image, with all your favorite tools
- But we can also dynamically install whatever we need
- Install a few tools:

```
$ apk add --update curl apache2-utils drill
```

---
## Investigating a service

- First, let's check what the dns resolves to
- Use drill or nslookup to resolve the dns:

```
$ drill <service-dns-name>
```

- This give us one IP address. 
  - It is not the IP address of a container. It is a virtual IP address (VIP) for the <service-dns-name> service.

---
## Investigating the VIP
Try to ping the VIP:

```
$ ping <service-dns-name>
```

- It `should` ping. (But this might change in the future.)
  - With Engine 1.12: VIPs respond to ping if a backend is available on the same machine.
  - With Engine 1.13: VIPs respond to ping if a backend is available anywhere.
  - (Again: this might change in the future.)


---
## What if I don't like VIPs?
- Services can be published using two modes: `VIP` and `DNSRR`.
  - With VIP, you get a virtual IP for the service, and a load balancer based on IPVS
  - With DNSRR, you get the former behavior (from Engine 1.11), 
  - where resolving the service yields the IP addresses of all the containers for this service

- You change this with
  - `docker service create --endpoint-mode [VIP|DNSRR]`

---
## Looking up VIP backends

 - You can also resolve a special name: `tasks.<name>`
 - It yelds all IP addresses of the containers for a given service

```
$ drill tasks.<service-dns-name>
```

This should list all IP addresses.

---
## Hands On

#### Playing with overlay networks

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/3.1-OperatingSwarm/1-debugging)

---
# Securing overlay networks

## Follow along on play-with-docker

---
## Securing overlay networks

- By default, overlay networks are using plain VXLAN encapsulation
  - (~Ethernet over UDP, using SwarmKit's control plane for ARP resolution)
- Encryption can be enabled on a per-network basis
  - (It will use IPSEC encryption provided by the kernel, leveraging hardware acceleration)
- This is only for the overlay driver
  - (Other drivers/plugins will use different mechanisms)

---
## Creating two networks

Let's create two networks for testing purposes

- Create an "insecure" network:

```
docker network create insecure --driver overlay --attachable
```

- Create a "secure" network:

```
docker network create secure --opt encrypted --driver overlay --attachable
```

Make sure that you don't typo that option
<br> _**errors are silently ignored!**_

---
## Deploying a web server both networks

- Let's use good old NGINX
- Attach it to both networks
- Use placement constraint to make sure that it is on a different node

Create a web server running somewhere else:
```
$ docker service create --name web \
       --network secure --network insecure \
       --constraint node.hostname!=node1 \
       nginx
```

---
## Sniff HTTP traffic

- We will use ngrep, which allows to grep for network traffic
- We will run it in a container, using host networking to access the host's interfaces
- Sniff network traffic and display all packets containing "HTTP":

```
$ docker run --net host jpetazzo/netshoot ngrep -tpd eth1 HTTP \
   | grep google
```

---
## Sniffing traffic !

- Let's see if we can intercept our traffic with Google!
- Open a new terminal
- Issue an HTTP request to Google (or anything you like):

```
$ curl google.com
```

- The ngrep container will display one # per packet traversing the network interface.
- When you do the curl, you should see the HTTP request in clear text in the output.

---
## Sniff traffic on overlay networks

- Node with `web` container on:

```
$ docker run --net host jpetazzo/netshoot ngrep -tpd eth0 HTTP
```

- Any other node:

```
docker run --rm --net insecure nicolaka/netshoot curl web
```
 - Now do the same through the secure network:

```
docker run --rm --net secure nicolaka/netshoot curl web
```

<small>When you run the first command, you will see HTTP fragments. 
<br>However, when you run the second one, only # will show up.
</small>