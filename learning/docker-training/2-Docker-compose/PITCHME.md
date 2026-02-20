# Docker Compose

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
## Docker Compose

Defining and running multi-container Docker applications

---
## Multiple container application

```shell
$ docker pull mysql

$ docker pull wordpress

$ docker run -d --name=db -e MYSQL_ROOT_PASSWORD=root mysql

$ docker run --name=wp -p 8000:80 --link db:db \
	-e WORDPRESS_DB_HOST=db \
	-e WORDPRESS_DB_PASSWORD=root wordpress
```

@[1](Pull mysql container)
@[3](Pull wordpress container)
@[5](Start mysql container named `db` with root password)
@[7-9](Start wordpress container linked with `db` container)

---
## Docker Compose - YAML

```yaml
version: '3'
services:
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
  wp:
    depends_on:
      - db
    image: wordpress
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_PASSWORD: root
```

@[2](Define all services for application)
@[3-6](Define mysql container named `db`)
@[7-15](Define wordpress container named `wp`)
@[8-9](depends_on will not wait for `db` to be "ready" before starting `wp`)

---
## Docker Compose - YAML

```yaml
version: '3'
services:
  db:
   image: mysql
   environment:
    MYSQL_ROOT_PASSWORD: root
  wp:
   depends_on:
    - db
   image: wordpress
   ports:
    - "8000:80"
   environment:
    WORDPRESS_DB_HOST: db
    WORDPRESS_DB_PASSWORD: root
```

```shell
$ docker-compose up
$ docker-compose ps
$ docker-compose stop
```

---

## Compose file versions

- Version 1 directly has the various containers
  - (`www`, `redis`...) at the top level of the  file.

- Version 2 has multiple sections:
  * `version` is mandatory and should be `"2"`.
  * `services` is mandatory and corresponds to the content of the version 1 format.
  * `networks` is optional and indicates to which networks   containers should be connected.
  * `volumes` is optional and can define volumes to be used and/or shared by the containers.

- Version 3
  * adds support for deployment options (scaling, rolling updates, etc.)

---
# Usages of Compose

---
## Compose Use cases

- Document how to start a given image.
  - ports, configuration, networks, ip, privileges
- Development replacement for a cluster
  - Startup all/needed services in microservice application
- Starting multi-container application on server

---
## Hands On

#### Docker compose

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/2-Docker-compose/1-compose)

---
# Automated builds

---
### The goodness of automated builds

- You can link a Docker Hub repository with a GitHub or BitBucket repository
- Each push to GitHub or BitBucket will trigger a build on Docker Hub
- If the build succeeds, the new image is available on Docker Hub
- You can map tags and branches between source and container images
- If you work with public repositories, this is free

---
## Hands On

#### Automated builds

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/2-Docker-compose/2-automated-builds)
