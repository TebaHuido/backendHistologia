FROM node:18-alpine

WORKDIR /usr/src/app

RUN npm install -g npm@8

COPY package*.json ./

RUN npm ci --legacy-peer-deps --verbose

COPY . .

CMD ["npx", "ng", "serve", "--host", "0.0.0.0"]

