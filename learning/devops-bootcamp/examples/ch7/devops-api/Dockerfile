from ubuntu:latest

run apt-get -y update && apt-get -y install golang git

run mkdir devops-api
workdir devops-api

copy . .

run go build

expose 8080

entrypoint [ "./devops-api" ]
