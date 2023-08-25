# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/rules/delivery_warehouse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2
from omni.pro.protos.v1.rules import warehouse_hierarchy_pb2 as v1_dot_rules_dot_warehouse__hierarchy__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!v1/rules/delivery_warehouse.proto\x12,pro.omni.oms.api.v1.rules.delivery_warehouse\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a"v1/rules/warehouse_hierarchy.proto"\x9f\x02\n\x11\x44\x65liveryWarehouse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12#\n\x1bhierarchy_warehouse_sort_by\x18\x03 \x01(\t\x12^\n\x13transfer_warehouses\x18\x04 \x03(\x0b\x32\x41.pro.omni.oms.api.v1.rules.warehouse_hierarchy.WarehouseHierarchy\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x06 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\x8b\x01\n\x1e\x44\x65liveryWarehouseCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x1bhierarchy_warehouse_sort_by\x18\x02 \x01(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc9\x01\n\x1f\x44\x65liveryWarehouseCreateResponse\x12[\n\x12\x64\x65livery_warehouse\x18\x01 \x01(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xfa\x02\n\x1c\x44\x65liveryWarehouseReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x83\x02\n\x1d\x44\x65liveryWarehouseReadResponse\x12\\\n\x13\x64\x65livery_warehouses\x18\x01 \x03(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12I\n\x11response_standard\x18\x03 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xb5\x01\n\x1e\x44\x65liveryWarehouseUpdateRequest\x12[\n\x12\x64\x65livery_warehouse\x18\x01 \x01(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc9\x01\n\x1f\x44\x65liveryWarehouseUpdateResponse\x12[\n\x12\x64\x65livery_warehouse\x18\x01 \x01(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"d\n\x1e\x44\x65liveryWarehouseDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"l\n\x1f\x44\x65liveryWarehouseDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\x94\x01\n\x1b\x41\x64\x64TransferWarehouseRequest\x12\x1d\n\x15\x64\x65livery_warehouse_id\x18\x01 \x01(\t\x12\x1e\n\x16warehouse_herarchy_ids\x18\x02 \x03(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc6\x01\n\x1c\x41\x64\x64TransferWarehouseResponse\x12[\n\x12\x64\x65livery_warehouse\x18\x01 \x01(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\x97\x01\n\x1eRemoveTransferWarehouseRequest\x12\x1d\n\x15\x64\x65livery_warehouse_id\x18\x01 \x01(\t\x12\x1e\n\x16warehouse_herarchy_ids\x18\x02 \x03(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc9\x01\n\x1fRemoveTransferWarehouseResponse\x12[\n\x12\x64\x65livery_warehouse\x18\x01 \x01(\x0b\x32?.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouse\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xed\x08\n\x18\x44\x65liveryWarehouseService\x12\xb8\x01\n\x17\x44\x65liveryWarehouseCreate\x12L.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseCreateRequest\x1aM.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseCreateResponse"\x00\x12\xb2\x01\n\x15\x44\x65liveryWarehouseRead\x12J.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseReadRequest\x1aK.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseReadResponse"\x00\x12\xb8\x01\n\x17\x44\x65liveryWarehouseUpdate\x12L.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseUpdateRequest\x1aM.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseUpdateResponse"\x00\x12\xb8\x01\n\x17\x44\x65liveryWarehouseDelete\x12L.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseDeleteRequest\x1aM.pro.omni.oms.api.v1.rules.delivery_warehouse.DeliveryWarehouseDeleteResponse"\x00\x12\xaf\x01\n\x14\x41\x64\x64TransferWarehouse\x12I.pro.omni.oms.api.v1.rules.delivery_warehouse.AddTransferWarehouseRequest\x1aJ.pro.omni.oms.api.v1.rules.delivery_warehouse.AddTransferWarehouseResponse"\x00\x12\xb8\x01\n\x17RemoveTransferWarehouse\x12L.pro.omni.oms.api.v1.rules.delivery_warehouse.RemoveTransferWarehouseRequest\x1aM.pro.omni.oms.api.v1.rules.delivery_warehouse.RemoveTransferWarehouseResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.rules.delivery_warehouse_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_DELIVERYWAREHOUSE"]._serialized_start = 171
    _globals["_DELIVERYWAREHOUSE"]._serialized_end = 458
    _globals["_DELIVERYWAREHOUSECREATEREQUEST"]._serialized_start = 461
    _globals["_DELIVERYWAREHOUSECREATEREQUEST"]._serialized_end = 600
    _globals["_DELIVERYWAREHOUSECREATERESPONSE"]._serialized_start = 603
    _globals["_DELIVERYWAREHOUSECREATERESPONSE"]._serialized_end = 804
    _globals["_DELIVERYWAREHOUSEREADREQUEST"]._serialized_start = 807
    _globals["_DELIVERYWAREHOUSEREADREQUEST"]._serialized_end = 1185
    _globals["_DELIVERYWAREHOUSEREADRESPONSE"]._serialized_start = 1188
    _globals["_DELIVERYWAREHOUSEREADRESPONSE"]._serialized_end = 1447
    _globals["_DELIVERYWAREHOUSEUPDATEREQUEST"]._serialized_start = 1450
    _globals["_DELIVERYWAREHOUSEUPDATEREQUEST"]._serialized_end = 1631
    _globals["_DELIVERYWAREHOUSEUPDATERESPONSE"]._serialized_start = 1634
    _globals["_DELIVERYWAREHOUSEUPDATERESPONSE"]._serialized_end = 1835
    _globals["_DELIVERYWAREHOUSEDELETEREQUEST"]._serialized_start = 1837
    _globals["_DELIVERYWAREHOUSEDELETEREQUEST"]._serialized_end = 1937
    _globals["_DELIVERYWAREHOUSEDELETERESPONSE"]._serialized_start = 1939
    _globals["_DELIVERYWAREHOUSEDELETERESPONSE"]._serialized_end = 2047
    _globals["_ADDTRANSFERWAREHOUSEREQUEST"]._serialized_start = 2050
    _globals["_ADDTRANSFERWAREHOUSEREQUEST"]._serialized_end = 2198
    _globals["_ADDTRANSFERWAREHOUSERESPONSE"]._serialized_start = 2201
    _globals["_ADDTRANSFERWAREHOUSERESPONSE"]._serialized_end = 2399
    _globals["_REMOVETRANSFERWAREHOUSEREQUEST"]._serialized_start = 2402
    _globals["_REMOVETRANSFERWAREHOUSEREQUEST"]._serialized_end = 2553
    _globals["_REMOVETRANSFERWAREHOUSERESPONSE"]._serialized_start = 2556
    _globals["_REMOVETRANSFERWAREHOUSERESPONSE"]._serialized_end = 2757
    _globals["_DELIVERYWAREHOUSESERVICE"]._serialized_start = 2760
    _globals["_DELIVERYWAREHOUSESERVICE"]._serialized_end = 3893
# @@protoc_insertion_point(module_scope)
