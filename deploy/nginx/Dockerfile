FROM nginx:1.26 as base_build

EXPOSE 80
EXPOSE 3000

RUN rm /etc/nginx/conf.d/default.conf


FROM base_build as local_prod_build

COPY local_prod_nginx.conf /etc/nginx/nginx.conf


FROM base_build as prod_build

COPY prod_nginx.conf /etc/nginx/nginx.conf
