# Playing on overlay networks

Start with a swarm cluster with at least one machine in.

Then create a new network with the __overlay driver__.

```
$ docker network create...
``` 

Next start a debug container

```
$ docker service create --network debugnetwork --name debug --mode global alpine sleep 1000000000
```

## Create some stuff to explore

Create a new swarm service on the __debugnetwork__ network, and give it the name __testme_.

Scale the service up to 5 replicas using the `docker service scale` command.

## Entering the debug container

Once all our container is started. You should enter the debug container using `docker exec -it`

## Installing our debugging tools

Install a few tools in the debug container

```
$ apk add --update curl apache2-utils drill
```

Now lets look at the virtual IP and the list of actual IP addresses

- First, let's check what the dns resolves to
- Use drill toresolve the dns:

```
$ drill testme
```

This returns the VIP. Now try the same with the special `tasks.testme` dns.

## Trying out endpoint modes

Create a new __testMeDnsrr__ service on the _correct network_ with the  `--endpoint-mode DNSRR` parameter, and _scale it to 5 instances_.

Use the same `drill` commands on this new service from the debug container.

This should list all IP addresses for both types of dns lookups.

