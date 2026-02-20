FROM openjdk:8u131-jdk-alpine

MAINTAINER PR Reddy "trainings@edwiki.in"

EXPOSE 8080

WORKDIR /usr/local/bin/

COPY target/sts-0.0.1-SNAPSHOT.jar webapp.jar

CMD ["java", "-jar","webapp.jar"]