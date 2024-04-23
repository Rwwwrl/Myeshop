FROM grafana/grafana-enterprise

COPY datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml
COPY dashboards/dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY dashboards/node_exporter_dashboard.json /etc/grafana/provisioning/dashboards/node_exporter_dashboard.json
