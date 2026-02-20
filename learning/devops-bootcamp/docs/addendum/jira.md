# Jira

At this point you should already have experience using Jira. Jira is available as a cloud service and a self managed server. In this section you will gain experience with the self managed server version of Jira by installing, managing and integrating it with other tools.

![jira image](img-addendum/jira_light.svg ':size=400px :class=light-mode-img-center :alt= jira image; light mode')
![jira image](img-addendum/jira_dark.svg ':size=400px :class=dark-mode-img-center :alt= jira image; dark mode')

## Install Jira

1. Create a new local virtual host or container and open port 8080.
2. Download [Jira Server](https://www.atlassian.com/software/jira/download) and copy the installer to your host.

> Note: you may need to check with the requirements of the Jenkins Integration plugin used in the last exercise and install a compatible version of Jira server.

3. Execute the Jira installer and follow the [instructions](https://confluence.atlassian.com/display/ALLDOC/Latest+JIRA+installation+documentation).
4. Open the Jira web interface [http://localhost:8080](http://localhost:8080) and choose "Set it up for me".

![jira image 1](img-addendum/jira1.webp ':class=img-shadow-center :alt= jira image 1')

5. Configure the evaluation license. This might be cached if you have recently configured a trial Bitbucket.

![jira image 2](img-addendum/jira2.webp ':class=img-shadow-center :alt= jira image 2')

6. Create an administrator account and wait for setup to complete.

![jira image 3](img-addendum/jira3.webp ':class=img-shadow-center :alt= jira image 3')

7. Once the server setup is complete create a new *Kanban software development* project.

![jira image 4](img-addendum/jira4.webp ':class=img-shadow-center :alt= jira image 4')

8. Create an issue in your Kanban project.

![jira image 5](img-addendum/jira5.webp ':class=img-shadow-center :alt= jira image 5')

## Connect Jira to your BitBucket server

1. Follow the steps [here](https://confluence.atlassian.com/bitbucketserver/linking-bitbucket-server-with-jira-776640408.html) to integrate Jira with the BitBucket server you setup earlier.
2. Using a repo in the BitBucket server create a branch, commit and pull request which automatically link back to an issue in your Jira server.

## Connect Jira to your Jenkins server

1. Install [Jenkins Integration for Jira](https://marketplace.atlassian.com/plugins/com.marvelution.jira.plugins.jenkins/server/overview) plugin.
2. Configure the plugin to connect to your Jenkins server.
3. Trigger a build job in Jenkins which is linked to a Jira issue. Confirm that the build results are displayed in the Jira issue and link back to the Jenkins build.

# Deliverables

- Discuss the advantages and disadvantages of using a self managed installation of Jira versus the cloud hosted service.
- Discuss some possible use cases for linking Jira issues with changes made in source control management.
- Discuss the advantages of linking issues in Jira with builds in Jenkins.
- Discuss how Jira connects an issue to a commit, branch or pull request in BitBucket and connects that issue to a build in Jenkins.
