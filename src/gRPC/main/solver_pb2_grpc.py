# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import solver_pb2 as solver__pb2


class SolverServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AnalyzeOnUnaryRPC = channel.unary_unary(
                '/SolverService/AnalyzeOnUnaryRPC',
                request_serializer=solver__pb2.SolverRequest.SerializeToString,
                response_deserializer=solver__pb2.SolverResponse.FromString,
                )
        self.AnalyzeOnServerStreamingRPC = channel.unary_stream(
                '/SolverService/AnalyzeOnServerStreamingRPC',
                request_serializer=solver__pb2.SolverRequest.SerializeToString,
                response_deserializer=solver__pb2.SolverResponse.FromString,
                )
        self.AnalyzeOnClientStreamingRPC = channel.stream_unary(
                '/SolverService/AnalyzeOnClientStreamingRPC',
                request_serializer=solver__pb2.SolverRequest.SerializeToString,
                response_deserializer=solver__pb2.SolverResponse.FromString,
                )
        self.AnalyzeOnBidirectionalStreamingRPC = channel.stream_stream(
                '/SolverService/AnalyzeOnBidirectionalStreamingRPC',
                request_serializer=solver__pb2.SolverRequest.SerializeToString,
                response_deserializer=solver__pb2.SolverResponse.FromString,
                )


class SolverServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AnalyzeOnUnaryRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnalyzeOnServerStreamingRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnalyzeOnClientStreamingRPC(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AnalyzeOnBidirectionalStreamingRPC(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SolverServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AnalyzeOnUnaryRPC': grpc.unary_unary_rpc_method_handler(
                    servicer.AnalyzeOnUnaryRPC,
                    request_deserializer=solver__pb2.SolverRequest.FromString,
                    response_serializer=solver__pb2.SolverResponse.SerializeToString,
            ),
            'AnalyzeOnServerStreamingRPC': grpc.unary_stream_rpc_method_handler(
                    servicer.AnalyzeOnServerStreamingRPC,
                    request_deserializer=solver__pb2.SolverRequest.FromString,
                    response_serializer=solver__pb2.SolverResponse.SerializeToString,
            ),
            'AnalyzeOnClientStreamingRPC': grpc.stream_unary_rpc_method_handler(
                    servicer.AnalyzeOnClientStreamingRPC,
                    request_deserializer=solver__pb2.SolverRequest.FromString,
                    response_serializer=solver__pb2.SolverResponse.SerializeToString,
            ),
            'AnalyzeOnBidirectionalStreamingRPC': grpc.stream_stream_rpc_method_handler(
                    servicer.AnalyzeOnBidirectionalStreamingRPC,
                    request_deserializer=solver__pb2.SolverRequest.FromString,
                    response_serializer=solver__pb2.SolverResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SolverService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SolverService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AnalyzeOnUnaryRPC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SolverService/AnalyzeOnUnaryRPC',
            solver__pb2.SolverRequest.SerializeToString,
            solver__pb2.SolverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AnalyzeOnServerStreamingRPC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/SolverService/AnalyzeOnServerStreamingRPC',
            solver__pb2.SolverRequest.SerializeToString,
            solver__pb2.SolverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AnalyzeOnClientStreamingRPC(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/SolverService/AnalyzeOnClientStreamingRPC',
            solver__pb2.SolverRequest.SerializeToString,
            solver__pb2.SolverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AnalyzeOnBidirectionalStreamingRPC(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/SolverService/AnalyzeOnBidirectionalStreamingRPC',
            solver__pb2.SolverRequest.SerializeToString,
            solver__pb2.SolverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)