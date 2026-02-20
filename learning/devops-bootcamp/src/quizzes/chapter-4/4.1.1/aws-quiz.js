const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# True or False: AWS does not offer a specific naming tool for its resources. A name is simply a generic tag with the label "Name" and a key of whatever you want the name to be.

1. [x] True
	> Good. While naming seems like a feature that should be standalone and separate from tags, this A) allows for quick searching of resources and B) allows for a standardized naming method across all resources, regardless of their type
1. [ ] False
	> Not quite. Reread the [Names](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.1.1-aws?id=names) section above

# From the following list, select all *quality* resource tags<br>If you are confused, refer to [DevCloudNinjas' tagging standards](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.1.1-aws?id=devcloudninjas39s-tagging-standards) above.

- [x] **Owner**=chris-blackburn
- [x] **Project**=pipeline-initiative
- [x] **Client**=boeing
- [ ] **Application**=test
	> Application names should be descriptive
- [ ] **Automation Candidate**=auto-deploy
	> The **Automation Candidate** should be set to "yes" or "no"
- [ ] **Owner**=patrick
	> It's a big company, lot's of Patricks. Try to stick to Slack handles or firstname-lastname
- [ ] **Environment**=aws
	> The resource is already on AWS, listing aws in the tag is pointless

# What happens if you run the following command?<br>\`aws-vault exec PROFILE_NAME -- aws ec2 describe-instances\`

1. [x] You are placed into a large JSON object file full of metadata about the organization's EC2 instances
	> Good. This output can be piped to a file for handling in automated workflows, and can be modified to filter the list to your specifications
1. [ ] A list of all of the names of the organization's EC2 instances prints. You can further inspect any of them
	> To limit the fields returned to just names, IDs or other labels, you'd have to leverage the \`--query\` flag on **describe-instances**. This expects a [JMESpath](https://jmespath.org/) to the fields you want returned
1. [ ] The command fails as it is improper
	> The command is in fact proper
1. [ ] The terminal further prompts you for the name of a specific EC2 instance to describe
	> Not quite. Other than entering credentials, the AWS CLI shouldn't prompt you. This makes it very convenient for using in automated workflows
`;

export { rawQuizdown }
