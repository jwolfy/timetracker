FROM node:16.5-alpine3.11 as build-stage
WORKDIR /app
COPY . .
RUN yarn install && yarn build

FROM nginx:stable-alpine as production-stage
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build-stage /app/dist .
ENTRYPOINT ["nginx", "-g", "daemon off;"]