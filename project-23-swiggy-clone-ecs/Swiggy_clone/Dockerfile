# Stage 1: Build the React application
FROM node:16-alpine as builder
WORKDIR /app
COPY package*.json ./
# Using npm ci for reliable builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve the static files with a non-root Nginx server
FROM nginxinc/nginx-unprivileged:alpine
WORKDIR /usr/share/nginx/html
# Switch to root to clear the default html files, then drop privileges back
USER root
RUN rm -rf ./*
COPY --from=builder /app/build .
USER nginx

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
