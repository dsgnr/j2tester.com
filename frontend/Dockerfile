FROM node:23-alpine3.19 AS builder
ARG API_URL 
ENV API_URL=$API_URL

COPY web /app
WORKDIR /app
RUN yarn install && yarn build

# production environment
FROM nginx:stable-alpine-slim AS web
ARG API_URL 
ENV API_URL=$API_URL
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./entrypoint.sh /entrypoint.sh
COPY ./nginx/nginx.conf.template /etc/nginx/conf.d/default.conf.template
EXPOSE 80
CMD ["sh", "/entrypoint.sh"]
