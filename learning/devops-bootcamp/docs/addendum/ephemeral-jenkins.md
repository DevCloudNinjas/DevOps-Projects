# Ephemeral Jenkins

Jenkins is a self-contained, open source automation server which can be used to automate all sorts of tasks related to building, testing, and delivering or deploying software. Jenkins can be thought of as an orchestrator of tools, controlling the when and how of running tools.

In previous sections, you have likely been using a more persistent Jenkins container. This requires a number of manual steps to configure Jenkins, install plugins and tools, and setup jobs. In this section you will be creating an ephemeral (i.e. no persistence) Jenkins instance using the [Jenkins Configuration as Code plugin](https://github.com/jenkinsci/configuration-as-code-plugin) and the [job-dsl plugin](https://jenkinsci.github.io/job-dsl-plugin/).

![jenkins image](img-addendum/jenkins_light.svg ':size=400px :class=light-mode-img-center :alt= jenkins image; light mode')
![jenkins image](img-addendum/jenkins_dark.svg ':size=400px :class=dark-mode-img-center :alt= jenkins image; dark mode')

## Exercise

1. Setup a fresh Jenkins server with the recommended plugins.

* ensure you have jdk and Maven installed in your container

 ?> Using the [official Jenkins image](https://hub.docker.com/r/jenkins/jenkins) will allow you to install plugins as part of the Docker build process.
2. Create a `.yaml` file for the [JCasC plugin](https://github.com/jenkinsci/configuration-as-code-plugin) that configures a basic Jenkins instance and the recommended plugins installed in the previous step.

* create a user with admin permissions
* make sure your instance has at least the git plugin, job-dsl plugin, and pipeline plugins installed
* check any warnings about permissions

3. Using the [job-dsl plugin](https://jenkinsci.github.io/job-dsl-plugin/), add a Pipeline job to your existing `.yaml` file to build spring-petclinic. You don't need to deploy this artifact.
4. Make sure spring-petclinic builds successfully.
5. Stop and remove your container.
6. Run your image and make sure that a fresh Jenkins instance is created and configured as you expect.

# Deliverable

* Compare and contrast ephemeral Jenkins and non-ephemeral Jenkins.
* Discuss the average windspeed velocity of a swallow.
* Discuss any challenges you may have had setting this up.
