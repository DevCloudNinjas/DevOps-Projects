## Data BackUp of CI/CD Stack

### Jenkins BackUp

Create an S3 bucket with a unique name.
```sh
Name: vprofile-cicd-stack-backup-rd
```

Create an IAM role for EC2  with policy `AmazonS3FullAccess` name as `vprofile-cicd-s3fullaccess`. We will attach this role to Jenkins, Nexus and Sonar server.

Login to Jenkins server.
```sh
sudo -i
systemctl stop jenkins
cd /var/lib
du -sh jenkins
cd jenkins
cd .m2/repository
rm -rf *
cd ../..
cd workspace
rm -rf *
cd ..
cd jobs
cd <Job_name>/builds
rm -rf <delete all directories with number> : rm -rf 1 2 3 4 5 
cd ../..
du -sh *  find the directory which takes most space delete build #s
cd .sonar/cache
rm -rf *
cd ..  # go back to /var/lib
tar -czvf jenkins_cicdjobs.tar.gz jenkins
aws s3 cp jenkins_cicdjobs.tar.gz s3://vprofile-cicd-stack-backup-rd
aws s3 ls vprofile-cicd-stack-backup-rd
```

### Nexus BackUp

```sh
sudo -i
systemctl stop nexus
cd /opt
tar -czvf nexus-cicd-vpro-pr.tgz nexus
aws s3 cp nexus-cicd-vpro-pr.tgz s3://vprofile-cicd-stack-backup-rd
aws s3 ls vprofile-cicd-stack-backup-rd
```

### SonarQube BackUp

We need to backup sonarqube directory and postgresql here.

```sh
sudo -i
systemctl stop sonarqube
cd /opt
tar -czvf sonarqube-vpro-pro-data.tgz sonarqube
aws s3 cp sonarqube-vpro-pro-data.tgz s3://vprofile-cicd-stack-backup-rd
aws s3 ls vprofile-cicd-stack-backup-rd
```

### App Server BackUp

```sh
sudo -i
cd /usr/local/tomcat8/
ls
cd conf/
ls
aws s3 tomcat-users.xml s3://vprofile-cicd-stack-backup-rd
cd ..
cd webapps/manager/META-INF/
aws s3 cp contect.xml s3://vprofile-cicd-stack-backup-rd
```