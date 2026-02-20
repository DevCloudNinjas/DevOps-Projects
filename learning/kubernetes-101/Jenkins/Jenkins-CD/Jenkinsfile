  def label = "deploy"
  podTemplate(label: label, yaml: """
  apiVersion: v1
  kind: Pod
  metadata:
    labels:
      name: deploy
  spec:
    serviceAccount: jenkins-agent-sa
    containers:
    - name: deploy
      image: dpthub/eddeployagent
      command:
      - cat
      tty: true
  """
  ) {
      node (label) {

          stage ('Checkout SCM'){
            git url: 'https://dptrealtime@bitbucket.org/dptrealtime/loginapp-cicd-deployment.git', branch: 'dev'
          }

          stage ('Helm Chart') {
            container('deploy') {
              dir('charts') {
                withCredentials([usernamePassword(credentialsId: 'jfrog', usernameVariable: 'username', passwordVariable: 'password')]) {
                      sh '/usr/local/bin/helm repo add dptweb-helm-local  https://edwikifacts.jfrog.io/artifactory/dptweb-helm-local --username $username --password $password'
                      sh "/usr/local/bin/helm repo update"
                      sh "/usr/local/bin/helm install dptweb-dev --namespace dev -f values.yaml ."
                      sh "/usr/local/bin/helm list -a --namespace dev"
                }
              }
          }
          }
      }
  }