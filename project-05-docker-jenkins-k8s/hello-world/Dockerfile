# Use a specific, modern version instead of 'latest' for reproducible builds
FROM tomcat:10.1-jdk17-temurin

# Create a non-root user to run Tomcat
RUN groupadd -r tomcat && useradd -r -g tomcat tomcat

# Set working directory to the webapps folder
WORKDIR /usr/local/tomcat/webapps

# Clean default webapps to reduce attack surface and copy new artifact
RUN rm -rf /usr/local/tomcat/webapps/*
COPY ./*.war /usr/local/tomcat/webapps/

# Fix ownership and permissions for the Tomcat non-root user
RUN chown -R tomcat:tomcat /usr/local/tomcat

# Switch to the non-root user
USER tomcat

# Expose default Tomcat port
EXPOSE 8080

CMD ["catalina.sh", "run"]
