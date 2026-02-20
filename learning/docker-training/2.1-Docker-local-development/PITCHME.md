# Local development workflow with Docker

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
## Containerized local development environments

We want to solve the following issues:

- "Works on my machine"
- "Not the same version"
- "Missing dependency"

By using Docker containers, we will get a consistent development environment.

---

## Working on the "namer" application

* We have to work on some application whose code is at:

  https://github.com/jpetazzo/namer.

* What is it? We don't know yet!
* Let's download the code.

```bash
$ git clone https://github.com/jpetazzo/namer
```

---

## Looking at the code

```bash
$ cd namer
$ ls -1
company_name_generator.rb
config.ru
docker-compose.yml
Dockerfile
Gemfile
```

Aha, a `Gemfile`! This is Ruby. Probably. We know this. Maybe?

---

## Looking at the `Dockerfile`

```dockerfile
FROM ruby
MAINTAINER Education Team at Docker <education@docker.com>

COPY . /src
WORKDIR /src
RUN bundler install

CMD ["rackup", "--host", "0.0.0.0"]
EXPOSE 9292
```

* This application is using a base `ruby` image.
* The code is copied in `/src`.
* Dependencies are installed with `bundler`.
* The application is started with `rackup`.
* It is listening on port 9292.

---

## Building and running the "namer" application

* Let's build the application with the `Dockerfile`!

```bash
$ docker build -t namer .
```

* Then run it. *We need to expose its ports.*

```bash
$ docker run -dP namer
```

* Check on which port the container is listening.

```bash
$ docker ps -l
```

---
## Connecting to our application

* Point our browser to our Docker node, on the port allocated to the container.
* Hit "reload" a few times.
* This is an enterprise-class, carrier-grade, ISO-compliant company name generator!

  (With 50% more bullshit than the average competition!)

---
## Making changes to the code

- Option 1:
  * Edit the code locally
  * Rebuild the image
  * Re-run the container
- Option 2:
  * Enter the container (with `docker exec`)
  * Install an editor
  * Make changes from within the container
- Option 3:
  * Use a *volume* to mount local files into the container
  * Make changes locally
  * Changes are reflected into the container

---
## Understanding volumes

* Volumes are *not* copying or synchronizing files between the host and the container.
* Volumes are *bind mounts*: a kernel mechanism associating a path to another.
* Bind mounts are *kind of* similar to symbolic links, but at a very different level.
* Changes made on the host or on the container will be visible on the other side.

  (Since under the hood, it's the same file on both anyway.)

---
## Hands On

#### Playing with docker containers

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/2.1-Docker-local-development/1-volume)

---
## Section summary

We've learned how to:

* Share code between container and host.

* Set our working directory.

* Use a simple local development workflow.
