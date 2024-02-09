import logging

from grpc_server.single_insecure_server import run_single_insecure_server
from grpc_server.multiple_insecure_server import run_multiple_insecure_server

logging.basicConfig(level=logging.INFO)


# run_single_insecure_server()
run_multiple_insecure_server(2)
