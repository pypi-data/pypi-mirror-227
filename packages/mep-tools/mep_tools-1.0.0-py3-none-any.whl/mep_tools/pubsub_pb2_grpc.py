# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import pubsub_pb2 as pubsub__pb2


class PublisherServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Add = channel.unary_unary(
                '/PublisherService/Add',
                request_serializer=pubsub__pb2.SubRequest.SerializeToString,
                response_deserializer=pubsub__pb2.SubResponse.FromString,
                )
        self.Remove = channel.unary_unary(
                '/PublisherService/Remove',
                request_serializer=pubsub__pb2.SubRequest.SerializeToString,
                response_deserializer=pubsub__pb2.SubResponse.FromString,
                )
        self.Notify = channel.stream_stream(
                '/PublisherService/Notify',
                request_serializer=pubsub__pb2.SubRequest.SerializeToString,
                response_deserializer=pubsub__pb2.SubResponse.FromString,
                )


class PublisherServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Add(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Remove(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Notify(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PublisherServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=pubsub__pb2.SubRequest.FromString,
                    response_serializer=pubsub__pb2.SubResponse.SerializeToString,
            ),
            'Remove': grpc.unary_unary_rpc_method_handler(
                    servicer.Remove,
                    request_deserializer=pubsub__pb2.SubRequest.FromString,
                    response_serializer=pubsub__pb2.SubResponse.SerializeToString,
            ),
            'Notify': grpc.stream_stream_rpc_method_handler(
                    servicer.Notify,
                    request_deserializer=pubsub__pb2.SubRequest.FromString,
                    response_serializer=pubsub__pb2.SubResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PublisherService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PublisherService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PublisherService/Add',
            pubsub__pb2.SubRequest.SerializeToString,
            pubsub__pb2.SubResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Remove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PublisherService/Remove',
            pubsub__pb2.SubRequest.SerializeToString,
            pubsub__pb2.SubResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Notify(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/PublisherService/Notify',
            pubsub__pb2.SubRequest.SerializeToString,
            pubsub__pb2.SubResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class SubscriberServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Update = channel.stream_stream(
                '/SubscriberService/Update',
                request_serializer=pubsub__pb2.PubRequest.SerializeToString,
                response_deserializer=pubsub__pb2.PubResponse.FromString,
                )


class SubscriberServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Update(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SubscriberServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Update': grpc.stream_stream_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=pubsub__pb2.PubRequest.FromString,
                    response_serializer=pubsub__pb2.PubResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SubscriberService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SubscriberService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Update(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/SubscriberService/Update',
            pubsub__pb2.PubRequest.SerializeToString,
            pubsub__pb2.PubResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
