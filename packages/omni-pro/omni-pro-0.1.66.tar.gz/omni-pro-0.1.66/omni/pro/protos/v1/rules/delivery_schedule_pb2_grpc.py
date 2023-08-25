# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.rules import delivery_schedule_pb2 as v1_dot_rules_dot_delivery__schedule__pb2


class DeliveryScheduleServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DeliveryScheduleCreate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleCreate",
            request_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateResponse.FromString,
        )
        self.DeliveryScheduleRead = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleRead",
            request_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadResponse.FromString,
        )
        self.DeliveryScheduleUpdate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleUpdate",
            request_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateResponse.FromString,
        )
        self.DeliveryScheduleDelete = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleDelete",
            request_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteResponse.FromString,
        )


class DeliveryScheduleServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DeliveryScheduleCreate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryScheduleRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryScheduleUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryScheduleDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_DeliveryScheduleServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "DeliveryScheduleCreate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryScheduleCreate,
            request_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateResponse.SerializeToString,
        ),
        "DeliveryScheduleRead": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryScheduleRead,
            request_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadResponse.SerializeToString,
        ),
        "DeliveryScheduleUpdate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryScheduleUpdate,
            request_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateResponse.SerializeToString,
        ),
        "DeliveryScheduleDelete": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryScheduleDelete,
            request_deserializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class DeliveryScheduleService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DeliveryScheduleCreate(
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
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleCreate",
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateRequest.SerializeToString,
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleCreateResponse.FromString,
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
    def DeliveryScheduleRead(
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
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleRead",
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadRequest.SerializeToString,
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleReadResponse.FromString,
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
    def DeliveryScheduleUpdate(
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
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleUpdate",
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateRequest.SerializeToString,
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleUpdateResponse.FromString,
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
    def DeliveryScheduleDelete(
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
            "/pro.omni.oms.api.v1.rules.delivery_schedule.DeliveryScheduleService/DeliveryScheduleDelete",
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteRequest.SerializeToString,
            v1_dot_rules_dot_delivery__schedule__pb2.DeliveryScheduleDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
