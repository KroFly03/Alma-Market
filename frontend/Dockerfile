FROM node:16.15.0-alpine as build

WORKDIR /app

EXPOSE 350

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build
