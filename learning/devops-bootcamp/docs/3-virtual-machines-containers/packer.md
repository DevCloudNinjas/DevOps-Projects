# Packer

[Packer](https://www.packer.io/intro/index.html) allows you to easily create
provisioned and configured machines in seconds. With Packer, teams will be less likely to run into the issue of a solution only working on one machine. Images can be created from
multiple platforms with all of the software configured at the time the image is
built. Packer defines configuration in a JSON file which can be added to
version control and increases scalability. It is worth noting Packer is lightweight and is capable of running on every major operating system today and it is very popular to use additional tools such as Chef and Ansible to further install software on the machine image.

![packager image](img3/packer.svg ':size=350x350 :class=icon :alt= packer image')

## Use cases

- Continuous Delivery
  - Lightweight, portable, and command-line driven.
  - New images can be launched and tested, verifying that the infrastructure changes work.
- Dev/Prod Parity
  - Keeps development, staging, and production as similar as possible.
  - Can be used to generate images from multiple platforms.
- Appliance/Demo Creation
  - Automatically create appliances with software preinstalled.

## Additional Resources on Packer

[Why Use Packer?](https://www.packer.io/intro/why.html)

[Packer Docs](https://www.packer.io/docs/)

[Packer Example](https://medium.com/devopslinks/build-your-own-ec2-machine-images-with-packer-ansible-on-aws-for-immutable-aws-deployments-f7dbe81934a1)

## Exercise

### Creating a VirtualBox Image

1. Read [Getting Started](https://www.packer.io/intro/getting-started/install.html)
to learn more about Packer and install it on your machine.
2. Using Packer, create a minimal CentOS VirtualBox image.
3. Edit your JSON file so that Jenkins is installed and accessible on the image when it is first booted up.
4. Edit your JSON file so your image is packaged into a Vagrant box after building.

### Parallel Builds with Packer

1. Using the same JSON as before, create a CentOS Docker image.
2. Using Packer’s provisioners, install Nexus on your new image.

You should be able to accomplish all of these tasks with a single JSON file.

## Tips

- Consider looking into Kickstart files to help install CentOS.
- Packer connects to your virtual machine over ssh, make sure you’ve created a user/password for it to use.
- Docker images built with Packer aren’t given a name by default, but you can use a post-processing step to add a tag to your image.

<center>

## Deliverable

</center>

<div class="grid2"><div class="col">
<center>

**Engineers**

</center>

- A single .JSON that can accomplish all of the tasks above.
Next Discuss:
- What was the hardest part of this exercise?
- What are some key differences between Packer and Vagrant?
- What purpose do each of the major sections of Packer's json file serve. (Builders, Provisioners, Post-Processors)

</div><div class="col">
<center>

**Consultants**

</center>

- Understand what the engineers are accomplishing with Packer
- Create a presentation about Packer, containerization, and how they are used at the enterprise
- Work with the engineers to have them perform a technical demo during your presentation
- Present your experience with Chapter 3 to the team

</div></div>
