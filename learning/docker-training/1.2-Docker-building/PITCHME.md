# Building with Docker

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
# `CMD` and `ENTRYPOINT`

---
## Defining a default command

When people run our container, we want to greet them with a nice hello message, and using a custom font.

For that, we will execute:

```bash
figlet -f script hello
```

* `-f script` tells figlet to use a fancy font.

* `hello` is the message that we want it to display.

---

## Adding `CMD` to our Dockerfile

Our new Dockerfile will look like this:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN ["apt-get", "install", "figlet"]
CMD figlet -f script hello
```

* `CMD` defines a default command to run when none is given.
* It can appear at any point in the file.
* Each `CMD` will replace and override the previous one.

Note:
* As a result, while you can have multiple `CMD` lines, it is useless.

---
## Build and test our image

Let's build it:

```bash
$ docker build -t figlet .
...
Successfully built 042dff3b4a8d
```

And run it:

```bash
$ docker run figlet
 _          _   _       
| |        | | | |      
| |     _  | | | |  __  
|/ \   |/  |/  |/  /  \_
|   |_/|__/|__/|__/\__/ 
```

---

## Overriding `CMD`

If we want to get a shell into our container (instead of running
`figlet`), we just have to specify a different program to run:

```bash
$ docker run -it figlet bash
root@7ac86a641116:/# 
```

* We specified `bash`.
* It replaced the value of `CMD`.

---

## Using `ENTRYPOINT`

We want to be able to specify a different message on the command line,
while retaining `figlet` and some default parameters.

In other words, we would like to be able to do this:

```bash
$ docker run figlet salut
           _            
          | |           
 ,   __,  | |       _|_ 
/ \_/  |  |/  |   |  |  
 \/ \_/|_/|__/ \_/|_/|_/
```


We will use the `ENTRYPOINT` verb in Dockerfile.

---

## Adding `ENTRYPOINT` to our Dockerfile

```dockerfile
FROM ubuntu
RUN apt-get update
RUN ["apt-get", "install", "figlet"]
ENTRYPOINT ["figlet", "-f", "script"]
```

* `ENTRYPOINT` defines a base command (and its parameters) for the container.
* The command line arguments are appended to those parameters.

Note:

* Like `CMD`, `ENTRYPOINT` can appear anywhere, and replaces the previous value.
Why did we use JSON syntax for our `ENTRYPOINT`?

* When CMD or ENTRYPOINT use string syntax, they get wrapped in `sh -c`.

* To avoid this wrapping, we can use JSON syntax.

What if we used `ENTRYPOINT` with string syntax?

```bash
$ docker run figlet salut
```

This would run the following command in the `figlet` image:

```bash
sh -c "figlet -f script" salut
```

---

## Build and test our image

Let's build it:

```bash
$ docker build -t figlet .
...
Successfully built 36f588918d73
```

And run it:

```bash
$ docker run figlet salut
           _            
          | |           
 ,   __,  | |       _|_ 
/ \_/  |  |/  |   |  |  
 \/ \_/|_/|__/ \_/|_/|_/
```

---

## Using `CMD` and `ENTRYPOINT` together

* `ENTRYPOINT` will define the base command for our container.
* `CMD` will define the default parameter(s) for this command.
* They *both* have to use JSON syntax.

---

## `CMD` and `ENTRYPOINT` together

Our new Dockerfile will look like this:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN ["apt-get", "install", "figlet"]
ENTRYPOINT ["figlet", "-f", "script"]
CMD ["hello world"]
```

Note: 
* `ENTRYPOINT` defines a base command (and its parameters) for the container.

* If we don't specify extra command-line arguments when starting the container,
  the value of `CMD` is appended.

* Otherwise, our extra command-line arguments are used instead of `CMD`.

---

## Build and test our image

Let's build it:

```bash
$ docker build -t figlet .
...
Successfully built 6e0b6a048a07
```

Run it without parameters:

```bash
$ docker run figlet
 _          _   _                             _        
| |        | | | |                           | |    |  
| |     _  | | | |  __             __   ,_   | |  __|  
|/ \   |/  |/  |/  /  \_  |  |  |_/  \_/  |  |/  /  |  
|   |_/|__/|__/|__/\__/    \/ \/  \__/    |_/|__/\_/|_/
```

---

## Overriding the image default parameters

Now let's pass extra arguments to the image.

```bash
$ docker run figlet hola mundo
 _           _                                               
| |         | |                                      |       
| |     __  | |  __,     _  _  _           _  _    __|   __  
|/ \   /  \_|/  /  |    / |/ |/ |  |   |  / |/ |  /  |  /  \_
|   |_/\__/ |__/\_/|_/    |  |  |_/ \_/|_/  |  |_/\_/|_/\__/ 
```

We overrode `CMD` but still used `ENTRYPOINT`.

---

## Overriding `ENTRYPOINT`

What if we want to run a shell in our container?

We cannot just do `docker run figlet bash` because
that would just tell figlet to display the word "bash."

We use the `--entrypoint` parameter:

```bash
$ docker run -it --entrypoint bash figlet
root@6027e44e2955:/# 
```

---
# Copying files during the build

---

## Build some C code

We want to build a container that compiles a basic "Hello world" program in C.

Here is the program, `hello.c`:

```bash
int main () {
  puts("Hello, world!");
  return 0;
}
```

Let's create a new directory, and put this file in there.

Then we will write the Dockerfile.

---

## The Dockerfile

```bash
FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential
COPY hello.c /
RUN make hello
CMD /hello
```

@[3](On Debian and Ubuntu, the package `build-essential` will get us a compiler.)

@[3](When installing it, don't forget to specify the `-y` flag, otherwise the build will fail (since the build cannot be interactive).)

@[4](Then we will use `COPY` to place the source file into the container.)

---

## Testing our C program

* Create `hello.c` and `Dockerfile` in the same direcotry.
* Run `docker build -t hello .` in this directory.
* Run `docker run hello`, you should see `Hello, world!`.

Success!

---

## `COPY` and the build cache

* Run the build again.
* Now, modify `hello.c` and run the build again.
* Docker can cache steps involving `COPY`.
* Those steps will not be executed again if the files haven't been changed.

---

## Details

* You can `COPY` whole directories recursively.
* Older Dockerfiles also have the `ADD` instruction.
  <br/>It is similar but can automatically extract archives.
* If we really wanted to compile C code in a compiler, we would:
  * Place it in a different directory, with the `WORKDIR` instruction.
  * Even better, use the `gcc` official image.

---
# Multi-stage builds

---
## Multi-stage builds

* In the previous example, our final image contain:
  * our `hello` program
  * its source code
  * the compiler
* Only the first one is strictly necessary.
* We are going to see how to obtain an image without the superfluous components.

---

## Multi-stage builds principles

* At any point in our `Dockerfile`, we can add a new `FROM` line.
* This line starts a new stage of our build.
* Each stage can access the files of the previous stages with `COPY --from=...`.
* When a build is tagged (with `docker build -t ...`), the last stage is tagged.
* Previous stages are not discarded: they will be used for caching, and can be referenced.

---

## Multi-stage builds in practice

* Each stage is numbered, starting at `0`
* We can copy a file from a previous stage by indicating its number, e.g.:

  ```dockerfile
  COPY --from=0 /file/from/first/stage /location/in/current/stage
  ```

* We can also name stages, and reference these names:

  ```dockerfile
  FROM golang AS builder
  RUN ...
  FROM alpine
  COPY --from=builder /go/bin/mylittlebinary /usr/local/bin/
  ```

---

## Multi-stage builds for our C program

We will change our Dockerfile to:

* give a nickname to the first stage: `compiler`
* add a second stage using the same `ubuntu` base image
* add the `hello` binary to the second stage
* make sure that `CMD` is in the second stage 

The resulting Dockerfile is on the next slide.

---

## Multi-stage build `Dockerfile`

Here is the final Dockerfile:

```dockerfile
FROM ubuntu AS compiler
RUN apt-get update
RUN apt-get install -y build-essential
COPY hello.c /
RUN make hello
FROM ubuntu
COPY --from=compiler /hello /hello
CMD /hello
```

Let's build it, and check that it works correctly:

```bash
docker build -t hellomultistage .
docker run hellomultistage
```

---
## Comparing single/multi-stage build image sizes

List our images with `docker images`, and check the size of:
- the `ubuntu` base image,
- the single-stage `hello` image,
- the multi-stage `hellomultistage` image.

We can achieve even smaller images if we use smaller base images.

Note:

However, if we use common base images (e.g. if we standardize on `ubuntu`),
these common images will be pulled only once per node, so they are
virtually "free."

---
## Building images

---
## Docker Cheat Sheet

Building

```shell
$ docker build -t my-image .
$ docker build -t my-image -f my.dockerfile .
```

Running

```shell
$ docker run my-image
$ docker run -p 9000:8080 --name my-container my-image
```

Cleanup

```shell
$ docker stop my-container // Or container id from docker ps
$ docker rm my-container   // Or container id from docker ps
```

---
## Hands On

#### Creating images

#### Exercises [here](https://github.com/mogensen/docker-handson-training/tree/master/1.2-Docker-building/1-building-images)

---
## Docker Stop

Did you notice that the `docker stop` took a long time for the python app?

---
## `docker stop`
_And also `docker-compose stop`_

> The main process inside the container will receive `SIGTERM`, and after a grace period, `SIGKILL`.


---
### `addition.py`

`web.py` does not handle `SIGTERM` out of the box.

- Docker sends the `SIGTERM` signal
- the container doesn't react to this signal
- 10 seconds later, since the container is still running, Docker sends the `SIGKILL` signal
- this terminates the container

---
# Image and tags

---
## Image and tags

- Images can have tags.
- Tags define image versions or variants.
- `docker pull ubuntu` will refer to `ubuntu:latest`.
- The `:latest` tag is generally updated often.

---
## When to (not) use tags

- Don't specify tags:
  - When doing rapid testing and prototyping.
  - When experimenting.
  - When you want the latest version.

- Do specify tags:
  - When recording a procedure into a script.
  - When going to production.
  - To ensure that the same version will be used everywhere.
  - To ensure repeatability later.
