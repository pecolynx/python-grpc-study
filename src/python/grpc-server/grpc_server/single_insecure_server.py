import logging
import signal
import threading
from concurrent import futures

import grpc
from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc

logger = logging.getLogger(__name__)


class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(
        self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext
    ) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}")


def run_single_insecure_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("gRPC server listening at :50052")

    # wait until got SIGTERM, and will exec graceful shut down.
    done = threading.Event()

    def on_done(signum, frame):
        logger.info("Got signal {}, {}".format(signum, frame))
        done.set()

    signal.signal(signal.SIGTERM, on_done)
    done.wait()

    logger.info("Waiting for RPCs to complete...")
    server.wait_for_termination(10)
    server.stop(10)
    logger.info("Stopped gRPC server")
