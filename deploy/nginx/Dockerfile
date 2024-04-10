FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /usr/uvicorn_socket_folder

COPY nginx.conf /etc/nginx/conf.d