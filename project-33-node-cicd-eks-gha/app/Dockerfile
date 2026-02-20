FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

COPY . .
RUN npm install
EXPOSE 3000
CMD [ "node", "index.js" ]