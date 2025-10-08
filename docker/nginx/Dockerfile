FROM nginx:1.27-alpine

# Paths are relative to the build context (docker/nginx/)
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d /etc/nginx/conf.d

EXPOSE 80
