FROM nginx:1.26

EXPOSE 80
EXPOSE 3000

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /usr/uvicorn_socket_folder

COPY nginx.conf /etc/nginx/nginx.conf