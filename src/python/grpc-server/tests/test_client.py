
import grpc

from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc

def test_hello():
    with grpc.insecure_channel('localhost:50000') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='John'))
        assert response.message == 'Hello, John'
