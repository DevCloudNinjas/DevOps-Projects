
docker build -f Dockerfile -t django_fintech_enterprise_container .
docker run -it -p 80:80 django_fintech_enterprise_container