sudo passwd postgres
su - postgres
createuser sonar
psql
ALTER USER sonar WITH ENCRYPTED password 'postgres';
CREATE DATABASE sonarqube OWNER sonar;
GRANT ALL PRIVILEGES ON DATABASE sonarqube to sonar;
\q
exit