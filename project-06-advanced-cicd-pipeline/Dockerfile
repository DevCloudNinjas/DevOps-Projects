# Use a modern, minimal, secure Alpine Java 17 image
FROM amazoncorretto:17-alpine

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy artifact and set permissions
COPY jarstaging/com/satish/demo-workshop/2.1.2/demo-workshop-2.1.2.jar sample_app.jar
RUN chown appuser:appgroup sample_app.jar

# Switch to non-root user
USER appuser

ENTRYPOINT [ "java", "-jar", "sample_app.jar" ]
