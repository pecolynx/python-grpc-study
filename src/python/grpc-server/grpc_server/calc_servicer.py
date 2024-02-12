import logging
from collections.abc import Iterator
from typing import Generator

import grpc
from calc.v1 import calc_pb2, calc_pb2_grpc

logger = logging.getLogger(__name__)


class CalcServicer(calc_pb2_grpc.CalcServicer):
    def UnaryUnary(
        self, request: calc_pb2.CalcRequest, context: grpc.ServicerContext
    ) -> calc_pb2.CalcResponse:
        sum = 0
        for data in request.data:
            sum += data
        return calc_pb2.CalcResponse(data=[sum])

    def UnaryStream(
        self, request: calc_pb2.CalcRequest, context: grpc.ServicerContext
    ) -> Generator[calc_pb2.CalcResponse, None, None]:
        sum = 0
        for data in request.data:
            sum += data
            if data == 0:
                if sum != 0:
                    yield calc_pb2.CalcResponse(data=[sum])
                    sum = 0

        if sum != 0:
            yield calc_pb2.CalcResponse(data=[sum])

    def StreamUnary(
        self, request: Iterator[calc_pb2.CalcRequest], context: grpc.ServicerContext
    ) -> calc_pb2.CalcResponse:
        sum = 0
        for req in request:
            for data in req.data:
                sum += data
                if data == 0:
                    return calc_pb2.CalcResponse(data=[sum])
        return calc_pb2.CalcResponse(data=[])

    def StreamStream(
        self, request: Iterator[calc_pb2.CalcRequest], context: grpc.ServicerContext
    ) -> Generator[calc_pb2.CalcResponse, None, None]:
        sum = 0
        for req in request:
            for data in req.data:
                sum += data
                if data == 0:
                    yield calc_pb2.CalcResponse(data=[sum])
                    sum = 0
