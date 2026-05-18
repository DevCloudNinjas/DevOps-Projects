FROM node:24-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 3001
USER node
CMD [ "node", "index.js" ]
