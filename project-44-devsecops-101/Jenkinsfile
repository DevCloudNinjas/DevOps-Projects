pipeline {
    agent any
    tools { 
        maven 'maven-3.8.6' 
    }
    stages {
        stage('Checkout git') {
            steps {
               git branch: 'main', url: 'https://github.com/praveensirvi1212/DevSecOps-project'
            }
        }
        
        stage ('Build & JUnit Test') {
            steps {
                sh 'mvn install' 
            }
            post {
               success {
                    junit 'target/surefire-reports/**/*.xml'
                }   
            }
        }
        stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('SonarQube-server') {
                        sh 'mvn clean verify sonar:sonar \
                        -Dsonar.projectKey=devsecops-project-key \
                        -Dsonar.host.url=$sonarurl \
                        -Dsonar.login=$sonarlogin'
                }
            }
        }
        stage("Quality Gate") {
            steps {
              timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true
              }
            }
        }
        
        stage('Docker  Build') {
            steps {
      	        sh 'docker build -t praveensirvi/sprint-boot-app:v1.$BUILD_ID .'
                sh 'docker image tag praveensirvi/sprint-boot-app:v1.$BUILD_ID praveensirvi/sprint-boot-app:latest'
            }
        }
        stage('Image Scan') {
            steps {
      	        sh ' trivy image --format template --template "@/usr/local/share/trivy/templates/html.tpl" -o report.html praveensirvi/sprint-boot-app:latest '
            }
        }
        stage('Upload Scan report to AWS S3') {
              steps {
                  sh 'aws s3 cp report.html s3://devsecops-project/'
              }
         }
        stage('Docker  Push') {
            steps {
                withVault(configuration: [skipSslVerification: true, timeout: 60, vaultCredentialId: 'vault-cred', vaultUrl: 'http://your-vault-server-ip:8200'], vaultSecrets: [[path: 'secrets/creds/docker', secretValues: [[vaultKey: 'username'], [vaultKey: 'password']]]]) {
                    sh "docker login -u ${username} -p ${password} "
                    sh 'docker push praveensirvi/sprint-boot-app:v1.$BUILD_ID'
                    sh 'docker push praveensirvi/sprint-boot-app:latest'
                    sh 'docker rmi praveensirvi/sprint-boot-app:v1.$BUILD_ID praveensirvi/sprint-boot-app:latest'
                }
            }
        }
        stage('Deploy to k8s') {
            steps {
                script{
                    kubernetesDeploy configs: 'spring-boot-deployment.yaml', kubeconfigId: 'kubernetes'
                }
            }
        }
        
 
    }
    post{
        always{
            sendSlackNotifcation()
            }
        }
}

def sendSlackNotifcation()
{
    if ( currentBuild.currentResult == "SUCCESS" ) {
        buildSummary = "Job_name: ${env.JOB_NAME}\n Build_id: ${env.BUILD_ID} \n Status: *SUCCESS*\n Build_url: ${BUILD_URL}\n Job_url: ${JOB_URL} \n"
        slackSend( channel: "#devops", token: 'slack-token', color: 'good', message: "${buildSummary}")
    }
    else {
        buildSummary = "Job_name: ${env.JOB_NAME}\n Build_id: ${env.BUILD_ID} \n Status: *FAILURE*\n Build_url: ${BUILD_URL}\n Job_url: ${JOB_URL}\n  \n "
        slackSend( channel: "#devops", token: 'slack-token', color : "danger", message: "${buildSummary}")
    }
}

    
