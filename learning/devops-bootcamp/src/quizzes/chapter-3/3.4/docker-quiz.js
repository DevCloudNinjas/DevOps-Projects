const rawQuizdown = `
---
shuffleAnswers: true
---

# Assume you made a Dockerfile that, when built into an image and ran, will install a handful of packages and log a success string. If you are on MacOS and your friend is on Windows, can you send them the Dockerfile and expect the container to build and operate exactly the same?

1. [x] Yes
	> Excellent, this is one of the main points of Docker and containers as a whole! You can share images between different environments and they *will* behave the same. They greatly help relieve the "It works on my machine" allegations
1. [ ] No
	> Not quite. The container actually *will* behave the same as this is one of Docker's main strengths. Refer again to the components of containers (third bullet point demonstrated here) in these [Docker docs](https://docs.docker.com/get-started/#what-is-a-container)

# What is the difference between a Docker image and a Docker container?

1. [x] A container is a runtime instance of an image
	> Good. The image is what defines the container and the container is what is actually running
1. [ ] An image is a runtime instance of a container
	> Not quite. Refer back to the [Images and Containers](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.4-containers?id=images-and-containers) section above
1. [ ] The two terms can be used interchangeably
	> Not quite. Refer back to the [Images and Containers](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.4-containers?id=images-and-containers) section above

# 1/2 - Suppose you need a very specific set of dependencies and packages installed to your container, but no base image exists that has them already installed for you. What problems does this pose? Select all that apply

- [x] Each distribution of the Dockerfile, when building the image, will have to install the packages since they aren't included in the base image
	> Good. The more that is aleady done by the time you go to build, the better
- [x] Manually installing them into the image will add complexity and slow build time
	> Good. The more directives that a Dockerfile contains, the more complexity and build time the image will have
- [x] Installing the dependencies instead of having them included in the base image will increase the image size
	> Good. One of the main (and hardest) goals with Docker images is keeping their size down as much as possible
- [ ] Docker only allows you to install a limit of 3 dependencies outside of the base image, so you'll have to choose what to install and what not to 
	> Thankfully this isn't the case. You can install all the dependencies that your heart desires
- [ ] There are no issues, it is standard convention to install them yourself in the image definition
	> Nice try. There definitely are some issues that are raised in this scenario

# 2/2 - How can you remedy the issue from the previous question? Select all that apply

- [x] Make a separate image that installs the packages for you and then use *that* image as your base image
	> Good. This isn't a bad solution to the problem and will keep the end image size down greatly
- [x] Utilize a multi stage build, where the first stage installs the packages and the second copies them into the final image
	> Good. This is a very advanced, and very great approach to solve this problem
- [ ] There is nothing you can do, this is one of Docker's downfalls as you can only use the base images they have available
	> You actually *can* create your own base image. In fact, any image can be used as a base image for others to build off of

# True or False: If you build the same Docker image twice, the build time will be shorter the second time around

1. [x] True
	> Good. This is because the image build will utilize caching to greatly speed up unchanged layers. This is one of Docker's best strengths
1. [ ] False
	> Not quite. Refer back to the [Layers](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.4-containers?id=layers) section above

# True or False: If you run the same Docker container twice, the start time will be shorter the second time around

1. [ ] True
	> Not quite. Nothing is being built or configured when running a container, it's simply an execution of what was already built (the image)
1. [x] False
	> Good. The start time for a container doesn't change for the most part (some variables can affect the start time but you shouldn't observe a difference in subsequesnt runs with the same control)

`;

export { rawQuizdown }