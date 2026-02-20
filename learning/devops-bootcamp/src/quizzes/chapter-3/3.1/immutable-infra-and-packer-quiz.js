const rawQuizdown = `
---
shuffleAnswers: true
shuffleQuestions: true
---

# Which statement is true about immutable infrastructure as opposed to mutable infrastructure?

1. [x] Immutable infrastructure has less risk and is less complex
1. [ ] Immutable infrastructure has more risk but is less complex
	> It might prove beneficial to go watch the [What is Mutable vs. Immutable Infrastructure](https://www.hashicorp.com/resources/what-is-mutable-vs-immutable-infrastructure/) video again
1. [ ] Immutable infrastructure has less risk but is more complex
	> It might prove beneficial to go watch the [What is Mutable vs. Immutable Infrastructure](https://www.hashicorp.com/resources/what-is-mutable-vs-immutable-infrastructure/) video again
1. [ ] Immutable infrastructure has more risk and is more complex
	> It might prove beneficial to go watch the [What is Mutable vs. Immutable Infrastructure](https://www.hashicorp.com/resources/what-is-mutable-vs-immutable-infrastructure/) video again

# Which infrastructure model can be described as "updating in place"?

1. [x] Mutable
1. [ ] Immutable
1. [ ] Revolving
1. [ ] Virtual

# Which infrastructure model creates new instances and tears down old ones instead of updating?

1. [ ] Mutable
1. [x] Immutable
1. [ ] Revolving
1. [ ] Virtual

# What is a "golden image" in the context of computer systems and software development?

1. [x] A standardized and pre-configured template of an operating system or software
1. [ ] An image file with a golden hue used for system backgrounds
1. [ ] A cryptographic image used for secure data storage
1. [ ] An image format specifically designed for high-resolution displays

# True or False: Packer can be used to mass-produce VMs that are 100% identical to the provided snapshot, regardless of their platform.

1. [x] True
	> Yes, along with provisioning VMs, one of Packer's main responsibilities is creating identical VM's for different platforms
1. [ ] False 
	> Packer actually *is* capable of creating VMs for multiple platform types all at once. This is one of its many strengths 
`;

export { rawQuizdown }