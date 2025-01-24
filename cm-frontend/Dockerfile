FROM node:alpine AS build

WORKDIR /app/ui-src

COPY ./cm-frontend /app/ui-src

RUN npm install -g @angular/cli@18
RUN npm install && npm run build

FROM nginx:latest AS ngi
# Copying compiled code and nginx config to different folder
# NOTE: This path may change according to your project's output folder
COPY ./cm-frontend/nginx.conf  /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/ui-src/dist/cm-frontend/browser /usr/share/nginx/html
