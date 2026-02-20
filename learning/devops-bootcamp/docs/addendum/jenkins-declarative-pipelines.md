---
docs/6-release-management/6.2-declarative-pipelines.md:
  category: CI/CD
  estReadingMinutes: 10
  exercises:
    -
      name: Jenkins Declarative Pipeline
      description: Use a Jenkins file on the previously built Jenkins, Artifactory pipeline such that Jenkins builds and tests every branch and deploys only from the main branch to artifactory.
      estMinutes: 180
      technologies:
      - Jenkins
      - Docker
      - Docker Compose
      - Kubernetes
      - Artifactory
---


# Declarative Pipelines

A Declarative Pipeline is a method for automating the process of setting up a pipeline in Jenkins. To do this we will be using a Jenkinsfile. Jenkinsfiles contain the definition of a Jenkins Pipeline in steps and is checked into source control to be used by Jenkins.

### Example Jenkinsfile

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
```

``` agent any ```

- Execute this Pipeline or any of its stages, on any available agent

``` stages ```

- Lists the stages that will be executed in this pipeline, for this example there are 3:
  - Build
  - Test
  - Deploy

``` stage('Build') ```

- Defines a stage 'Build'.

``` steps ```

- Performs some steps related to the 'Build' stage.

``` stage('Test') ```

- Defines a stage 'Test'.

``` steps ```

- Performs some steps related to the 'Test' stage.

``` stage('Deploy') ```

- Defines a stage 'Deploy'.

``` steps ```

- Performs some steps related to the 'Deploy' stage.

?> Stage names can be anything, and there can be any number of stages. For further details on Jenkins pipelines, consult the [official documentation](https://jenkins.io/doc/book/pipeline/).

## Exercise

1. Using your Jenkins and Artifactory instances from the previous section, implement a Jenkinsfile to automate your pipeline.
    - For the three projects spring-petclinic, joda-time hibernate, and junit your projects should build, test, and deploy each to Artifactory.
    - When deploying to Artifactory, do not use plugins and instead use shell commands and the [Artifactory API](https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API).
2. Setup each Pipeline to build and test every branch, but only deploy from the main branch.

## Multi-Branch Pipeline

There is a Multi-Branch Pipeline job type in Jenkins that is very similar to the singular Pipeline job, but rather than only monitoring one branch it will monitor all branches. It will also allow you to test everytime you push onto a branch. However, it won't automatically only deploy from the main branch.

# Deliverable

Describe why a declarative pipeline is used with Jenkins and Artifactory.
