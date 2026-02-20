const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# What are the key distinctions between containers and virtual machines in terms of resource utilization? Select all that apply

- [x] Containers share the host operating system's kernel, while VMs run their own operating system kernel
	> Good. This was the big revelation with containers that keeps them lightweight and easily scalable, HOWEVER there is a trade off. Because containers all share a kernel, if any one of them gets compromised (pwned), the attacker will have access to all of them. Since VMs have their own kernels, an attack on any one of them won't directly grant access to the rest. These tradeoffs are important to keep in mind when making decisions between VMs and containers
- [x] Containers are stateless (ephemeral), while VMs can retain state between executions
	> Good. While VMs maintain state across multiple runs, containers do not due to their ephemeral nature. It is not uncommon to attach volumes to containers to maintain state for you, and you will explore these methods later
- [ ] Containers use more system resources compared to VMs
	> Not quite, it's actually the opposite!
- [ ] Containers require hypervisors for isolation, whereas VMs do not
	> Not quite, it's actually the opposite!

# How do containers and virtual machines differ in terms of deployment speed and efficiency?

1. [x] Containers offer faster deployment and higher efficiency compared to VMs
	> Good. Because containers are lightweight, they can be deployed much quicker than VMs, and utilize resources better making them more efficient
1. [ ] Containers are slower to deploy than VMs and offer lower efficiency
	> Due to being lightweight, containers actually deploy quicker than VMs
1. [ ] Containers are slower to deploy but provide better efficiency due to their lightweight nature
	> Containers *are* lightweight which gives them better efficiency, but it also makes them faster to deploy
1. [ ] VMs and containers have similar deployment speeds and efficiency
	> Not quite. One of the main advantages to containers is that they outperform VMs in these fields

`;

export { rawQuizdown }