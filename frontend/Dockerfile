FROM node:16.5-alpine3.11 as build-stage
WORKDIR /app
COPY ./package.json ./yarn.lock ./babel.config.js ./
COPY ./src ./src
COPY ./public ./public
RUN yarn install
RUN yarn build

FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/conf.d/default.conf
