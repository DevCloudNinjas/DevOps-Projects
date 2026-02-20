const rawQuizdown = `
---
shuffleAnswers: true
---

# Given the above .ssh/config file, select all commands that will successfully ssh to the host. You can assume the public key file has already been sent to the host.

- [x] ssh my_host
- [x] ssh \`ec2-user@ec2-42-42-42-42.us-west-2.compute.amazonaws.com\` -i ~/.ssh/host_public_key.pub
- [ ] ssh \`ec2-user@ec2-42-42-42-42.us-west-2.compute.amazonaws.com\`
	> In this ssh command, no private key is specified, so you'll have no way of authenticating
- [ ] ssh ec2-user@my_host

# What are the main reasons for ssh key exchanges? Select all that apply:

- [x] They provide a way for automated actions to login successfully without having to enter a password
- [x] They eliminate the TOIL that comes with entering passwords repeatedly
- [x] They eliminate the need for a password, while also being more secure
- [ ] They eliminate the need for a password, but are less secure than using a password
	> Using key exhanges are *more* secure than passwords, because they are longer, more complex, and encrypted
- [ ] They allow multiple users to share the same authentication credentials, which enhances security
	> This is actually harmful for security. If one user's information leaks, it compromises others aswell

# Why are the permission levels \`0700\` for the \`.ssh/\` directory and \`0600\` for the \`.ssh/authorized_keys\` file recommended as secure settings for SSH authentication? Select the most accurate explanation.
You may choose to explore more about permissions [here](https://mason.gmu.edu/~montecin/UNIXpermiss.htm)

1. [x] To allow only the file owner to read and write .ssh/authorized_keys and to access the .ssh/ directory, preventing unauthorized users from viewing or modifying private SSH keys
1. [ ] To ensure that .ssh/ and .ssh/authorized_keys are readable, writable, and executable by everyone, guaranteeing maximum compatibility across different users and systems
1. [ ] To enable group and other users to access SSH keys for administrative and troubleshooting purposes, while restricting write permission to the owner only
1. [ ] To restrict all access to .ssh/ and .ssh/authorized_keys for security purposes, making these files and directories completely inaccessible

# What does the \`0700\` permission denote for the \`.ssh\` directory?<br>
You may choose to explore more about permissions [here](https://mason.gmu.edu/~montecin/UNIXpermiss.htm)

1. [x] Owner has Read, Write, and Execute permissions
1. [ ] Group has Read, Write, and Execute permissions
1. [ ] Owner has Read and Execute permissions
1. [ ] Group has Read and Execute permissions
1. [ ] Group has Read and Write permissions
1. [ ] Owner has Read and Write permissions

# What does the \`0600\` permission denote for the \`.ssh/config\` file?
You may choose to explore more about permissions [here](https://mason.gmu.edu/~montecin/UNIXpermiss.htm)

1. [x] Owner has Read and Write permissions
1. [ ] Owner has Read, Write, and Execute permissions
1. [ ] Group has Read, Write, and Execute permissions
1. [ ] Owner has Read and Execute permissions
1. [ ] Group has Read and Execute permissions
1. [ ] Group has Read and Write permissions
`;

export { rawQuizdown }