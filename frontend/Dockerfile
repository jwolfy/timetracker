FROM node:16.5-alpine3.11 as build-stage
WORKDIR /app
COPY . .
RUN yarn install && yarn build --silent

FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
RUN rm -rf /etc/nginx/conf.d
RUN rm -rf /etc/nginx/nginx.conf.default
COPY nginx.conf /etc/nginx/nginx.conf
