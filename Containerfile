FROM registry.access.redhat.com/ubi9/nodejs-22@sha256:90d19cd1a4ba03bcb63c46320862955fc1560511532ee35ff472289bf5fe2276 AS build
WORKDIR /opt/app-root/src
COPY --chown=1001:0 package*.json ./
RUN npm ci
COPY --chown=1001:0 . .
RUN npm run build

FROM docker.io/nginxinc/nginx-unprivileged@sha256:c18d735d33a1c3ccb5ef201d504e5b4aa4d003e81f034b329011267f4c4d0f58
COPY --from=build /opt/app-root/src/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
