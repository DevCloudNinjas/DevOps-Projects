# Start Here: project-18-jenkins-java-full-cicd

**Learning focus:** Beginner Java/Spring Boot CI/CD and DevSecOps pipeline concepts

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `mvn -q -f spring-boot-app/pom.xml test` to establish the local Maven test baseline before touching Docker, Jenkins, SonarQube, Helm, Argo CD, or Kubernetes.

## Checkpoints

1. 1. The Maven command completes and produces a passing local test result for `spring-boot-app`
2. 2. `mvn clean package` creates the Spring Boot artifact under `spring-boot-app/target`, which the learner can identify without deploying it
3. 3. The learner can run the packaged application locally and observe the web page at `http://localhost:8080`, then relate the JenkinsFile stages and Kubernetes manifests to checkout, build, scan, package, and deployment concepts without executing a live deployment.

## Hints if you are stuck

1. 1. If Maven fails immediately, compare the installed Java/Maven versions with the Spring Boot project's `pom.xml` expectations and read the first error rather than the final summary
2. 2. If the packaged application is not found, verify that the command was run from the project root and that the artifact was created in `spring-boot-app/target`
3. 3. If the local page is unreachable, check whether the Java process is still running and whether the URL and port match the README's local command, without changing the Kubernetes or Jenkins files.

## Evidence to capture

Terminal capture of passing Maven tests, the generated JAR in `spring-boot-app/target`, and a local browser view of the Spring Boot page, plus a short stage-to-file mapping for `JenkinsFile`, `Dockerfile`, and the Kubernetes manifests.

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
