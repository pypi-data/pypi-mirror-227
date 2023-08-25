# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.rules import (
    delviery_shipper_warehouse_pb2 as v1_dot_rules_dot_delviery__shipper__warehouse__pb2,
)


class DeliveryShipperWarehouseServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DeliveryShipperWarehouseCreate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseCreate",
            request_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateResponse.FromString,
        )
        self.DeliveryShipperWarehouseRead = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseRead",
            request_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadResponse.FromString,
        )
        self.DeliveryShipperWarehouseUpdate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseUpdate",
            request_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateResponse.FromString,
        )
        self.DeliveryShipperWarehouseDelete = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseDelete",
            request_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteResponse.FromString,
        )


class DeliveryShipperWarehouseServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DeliveryShipperWarehouseCreate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryShipperWarehouseRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryShipperWarehouseUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryShipperWarehouseDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_DeliveryShipperWarehouseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "DeliveryShipperWarehouseCreate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryShipperWarehouseCreate,
            request_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateResponse.SerializeToString,
        ),
        "DeliveryShipperWarehouseRead": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryShipperWarehouseRead,
            request_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadRequest.FromString,
            response_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadResponse.SerializeToString,
        ),
        "DeliveryShipperWarehouseUpdate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryShipperWarehouseUpdate,
            request_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateResponse.SerializeToString,
        ),
        "DeliveryShipperWarehouseDelete": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryShipperWarehouseDelete,
            request_deserializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteRequest.FromString,
            response_serializer=v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class DeliveryShipperWarehouseService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DeliveryShipperWarehouseCreate(
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
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseCreate",
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateRequest.SerializeToString,
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseCreateResponse.FromString,
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
    def DeliveryShipperWarehouseRead(
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
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseRead",
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadRequest.SerializeToString,
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseReadResponse.FromString,
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
    def DeliveryShipperWarehouseUpdate(
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
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseUpdate",
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateRequest.SerializeToString,
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseUpdateResponse.FromString,
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
    def DeliveryShipperWarehouseDelete(
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
            "/pro.omni.oms.api.v1.rules.delivery_shipper_warehouse.DeliveryShipperWarehouseService/DeliveryShipperWarehouseDelete",
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteRequest.SerializeToString,
            v1_dot_rules_dot_delviery__shipper__warehouse__pb2.DeliveryShipperWarehouseDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
