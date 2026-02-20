# Bitbucket

Bitbucket is a web-based version control repository hosting service owned by
Atlassian, for source code management and development projects.
In this step we will install Bitbucket and configure it such that Jenkins can
use it to git clone from. We will be creating, cloning, building, and deploying
jodatime as a petclinic dependency.

Be sure to keep enough notes to create a
step-by-step guide showing your experience through this section.

![BitBucket image](img-addendum/bitbucket_light.svg ':size=400px :class=light-mode-img-center :alt= BitBucket image; light mode')
![BitBucket image](img-addendum/bitbucket_dark.svg ':size=400px :class=dark-mode-img-center :alt= BitBucket image; dark mode')

## Exercise 1

1. Create a new server and install Bitbucket

- Confirm port 7990 is open for the HTTP Port
- Confirm port 8006 is open for Control Port
- Install Bitbucket as a service

2. Browse to <http://<Public> DNS>:7990/ and follow the prompts to get a free trial. Use the internal database.
3. Setup a new jodatime repo in BitBucket using the instructions provided within Bitbucket to initialize a new repo.

- You will need to setup a user with enough permission to access and git clone the repo
- You will need to download the jodatime.tar.gz from [here](//github.com/JodaOrg/joda-time/releases).
- Uncompress jodatime and initialize it as a git repo with Bitbucket remotes.

4. Create a new Maven Jenkins job that will `git clone` from Bitbucket and `clean deploy` jodatime to Nexus.

- Use the Bitbucket Jenkins plugin

5. Configure your up and down dependencies between petclinic and jodatime.
6. Run a jodatime build and make sure it clones from Bitbucket and successfully deploys the artifact to Nexus.
7. Run a petclinic build to ensure it uses your jodatime artifact from Nexus.

### Deliverable

Have a pipeline of Bitbucket, Jenkins, and Nexus where a user can deploy an artifact from a Bitbucket project, to a Jenkins job, to a Nexus repository.

## Exercise 2

Follow these instructions to set up a webhook for the above Jenkins-Bitbucket combo.

1. Set up Bitbucket for the Webhook:
1. Open BitBucket and go to the repo that you are creating a hook for. In that repo select settings (the gear) then select Hooks under "WORKFLOW".
2. If you don't have the [Jenkins Webhook Plugin](//marketplace.atlassian.com/apps/1211284/webhook-to-jenkins-for-bitbucket?hosting=server&tab=overview) yet then install it. If it is installed already, make sure to enable it.
3. Click the plugin or the pencil icon to edit it. You should see a screen labeled "Bitbucket Server Webhook to Jenkins".
4. In this screen you need to:
    - Set up the URL for Jenkins
      - Use format <http://<Jenkins_IP>:8080/>

    - Set up URL that Jenkins has configured as the repo clone
      - Just copy and paste from your Jenkins configuration
      - For the repo clone dropdown:
        - Use SSH if you have used the external IP and it matches the exact IP of BitBucket Repo.
        - Use HTTP if you have used the external IP and it matches the exact IP of BitBucket Repo.

2. Setup Jenkins to Handle WebHooks
1. Download the [Bitbucket Plugin](//wiki.jenkins-ci.org/display/JENKINS/BitBucket+Plugin) if you haven't already.
2. Open the configuration of the job that will be using the webhook.
3. Go to Poll SCM and turn off all timing but leave on the Poll. You will get an error (see below) but ignore that, the webhook takes care of it. If polling is off then Bitbucket cannot handle webhooks in that regard.
4. Check Build when a change is pushed to Bitbucket
5. Your configuration should have the following checked under Build Triggers:
    - "Build whenever a SNAPSHOT dependency is built"
    - "Build when a change is pushed to BitBucket"
    - "Poll SCM"
6. Save the configuration and go back to Bitbucket to test it.

3. Wrapping things up
1. Verify your configuration by going back to BitBucket and go to your plugin page which says "Bitbucket Server Webhook to Jenkins".
2. Ensure that the Jenkins URL is filled out, and the Repo Clone URL uses SSH
3. Click Trigger Jenkins in the options of the webhook setup. If it successfully triggers then click _Enable_ (or _Save_) and you are done.

  ?> If you get an error then check your IPs and other settings to verify everything is correct. Specificity is a highly important with this as there are multiple IP's flying around. Remember this is a per repo activity meaning you must do this for each and every repo.

4. Finished
  You have now completed the set up for the assignment. You should now test a push from your local repo and verify it triggers in Jenkins.

### Deliverable

Be able to push from a local repo up to Bitbucket, and verify that your Jenkins job is triggered.
