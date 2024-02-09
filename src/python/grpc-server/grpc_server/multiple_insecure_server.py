from concurrent import futures

import threading
import signal
import grpc
from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc

import multiprocessing
import time
import logging

logger = logging.getLogger(__name__)

class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(
        self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext
    ) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}")

class GrpcServer:
    def __init__(self) -> None:
        pass

    def run(self, port_number: int) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
        server.add_insecure_port(f"[::]:{port_number}")
        server.start()
        print(f"gRPC server listening at :{port_number}")

        server.wait_for_termination()

def shutdown(logger: logging.Logger, worker: multiprocessing.Process):
    worker.terminate()
    worker.join()
    logger.info("Stopped gRPC server")

def run_multiple_insecure_server(num: int):
    workers = []
    for i in range(num):
        port_number = 50000 + i
        grpc_server = GrpcServer()
        
        worker = multiprocessing.Process(
            target=grpc_server.run, args=(port_number,)
        )

        worker.start()
        workers.append(worker)
    
    def on_done(signum, frame):
        logger.info('Got signal {}, {}'.format(signum, frame))
        tpe = futures.ThreadPoolExecutor(max_workers=3)
        for worker in workers:
            tpe.submit(shutdown, logger, worker)
        tpe.shutdown()
        
    signal.signal(signal.SIGTERM, on_done)

    for worker in workers:
        worker.join()
