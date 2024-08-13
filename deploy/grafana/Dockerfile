FROM grafana/grafana-enterprise

EXPOSE 3000

COPY datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml
COPY dashboards/dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY dashboards/node_exporter_dashboard.json /etc/grafana/provisioning/dashboards/node_exporter_dashboard.json
COPY dashboards/postgres_exporter_dashboard.json /etc/grafana/provisioning/dashboards/postgres_exporter_dashboard.json
