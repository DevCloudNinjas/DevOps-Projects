# Docker Registry

In this section we'll be learning about Docker Registry. As you've learned previously, Docker has a public online image registry which allows users to store and download the Docker images they've created. You can view and search the images in this registry using the [Dockerhub website](https://hub.docker.com/).

In some situations it might be useful to manage your own collection of Docker images. In this case you could set up an internal Docker Registry to store them in.

![build image](img-addendum/build_light.svg ':size=100x100 :class=light-mode-icon :alt= build image; light mode')
![build image](img-addendum/build_dark.svg ':size=100x100 :class=dark-mode-icon :alt= build image; dark mode')

## Setup a Docker Registry

This is a group exercise. If you are just one person, that's okay; we believe in you! However, try to complete this as a group if possible.

1. Read this documentation on [Docker Registry](https://docs.docker.com/registry/)
2. Using the documentation, one person should set up Docker Registry, either on your own machine or a virtual machine.
3. Confirm that the registry can be accessed from the machine that it is running on.
4. On another machine, another person should try to access the registry remotely.
5. Docker will not connect to a Registry over an insecure connection, so set up [self signed certificates](https://docs.docker.com/registry/insecure/#use-self-signed-certificates).
6. Confirm that you can connect to your registry from a remote machine.

## Using Docker Registry

1. Read the documentation about [Docker tags](https://docs.docker.com/engine/reference/commandline/tag/).
2. Create a Docker image, and give it a name without any version tag.
3. Add a tag to the image you just created, giving it the tag `1.0`.
4. List the images you just created. Notice how docker displays the image with multiple tags.
5. Push your image up to your Docker Registry.
6. Delete the local image from Docker.
7. Run a container with the image you uploaded to the registry. Verify it downloads and runs correctly.
8. Create a new version of your image by making a change to the Dockerfile, and build it with the `-t` option to tag it with `1.1`.
9. Update the `latest` tag to point to your new image, and give the tag `stable` to your `1.0` image.
10. Push all your images up to the Docker Registry you set up.
11. Delete your local Docker image.
12. Upgrade your running container to the new image version.
13. Have your group or partner experiment by pulling down your images from the registry. Take note of the different tags you can use to refer to the same images.

# Deliverable

- A Docker Registry setup accessible from remote machines.
- Discuss why you might choose to use a private Docker Registry instead of Docker's public repository.
- Discuss the limitations of Docker Registry compared to Dockerhub.
- Discuss how Docker tags work, and how they can be used.
