FROM nginx:1.26 as base_build

EXPOSE 80
EXPOSE 3000

RUN rm /etc/nginx/conf.d/default.conf


FROM base_build as local_prod_build

COPY local_prod_build/nginx.conf /etc/nginx/nginx.conf


FROM base_build as prod_build

EXPOSE 443

COPY prod_build/nginx.conf /etc/nginx/nginx.conf
