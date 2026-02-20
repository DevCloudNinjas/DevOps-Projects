const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# Assume you run the following commands in an empty directory:
\`\`\`vagrant init\`\`\`<br>\`\`\`vagrant up\`\`\`<br>\`\`\`vagrant ssh\`\`\`<br>What is the outcome?

1. [x] The vagrant up will fail because you have not specified a base box to use in the Vagrant file
  > Good, as long as the box you specify is set to the right type, these commands will work as expected
1. [ ] The vagrant up will fail because you have not constructed a configure block
  > This can be used to customize or provision your machine, but not required to make it work in the first place
1. [ ] The vagrant init will fail because the directory is empty and there are no targets to build from
  > Vagrant init doesn't actually pull from any targets, so it can safely be run by itself in an empty directory
1. [ ] The vagrant ssh will fail because you have not inserted a key to the VM's authorized_keys file
  > This shouldn't affect anything, as Vagrant handles the authentication for you when developing locally like this
1. [ ] The vagrant ssh will fail because you have not specified the box's name
  > Should you have multiple machines already spun up, this would be the case. But with only one relative machine, this command will work just fine
1. [ ] The commands will work and you will be SSHed into the VM
  > If only it were *this* seamless. Turns out there happens to be at least one simple step

# What is the distinguishment between Packer and Vagrant (ie what pieces of the puzzle do each provide)?

1. [x] Packer creates machine images that Vagrant uses as base boxes for VMs
1. [ ] Vagrant creates machine images that Packer uses as base boxes for VMs  
1. [ ] Either tool can create machine images and VMs, we just paired them because they go well together
`;

export { rawQuizdown }