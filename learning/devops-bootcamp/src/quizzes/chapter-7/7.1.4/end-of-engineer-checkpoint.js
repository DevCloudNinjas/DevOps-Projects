const rawQuizdown = `
---
shuffleAnswers: true
---
# What does the \`\`\`Read\`\`\` function of a data source do?

- [x] Refreshes the Terraform state based on the actual state of the resource in the API.
- [ ] Reads the configuration of your client and judges if it is correct.
- [ ] Queries your configured API for all resources.

# What is one difference between a schema and data model in the context of the Hashicorp tutorial?

- [x] A schema uses Terraform types and a data model uses Go types.
- [ ] A schema uses Go types and a data model uses Terraform types.
- [ ] A schema is untyped and a data model is typed.
- [ ] A schema is typed and a data model is untyped.

# What is the purpose of a Schema for a resource?

- [x] It prepares the resource to accept data from the Terraform configuration and store order information in the Terraform state.
- [ ] It establishes a connection to the external API and queries it for the structure of API resources.
- [ ] It determines the order of resource creation.

# What is the purpose of the \`\`\`Update\`\`\` function for a resource?

- [x] To update the resource based on the Terraform plan.
- [ ] To update the Terraform plan.
- [ ] To update the resource based on the Terraform state.
- [ ] To update the Terraform state.
`;

export { rawQuizdown }
