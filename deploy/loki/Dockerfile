FROM grafana/loki:2.9.2

RUN mkdir -p /etc/loki

EXPOSE 3100
EXPOSE 7946
EXPOSE 9095
EXPOSE 3102

COPY loki_config.yaml /etc/loki/config.yaml
