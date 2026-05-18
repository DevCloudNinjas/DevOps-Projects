# Use an official Node runtime as a parent image
FROM node:24-alpine

# Add Maintainer info
LABEL maintainer="harshhaareddy <harshhaa03@gmail.com>"

# Set the working directory to /app
WORKDIR '/app'

# Copy package.json to the working directory
COPY package.json .

# Install any needed packages specified in package.json
RUN npm install

# Copying the rest of the code to the working directory
COPY . .

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run index.js when the container launches
USER node
CMD ["node", "index.js"]
