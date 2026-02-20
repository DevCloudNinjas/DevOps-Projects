#  Creating your first Images with Docker

## About this exercise set

> To help the users of this exercise to learn how to use docker and where to get help when they are stuck in the real world, I have tried to create exercises that forces the user to look in documentation and experiment.
>
> **This means, that the exercise set is not a simple copy & paste exercise**

This folder contains a very small docker container, capable of adding two numbers.

## Looking at the order of the layers when building

Start by using the `addition.py` from last exercise, with the following `dockerfile`:

## Bad `dockerfile`

```dockerfile
FROM python:2.7-alpine
COPY addition.py /
RUN pip install web.py
ENTRYPOINT ["python", "addition.py"]
```

### Build the app

Build the image using the following command.

```shell
$ time docker build -t add-a-tron-server .
```

This builds the images for us and when the is done the `time` command prints the total time spend on the build.
If you do this a couple of times you should see that all the docker cache magic makes the build very fast.

__Exercise__: Try to edit the `addition.py` file. How long does the build take now? 


## Good `dockerfile`

Now lets try to sort the lines after what changes most rarely.

```dockerfile
FROM python:2.7-alpine
ENTRYPOINT ["python", "addition.py"]
RUN pip install web.py
COPY addition.py /
```

### Build the app

__Exercise__: After a couple of builds you should see that all the docker cache magic makes the build very fast.
BUT Try to edit the `addition.py` file (to a version that you have not had before; docker also caches older versions of the files).
How long does the build take now?
