const rawQuizdown = `

# You are working on a new personal project and are designing a basic web app. Currently you are at the early stages of development and aren't hosting your project anywhere (ie you are using localhost to run)<br>What service ecosystem are you currently experiencing?

1. [x] Self-Managed
	> Good. This is as simple as it gets. You supply everything that your app needs and aren't outsourcing for any of it
1. [ ] Infrastructure as a Service
1. [ ] Container as a Service
1. [ ] Platform as a Service
1. [ ] Function as a Service
1. [ ] Software as a Service

# Your app is relatively small, so when you start looking into hosting it, you know you can do so relatively cheaply and use minimal resources. What service ecosystem would be a good fit for hosting your app?

1. [ ] Self-Managed
1. [x] Infrastructure as a Service
	> Good. You can explore service offerings such as Amazon's EC2 or Azure's VM
1. [ ] Container as a Service
1. [ ] Platform as a Service
1. [ ] Function as a Service
1. [ ] Software as a Service

# Your professor is telling you that your project is too simple. Without touching the app too much, you decide to increase complexity on the hosting side of things by exploring methods to host using Kubernetes features. What service ecosystem should you explore?

1. [ ] Self-Managed
1. [ ] Infrastructure as a Service
1. [x] Container as a Service
	> Good. You can explore service offerings such as Amazon's ECS/EKS or Azure's AKS
1. [ ] Platform as a Service
1. [ ] Function as a Service
1. [ ] Software as a Service

# At the end of the day you decide to wind down by watching a movie on Netflix. What service ecosystem are you experiencing now?

1. [ ] Self-Managed
1. [ ] Infrastructure as a Service
1. [ ] Container as a Service
1. [ ] Platform as a Service
1. [ ] Function as a Service
1. [x] Software as a Service
	> Good. This is the complete opposite end of the spectrum as the first scenario. You have nothing to do with the app, and are being granted with all of it

`;

export { rawQuizdown }