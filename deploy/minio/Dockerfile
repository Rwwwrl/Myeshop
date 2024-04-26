FROM minio/minio

EXPOSE 9000
EXPOSE 9001

RUN mkdir -p /data/loki-data && \
    mkdir -p /data/loki-ruler

CMD ["minio", "server", "/data", "--console-address", ":9001"]
