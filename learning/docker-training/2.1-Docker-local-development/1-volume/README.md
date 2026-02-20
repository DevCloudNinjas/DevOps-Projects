# Our first volume

## Working on the "namer" application

* We have to work on some application whose code is at:

  https://github.com/jpetazzo/namer.

Let's start by downloading the code.

```bash
$ git clone https://github.com/jpetazzo/namer
```

## Building and running the "namer" application

* Let's build the application with the `Dockerfile`!

```bash
$ docker build -t namer .
```

Then run it. *We need to expose its ports.*

```bash
$ docker run -dP namer
```

Check on which port the container is listening. And access it in your browser.

## Local development - fast

Now. We need to update the code, and for this we will:

  * Use a *volume* to mount local files into the container
  * Make changes locally
  * Changes are reflected into the container

First tell Docker to map the current directory to `/src` in the container.

```bash
$ docker run -d -v $(pwd):/src -P namer
```

* `-d`: the container should run in detached mode (in the background).
* `-v`: the following host directory should be mounted inside the container.
* `-P`: publish all the ports exposed by this image.
* `namer` is the name of the image we will run.
* We don't specify a command to run because is is already set in the Dockerfile.

The `-v` flag mounts a directory from your host into your Docker container.

The flag structure is:

```bash
[host-path]:[container-path]:[rw|ro]
```

* If `[host-path]` or `[container-path]` doesn't exist it is created.
* You can control the write status of the volume with the `ro` and `rw` options.
* If you don't specify `rw` or `ro`, it will be `rw` by default.

## Testing the development container

Check the port used by our new container.

```bash
$ docker ps -l
CONTAINER ID  IMAGE  COMMAND  CREATED        STATUS  PORTS                   NAMES
045885b68bc5  namer  rackup   3 seconds ago  Up ...  0.0.0.0:32770->9292/tcp ...
```

Open the application in your web browser.

Our customer really doesn't like the color of our text. Let's change it.
Edit the `company_name_generator.rb` file in your favorite editor, and change the `color` to your favodite color!

## Viewing your changes

Reload the application in our browser.
The color should now have changed!
Without you having rebuilt the image, or started a new container.

## Trash your servers and burn your code

*(This is the title of a
[2013 blog post](http://chadfowler.com/2013/06/23/immutable-deployments.html)
by Chad Fowler, where he explains the concept of immutable infrastructure.)*

Let's mess up majorly with our container.

Try breaking the ruby syntax in the `company_name_generator.rb` file. Does it still work in the browser? No?
Now, how can we fix this?

Our old container (with the blue version of the code) is still running.
And still working, because it has a full build image with all files in, and not a mapped volume.

## Immutable infrastructure in a nutshell

* Instead of *updating* a server, we deploy a new one.
* This might be challenging with classical servers, but it's trivial with containers.
* In fact, with Docker, the most logical workflow is to build a new image and run it.
* If something goes wrong with the new image, we can always restart the old one.
* We can even keep both versions running side by side.

If this pattern sounds interesting, you might want to read about *blue/green deployment*
and *canary deployments*.

## Improving the workflow

The workflow you just did is nice, but it requires us to:

* keep track of all the `docker run` flags required to run the container,
* inspect the `Dockerfile` to know which path(s) to mount,
* write scripts to hide that complexity.

There has to be a better way!

## Exercise: Docker Compose to the rescue

Instead of looking at the `docker-compose.yml` in the repository, try to make your own.

Take the docker commands that we have used so fare, and write a new `my-docker-compose.yml` file that we can use for our "namer" app.

_Hint:_ It should contain a __build__ element that defines how to build the container, a __volumes__ element that defines that to map where, and a __ports__ element that allows us to access the container.

Now try it:

```bash
$ docker-compose up -d -f my-docker-compose.yml
```

## Recap of the development workflow

1. Write a Dockerfile to build an image containing our development environment.
   <br/>
   (Rails, Django, ... and all the dependencies for our app)

2. Start a container from that image.
   <br/>
   Use the `-v` flag to mount our source code inside the container.

3. Edit the source code outside the containers, using regular tools.
   <br/>
   (vim, emacs, textmate...)

4. Test the application.
   <br/>
   (Some frameworks pick up changes automatically.
   <br/>Others require you to Ctrl-C + restart after each modification.
   <br/>Some, like NodeJs, has framworks specifically for development that will watch the files on disk to always run the latest version.)

5. Iterate and repeat steps 3 and 4 until satisfied.

6. When done, commit+push source code changes.

## Debugging inside the container

Docker has a command called `docker exec`.

It allows users to run a new process in a container which is already running.

If sometimes you find yourself wishing you could SSH into a container: you can use `docker exec` instead.

You can get a shell prompt inside an existing container this way, or run an arbitrary process for automation.

## `docker exec` exercise

Start the namer application with docker run:

```bash
$ docker build -t namer .
$ docker run -dP namer
$ docker ps -l
```

Get the id of the namer container and enter the container like this:

```bash
$ # You can run ruby commands in the area the app is running and more!
$ docker exec -it <yourContainerId> bash
root@5ca27cf74c2e:/opt/namer# irb
irb(main):001:0> [0, 1, 2, 3, 4].map {|x| x ** 2}.compact
=> [0, 1, 4, 9, 16]
irb(main):002:0> exit

$ # To exit the container and go back to your own machine type exit
$ exit
```

## Stopping the container

Now that we're done stop all your running containers and remove them.
