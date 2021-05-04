#! /bin/bash -e
docker run \
    --rm \
    -t \
    -e INFLUXDB_V2_TOKEN \
    -e INFLUXDB_V2_URL \
    -e INFLUXDB_V2_ORG \
    -e INFLUXDB_V2_SSL_CA_CERT \
    -e GATEWAY_IP \
    -e CLOUDID \
    -e INSTALLATION_CODE \
    cgspeck/eagle200-to-influx:latest

