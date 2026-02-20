const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# Fill in the blanks: ____ is more suitable for simple, local development, while ____ is more suitable for complex, production environments

1. [x] Docker Compose, Kubernetes
	> Good. Both tools accomplish the same goal, but on separate complexity scopes
1. [ ] Kubernetes, Docker Compose
	> Because Docker Compose lacks features needed for complicated environments (which most production environments are), Kubernetes is the superior tool in production cases
1. [ ] Kubernetes, Docker
	> Keep in mind that while Kubernetes and Docker Compose handle container orchestration, all Docker does is create containers
1. [ ] Docker, Kubernetes
	> Keep in mind that while Kubernetes and Docker Compose handle container orchestration, all Docker does is create containers

# Order the following Kubernetes resources into the correct scopes (highest scope to lowest scope)<br>If you are confused, reread the [Design](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.5.2-kubernetes?id=design) section above.

1. Cluster
2. Node
3. Pod

# True or False: Making an invalid command to the Kubernetes API can run the risk of breaking resources in your cluster

1. [ ] True
	> Not quite. Refer back to the [Design](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.5.2-kubernetes?id=design) section above to get a firmer grasp on how Kubernetes handles changes to the cluster
1. [x] False
	> Excellent! The great thing about the Kubernetes engine is that *proposed* changes (your commands) must be validated by an API server before any changes are made to etcd

# Fill in the blanks: While Services and Deployments both are used to group pods, ____ are used for the starting/stopping/scaling of pods and ____ are used for the linking/networking of pods

1. [x] Deployments, Services
	> Good. These terms are easy to mix up because they deal with similar things, so this is a good item to commit to memory
1. [ ] Services, Deployments
	> Not quite. These terms are easy to mix up because they deal with similar things, so don't sweat it. Reread the [Services](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.5.2-kubernetes?id=services) and [Deployments](https://bootcamp.devcloudninjas.com/#/3-virtual-machines-containers/3.5.2-kubernetes?id=deployments) definitions above to help commit these to memory

`;

export { rawQuizdown }