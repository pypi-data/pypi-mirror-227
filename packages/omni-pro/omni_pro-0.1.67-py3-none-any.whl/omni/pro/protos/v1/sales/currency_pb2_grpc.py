# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.sales import currency_pb2 as v1_dot_sales_dot_currency__pb2


class CurrencyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CurrencyCreate = channel.unary_unary(
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyCreate",
            request_serializer=v1_dot_sales_dot_currency__pb2.CurrencyCreateRequest.SerializeToString,
            response_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyCreateResponse.FromString,
        )
        self.CurrencyRead = channel.unary_unary(
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyRead",
            request_serializer=v1_dot_sales_dot_currency__pb2.CurrencyReadRequest.SerializeToString,
            response_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyReadResponse.FromString,
        )
        self.CurrencyUpdate = channel.unary_unary(
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyUpdate",
            request_serializer=v1_dot_sales_dot_currency__pb2.CurrencyUpdateRequest.SerializeToString,
            response_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyUpdateResponse.FromString,
        )
        self.CurrencyDelete = channel.unary_unary(
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyDelete",
            request_serializer=v1_dot_sales_dot_currency__pb2.CurrencyDeleteRequest.SerializeToString,
            response_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyDeleteResponse.FromString,
        )


class CurrencyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CurrencyCreate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CurrencyRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CurrencyUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CurrencyDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CurrencyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CurrencyCreate": grpc.unary_unary_rpc_method_handler(
            servicer.CurrencyCreate,
            request_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyCreateRequest.FromString,
            response_serializer=v1_dot_sales_dot_currency__pb2.CurrencyCreateResponse.SerializeToString,
        ),
        "CurrencyRead": grpc.unary_unary_rpc_method_handler(
            servicer.CurrencyRead,
            request_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyReadRequest.FromString,
            response_serializer=v1_dot_sales_dot_currency__pb2.CurrencyReadResponse.SerializeToString,
        ),
        "CurrencyUpdate": grpc.unary_unary_rpc_method_handler(
            servicer.CurrencyUpdate,
            request_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyUpdateRequest.FromString,
            response_serializer=v1_dot_sales_dot_currency__pb2.CurrencyUpdateResponse.SerializeToString,
        ),
        "CurrencyDelete": grpc.unary_unary_rpc_method_handler(
            servicer.CurrencyDelete,
            request_deserializer=v1_dot_sales_dot_currency__pb2.CurrencyDeleteRequest.FromString,
            response_serializer=v1_dot_sales_dot_currency__pb2.CurrencyDeleteResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.sales.currency.CurrencyService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class CurrencyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CurrencyCreate(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyCreate",
            v1_dot_sales_dot_currency__pb2.CurrencyCreateRequest.SerializeToString,
            v1_dot_sales_dot_currency__pb2.CurrencyCreateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CurrencyRead(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyRead",
            v1_dot_sales_dot_currency__pb2.CurrencyReadRequest.SerializeToString,
            v1_dot_sales_dot_currency__pb2.CurrencyReadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CurrencyUpdate(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyUpdate",
            v1_dot_sales_dot_currency__pb2.CurrencyUpdateRequest.SerializeToString,
            v1_dot_sales_dot_currency__pb2.CurrencyUpdateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CurrencyDelete(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.sales.currency.CurrencyService/CurrencyDelete",
            v1_dot_sales_dot_currency__pb2.CurrencyDeleteRequest.SerializeToString,
            v1_dot_sales_dot_currency__pb2.CurrencyDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
