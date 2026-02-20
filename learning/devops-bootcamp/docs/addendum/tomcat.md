# Tomcat

In this section you will learn how to configure Tomcat. Tomcat is an open-source Java Servlet container developed by Apache, that provides a Java HTTP web server environment to run and test java code.
You can find out more about Tomcat from the [official website](https://tomcat.apache.org/) and [Wikipedia page](https://en.wikipedia.org/wiki/Apache_Tomcat).

![tomcat image](img-addendum/tomcat.svg ':size=300x200 :class=icon :alt= tomcat image')

## Setup Tomcat

1. Setup a new server using on your golden image.
2. Check that your software is up-to-date, and update anything that's needed.
3. Install and configure Tomcat to run on your server.

### Before moving on

Before continuing, make sure you have two separate servers, one running Jenkins, and one running Tomcat.

## Deploying from Jenkins to Tomcat

1. Setup an SSH key to allow Jenkins to connect to Tomcat.
2. Configure a Jenkins job which builds [spring-petclinic](https://github.com/devcloudninjas/spring-petclinic).
3. Configure a second job that deploys the build artifacts to Tomcat with SCP using either:

- A shell script
- A Jenkins plugin

4. Set up your jobs so that when the build job is complete, the deploy job is triggered automatically.
5. Visit your Tomcat server and confirm the project deployed correctly. You should be able to see the webapp in your browser.

## Applying the Maven Way

In Chapter 4 we discussed the benefits of convention over configuration. When
building new jobs it is common to venture away from the Maven Way in
order to experiment with how it can be built. Once you determine the correct
process, it is best to codify that process into plugins, allowing you to save
configuration in version control and increase modularity. In the previous
exercise we explored deploying our artifact using SCP, however there is another
way.

1. Read about the [Tomcat Maven Plugin](http://tomcat.apache.org/maven-plugin-2.0/tomcat7-maven-plugin/)
2. Edit your Maven settings to provide authentication for Tomcat.
3. Edit your POM to deploy to Tomcat using the given credentials.
4. Reconfigure your Jenkins job to ensure the plugin runs.

Discuss the differences between both approaches.

# Deliverable

A simple pipeline setup with Jenkins capable of delivering an artifact to Tomcat, where you can view the application.
Discuss the benefits of using a tool like Tomcat in software development.
