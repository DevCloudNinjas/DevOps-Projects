# Nexus

A software artifact is the product produced by software development, often used to mean compiled executables or packaged code. Just like how source code is generally stored in repositories and version controlled, artifacts are also stored in repositories where their versions are tracked.

Nexus is one such repository manager which stores artifacts. Previously in the Bootcamp, we've used it with Maven as the ultimate destination of our deployments. However, if you're storing artifacts, it's obvious you might also like to use them later. In this section we'll use Nexus as an intermediate step, with the artifacts stored they're being used later in our pipeline.

![repo image](img-addendum/repository_light.svg ':size=150x150 :class=light-mode-icon :alt= repo image; light mode')
![repo image](img-addendum/repository_dark.svg ':size=150x150 :class=dark-mode-icon :alt= repo image; dark mode')

# Setup Nexus

1. Install Nexus on a new server.
2. Configure a Jenkins [spring-petclinic](learning/devops-bootcamp) job to deploy SNAPSHOT artifacts to your Nexus.

Confirm that your artifact was deployed.

# Retrieving Artifacts from Nexus

1. Install the [Publish Over SSH](https://wiki.jenkins.io/display/JENKINS/Publish+Over+SSH+Plugin) Jenkins plugin.
2. Setup an SSH key pair between your Tomcat server and Jenkins.
3. Create a new Jenkins job that will connect to your Tomcat server, then download a .war file from Nexus.
4. Nexus stores metadata for builds separate from the artifacts themselves. Use this metadata and add a script to your deploy job so that it downloads the newest petclinic artifact from Nexus.

### Deliverable

  Have a Jenkins job deploy an artifact to Nexus, then deploy the artifact from Nexus to Tomcat.
