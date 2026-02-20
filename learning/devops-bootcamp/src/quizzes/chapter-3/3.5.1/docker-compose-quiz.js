const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# True or False: In your Docker Compose file, you can only reference images that you have locally

1. [ ] True
	> Actually, you are able to pull images from Docker Hub or other image repositories. If you want to try, you can push your images to Docker Hub and then reference them in the Compose yaml file. They'll get pulled down and then used
1. [x] False
	> Good, you can either use local images or images from Docker Hub or other image repositories

# True or False: In your Docker Compose file, you always have to use pre-built images, and cannot build them in the moment from Dockerfiles

1. [ ] True
	> Not quite, Docker Compose actually gives you the freedom of either using pre-built images, or building fresh from a Dockerfile
1. [x] False
	> Correct. You have to specify which method in your Compose yaml file by using different directives, but you can either pull an already-built image, or build one from a local Dockerfile

#	Which of the following advantages does Docker Compose offer compared to manually managing Docker containers? Select all that apply

- [x] Orchestration of multiple containers
	> Good. You can easily declare multiple containers to be used in tandem
- [ ] Procedural configuration using manual commands
	> This is how manual configuration works. Docker Compose offers configuration yaml files to easily orchestrate configuration
- [x] Automatic creation of default networks for services
	> Good. If you are trying to link separate Docker containers manually, there is necessary work to be done for networking. Compose does this for you
- [ ] Scalability of services
	> Not quite. Out of the box, Docker Compose doesn't allow you to scale containers (quickly spin up or down number of replicas of a container to split the workload). This is partly why Compose isn't well-suited for complex production environments. In the next section, you'll learn about Kubernetes, a tool that *can* do things such as scaling 
- [x] Ease of persistent data storage options
	> Good. You can manually attach volumes to containers and maintain them, but Compose greatly simplifies the process

# Fill in the blanks: Docker is a ____ tool whereas Docker Compose is a ____ tool

1. [ ] container orchestration, containerization
1. [ ] build, container orchestration
1. [ ] build, containerization
1. [x] containerization, container orchestration

`;

export { rawQuizdown }