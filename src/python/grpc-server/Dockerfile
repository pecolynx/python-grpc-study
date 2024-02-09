FROM python:3.11.2-slim-buster

WORKDIR /opt/app

COPY src.python.grpc-server/grpc-server.pex /opt/app/grpc_server.pex

ENTRYPOINT ["/bin/bash", "-c", "/opt/app/grpc_server.pex"]
