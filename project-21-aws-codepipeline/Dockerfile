FROM node:16.17.0-alpine as builder
WORKDIR /app
COPY ./package.json .
COPY ./yarn.lock .
RUN yarn install
COPY . .
ARG TMDB_V3_API_KEY
ENV VITE_APP_TMDB_V3_API_KEY=${TMDB_V3_API_KEY}
ENV VITE_APP_API_ENDPOINT_URL="https://api.themoviedb.org/3"
RUN yarn build

FROM nginxinc/nginx-unprivileged:alpine
WORKDIR /usr/share/nginx/html
USER root
RUN rm -rf ./*
COPY --from=builder /app/dist .
USER nginx
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]