import time
import unittest

import grpc
import grpc_testing
from calc.v1 import calc_pb2
from grpc_server.calc_servicer import CalcServicer


class CalcServerServicerTest(unittest.TestCase):
    def setUp(self):
        self._real_time = grpc_testing.strict_real_time()
        self._fake_time = grpc_testing.strict_fake_time(time.time())
        self.calc_service = calc_pb2.DESCRIPTOR.services_by_name["Calc"]

        servicer = CalcServicer()
        descriptors_to_servicers = {self.calc_service: servicer}
        self._real_time_server = grpc_testing.server_from_dictionary(
            descriptors_to_servicers, self._real_time
        )
        self._fake_time_server = grpc_testing.server_from_dictionary(
            descriptors_to_servicers, self._fake_time
        )

    def test_successful_unary_unary(self):
        unary_unary = self.calc_service.methods_by_name["UnaryUnary"]
        request = calc_pb2.CalcRequest(data=[1, 2, 3])
        rpc = self._real_time_server.invoke_unary_unary(
            unary_unary,
            (),
            request,
            None,
        )
        rpc.initial_metadata()
        response, trailing_metadata, code, details = rpc.termination()

        self.assertEqual(response, calc_pb2.CalcResponse(data=[1 + 2 + 3]))
        self.assertIs(code, grpc.StatusCode.OK)

    def test_successful_unary_stream(self):
        unary_stream = self.calc_service.methods_by_name["UnaryStream"]
        request = calc_pb2.CalcRequest(data=[1, 2, 3, 0, 4, 5, 6])
        rpc = self._real_time_server.invoke_unary_stream(
            unary_stream,
            (),
            request,
            None,
        )
        rpc.initial_metadata()
        trailing_metadata, code, details = rpc.termination()

        self.assertEqual(rpc.take_response(), calc_pb2.CalcResponse(data=[1 + 2 + 3]))
        self.assertEqual(rpc.take_response(), calc_pb2.CalcResponse(data=[4 + 5 + 6]))
        self.assertIs(code, grpc.StatusCode.OK)

    def test_successful_stream_unary(self):
        stream_unary = self.calc_service.methods_by_name["StreamUnary"]
        rpc = self._real_time_server.invoke_stream_unary(
            stream_unary,
            (),
            None,
        )
        rpc.send_request(calc_pb2.CalcRequest(data=[1, 2]))
        rpc.send_request(calc_pb2.CalcRequest(data=[3, 0]))
        rpc.requests_closed()
        rpc.initial_metadata()
        response, trailing_metadata, code, details = rpc.termination()

        self.assertEqual(response, calc_pb2.CalcResponse(data=[1 + 2 + 3]))
        self.assertIs(code, grpc.StatusCode.OK)

    def test_successful_stream_stream(self):
        stream_stream = self.calc_service.methods_by_name["StreamStream"]
        rpc = self._real_time_server.invoke_stream_stream(
            stream_stream,
            (),
            None,
        )
        rpc.send_request(calc_pb2.CalcRequest(data=[1, 2]))
        rpc.send_request(calc_pb2.CalcRequest(data=[3, 0, 4]))
        rpc.send_request(calc_pb2.CalcRequest(data=[5]))
        rpc.send_request(calc_pb2.CalcRequest(data=[6, 0]))
        rpc.requests_closed()
        rpc.initial_metadata()

        self.assertEqual(rpc.take_response(), calc_pb2.CalcResponse(data=[1 + 2 + 3]))
        self.assertEqual(rpc.take_response(), calc_pb2.CalcResponse(data=[4 + 5 + 6]))

        trailing_metadata, code, details = rpc.termination()
        self.assertIs(code, grpc.StatusCode.OK)
