const rawQuizdown = `
---
shuffleAnswers: true
---

# What is an EC2 instance?

1. [x] A virtual machine
	> Good, an Elastic Compute Cloud (EC2) instance is just Amazon's terminology for a VM hosted in their cloud
1. [ ] A container
	> You have the right idea but you're a little off. Read these docs on [what an EC2 instance is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) if you're confused
1. [ ] A runtime instance of an app
	> Not quite. An EC2 instance can hold a runtime instance, but it isn't one, itself. Read these docs on [what an EC2 instance is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) if you're confused
1. [ ] A set of security rules
	> Not quite. An EC2 instance will need security rules, but it is something else entirely. Read these docs on [what an EC2 instance is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) if you're confused

# What is an AMI?

1. [x] A base box
	> Good. An Amazon Machine Image (AMI) is simply a base box for an EC2 instance. It stores necessary information required for starting an instance
1. [ ] An operating system
	> While an AMI is fundamental to how an instance will run, it is not the OS. Read these docs on [what an AMI is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) if you're confused
1. [ ] A container
	> Not quite. Read these docs on [what an AMI is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) if you're confused
1. [ ] A runtime instance of an app
	> Not quite. Read these docs on [what an AMI is](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) if you're confused

# How does an EC2 instance obtain its default username/password?

1. [x] They are attached to the AMI and listed in the marketplace
	> Good. Most of the time, you'll find your login info when selecting the AMI in the marketplace
1. [ ] They are provided by the user when creating the instance
	> Not quite. Think back to how you found your login info during the exercise
1. [ ] They are loaded into the instance by an install script
	> Not quite. Think back to how you found your login info during the exercise
1. [ ] They are created on the AWS console
	> Not quite. Think back to how you found your login info during the exercise

# How does an EC2 instance manage web traffic to/from itself?

1. [x] Security Group
	> Good. When configuring your Security Group, you must define a set of inbound and outbound rules. This is what dictates the security restrictions for your instance
1. [ ] Predefined rules in the AMI
	> Not quite. Think back to where/how you defined the access priviledges for your instance during the exercise
1. [ ] Load Balancer
	> Not quite. A Load Balancer deals with auto-scaling your instance, and you'll learn more about it later. Think back to where/how you defined the access priviledges for your instance during the exercise
1. [ ] Traffic Management Service
	> Not quite. Traffic Management Service is not a real thing in AWS, but there is something you used in this section that essentially does just that. Think back to where/how you defined the access priviledges for your instance during the exercise

# Fill in the blanks: The Jenkins _____ schedules jobs and monitors progress, and the Jenkins _____s actually execute the jobs

1. [x] Controller, Agent
	> Good. The controller is the original node that delegates work to one or multiple agents
1. [ ] Agent, Controller
	> Almost there! Refer back to the [Jenkins Architecture](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.2.2-ec2?id=jenkins) above
1. [ ] Pipeline, Agent
	> Not quite. The Jenkins Pipeline refers to the entire process as a whole. Refer back to the [Jenkins Architecture](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.2.2-ec2?id=jenkins) above
1. [ ] Pipeline, Controller
	> Not quite. The Jenkins Pipeline refers to the entire process as a whole. Refer back to the [Jenkins Architecture](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.2.2-ec2?id=jenkins) above

# True or False: You can have agents working together and running in unison across different environments in one Jenkins pipeline

1. [x] True
	> Good. Jenkins, like other CI/CD tools such as GitHub Actions, allows for synchronization with several different tools and environments.
1. [ ] False
	> Actually, you can. Jenkins, like other CI/CD tools such as GitHub Actions, allows for synchronization with several different tools and environments.

`;

export { rawQuizdown }