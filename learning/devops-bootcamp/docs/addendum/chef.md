---
docs/6-infrastructure-configuration-management/6.3-chef.md:
  category: Infrastructure as Code
  estReadingMinutes: 15
  exercises:
    -
      name: Installing Chef Workstation and Creating a Wrapper Cookbook
      description: Install Chef Workstation and create a Wrapper Cookbook for Nginx, including recipe development, local testing with Vagrant, and ensuring code quality.
      estMinutes: 240
      technologies:
      - Chef
      - Chef Workstation
      - Vagrant
    -
      name: Setting Up Chef Server and Bootstrapping AWS Instances
      description: Install Chef Server on an AWS instance, upload the Nginx cookbook to the server, and bootstrap a new AWS instance with the Nginx cookbook.
      estMinutes: 480
      technologies:
      - Chef
      - Chef Server
      - AWS
      - Nginx
---

# Chef

## Overview

This lab is designed to give you a base understanding of Chef and how it works. This tool is one of the most popular configuration managers and is used by many engineering teams to create better experiences for their customers and teams. DevCloud Ninjas has some Chef Repos that you can see at [GitHub/devcloudninjas-chef.](https://github.com/devcloudninjas-chef)

### Chef Basics

Read about Chef and determine the following questions:

- What type of architecture does chef use? Agentless, Master-Agent, etc.
- What is a cookbook?
- What is a wrapper cookbook?
- What is a Chef repo?
- What is a recipe?
- What is an attribute?
- What is metadata?
- What is Berkshelf?
- What is a data bag?
- What is Chef Workstation?
- What is ChefSpec?
- What is test kitchen?
- What is Cookstyle?
- What is the Supermarket?
- What is Chef Solo?
- How do you use Vagrant for local Dev?

You can get most of this information on:

- [Chef.io](https://www.chef.io/)
- [Learn.chef.io](https://learn.chef.io/)
- [Vagrant Chef Solo Provisioner](https://www.vagrantup.com/docs/provisioning/chef_solo.html)
- [About Cookbooks](https://docs.chef.io/cookbooks.html)

> ### Discuss your findings with your peers

## Exercise 1

1. Install Chef Workstation on your system if it is not currently.
2. Create Wrapper Cookbook of Nginx.
   - Use Vagrant for local development.
   - Include a recipe in the default.rb that adds a file to the home directory called name.txt with your name inside.
   - No Ruby Errors
   - No Cookstyle Errors
   - There must be ChefSpec for it

## Exercise 2

1. Create a static Hello, world html page. (if there's time).
2. Install Chef Server on AWS instance.
3. Upload Nginx cookbook to chef server
4. Bootstrap a new AWS instance with Nginx cookbook.

> ### Note:
>
> - The server and workstation instances might be too much for a t2.micro or t2.small. A t2.medium is recommended.
> - Vague steps on purpose - ask leader for clarification if need be
> - There are more than one way to get to the same outcome - be prepared to talk about your method.
> - We will discuss at every section so be sure to keep each other on pace.

<center>

## Deliverables

</center>

<div class="grid2"><div class="col">
<center>

**Engineers**

</center>

- What was the hardest part of this?
- How may local testing help?
- What do you think of Chef?

</div><div class="col">
<center>

**Consultants**

</center>

- What is this tool?
- How is it used in an enterprise?
- Licensing costs
- DevCloud Ninjas' POV/uses for Chef
- Explain pros and cons
- Create high level deck explaining Chef. Coordinate with your team to also have a technical demo
- Once an engineer has completed this exercise work with them to run through steps 4-6

</div></div>
