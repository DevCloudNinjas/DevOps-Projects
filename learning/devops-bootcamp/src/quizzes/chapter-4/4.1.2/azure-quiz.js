const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# What is best practice for grouping resources in Azure?

1. [x] Put all resources associated with a specific app/project in the same Resource Group, regardless of their type
	> Good. Azure actually will handle cascade deleting for you in this case. If you remove the Resource Group, Azure will attempt to remove all resources inside of it first, so you don't have to
1. [ ] Group all resources by type into their own Resource Groups (ie Resource Groups only contain resources of one type)
	> Not quite. If you're confused about grouping resources, refer to this [Best Practices](https://community.ibm.com/community/user/aiops/blogs/chris-graham/2023/02/14/microsoft-azure-resource-groups-introduction-best) article by IBM
1. [ ] Put all resources associated with a specific app/project in the same Subscription regardless of their type
	> Not quite, you'd actually need to use  Resource Group for this. Look above to note the difference between a Resource Group and a Subscription. If you're confused about grouping resources, refer to this [Best Practices](https://community.ibm.com/community/user/aiops/blogs/chris-graham/2023/02/14/microsoft-azure-resource-groups-introduction-best) article by IBM
1. [ ] Group all resources by type into their own Subscriptions (ie Subscriptions only contain resources of one type)
	> Not quite, you'd actually need to use  Resource Group for this. Look above to note the difference between a Resource Group and a Subscription. If you're confused about grouping resources, refer to this [Best Practices](https://community.ibm.com/community/user/aiops/blogs/chris-graham/2023/02/14/microsoft-azure-resource-groups-introduction-best) article by IBM
1. [ ] There is no 'best practice' as Azure automatically groups resources for you
	> Actually there is a best practice when it comes to this, like with most things. Additionally, Azure won't auto group resources for you. You need to decide where they live. If you're confused about grouping resources, refer to this [Best Practices](https://community.ibm.com/community/user/aiops/blogs/chris-graham/2023/02/14/microsoft-azure-resource-groups-introduction-best) article by IBM

# True or False: You can change the name of a resource in Azure at any time without needing to alter the resource itself.

1. [ ] True
	> Not quite. Resource names in Azure are immutable by design, meaning they shouldn't/can't be changed. Refer back to the [Resource Naming and Tagging](https://bootcamp.devcloudninjas.com/#/4-cloud-computing/4.1.2-azure?id=resource-naming-and-tagging) section above
1. [x] False
	> Good. Since resource names are immutable, you would need to destroy the resource and recreate it with a different name

# What Azure CLI command will display JSON metadata about all of the VMs in your current subscription?<br>Feel free to run the commands in your terminal to test them out.

1. [x] az vm list
	> Good. From there you can apply different filters, such as only searching in specific resource groups with the \`--resource-group\` option
1. [ ] az vm ls
	> Not quite. If you recall, the AWS CLI uses \`ls\` to list some resource types, but Azure is a bit different
1. [ ] az list vm
	> Be sure to keep ordering in mind. General formula is \`az RESOURCE_TYPE COMMAND OPTIONS\`
1. [ ] az ls vm
	> Be sure to keep ordering in mind. General formula is \`az RESOURCE_TYPE COMMAND OPTIONS\`
1. [ ] az vm describe-instances
	> Not quite. If you recall, the AWS CLI leverages the \`describe-instances\` command to display certain things, but Azure does not

`;

export { rawQuizdown }