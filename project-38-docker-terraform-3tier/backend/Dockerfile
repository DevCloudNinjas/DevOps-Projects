FROM node:10-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 3001
CMD [ "node", "index.js" ]
