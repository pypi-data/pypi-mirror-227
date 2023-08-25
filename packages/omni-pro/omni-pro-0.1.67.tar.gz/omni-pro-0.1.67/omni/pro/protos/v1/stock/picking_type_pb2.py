# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/stock/picking_type.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2
from omni.pro.protos.v1.stock import location_pb2 as v1_dot_stock_dot_location__pb2
from omni.pro.protos.v1.stock import sequence_pb2 as v1_dot_stock_dot_sequence__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1bv1/stock/picking_type.proto\x12&pro.omni.oms.api.v1.stock.picking_type\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x17v1/stock/sequence.proto\x1a\x17v1/stock/location.proto"\xf9\x04\n\x0bPickingType\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\rsequence_code\x18\x03 \x01(\t\x12\x14\n\x0cwarehouse_id\x18\x04 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x05 \x01(\t\x12\x1e\n\x16return_picking_type_id\x18\x06 \x01(\x05\x12\x33\n\x0fshow_operations\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x31\n\rshow_reserved\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12M\n\x17\x64\x65\x66\x61ult_location_src_id\x18\t \x01(\x0b\x32,.pro.omni.oms.api.v1.stock.location.Location\x12N\n\x18\x64\x65\x66\x61ult_location_dest_id\x18\n \x01(\x0b\x32,.pro.omni.oms.api.v1.stock.location.Location\x12\x41\n\x0bsequence_id\x18\x0b \x01(\x0b\x32,.pro.omni.oms.api.v1.stock.sequence.Sequence\x12\x0f\n\x07\x62\x61rcode\x18\x0c \x01(\t\x12\x1a\n\x12reservation_method\x18\r \x01(\t\x12\x11\n\ttype_code\x18\x0e \x01(\t\x12*\n\x06\x61\x63tive\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x10 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xbb\x03\n\x18PickingTypeCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rsequence_code\x18\x02 \x01(\t\x12\x14\n\x0cwarehouse_id\x18\x03 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x04 \x01(\t\x12\x1e\n\x16return_picking_type_id\x18\x05 \x01(\x05\x12\x33\n\x0fshow_operations\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x31\n\rshow_reserved\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x1f\n\x17\x64\x65\x66\x61ult_location_src_id\x18\x08 \x01(\x05\x12 \n\x18\x64\x65\x66\x61ult_location_dest_id\x18\t \x01(\x05\x12\x0f\n\x07\x62\x61rcode\x18\n \x01(\t\x12\x1a\n\x12reservation_method\x18\x0b \x01(\t\x12\x11\n\ttype_code\x18\x0c \x01(\t\x12\x13\n\x0bsequence_id\x18\r \x01(\x05\x12\x36\n\x07\x63ontext\x18\x0e \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xb1\x01\n\x19PickingTypeCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12I\n\x0cpicking_type\x18\x02 \x01(\x0b\x32\x33.pro.omni.oms.api.v1.stock.picking_type.PickingType"\xf4\x02\n\x16PickingTypeReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xeb\x01\n\x17PickingTypeReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12J\n\rpicking_types\x18\x03 \x03(\x0b\x32\x33.pro.omni.oms.api.v1.stock.picking_type.PickingType"\x9d\x01\n\x18PickingTypeUpdateRequest\x12I\n\x0cpicking_type\x18\x01 \x01(\x0b\x32\x33.pro.omni.oms.api.v1.stock.picking_type.PickingType\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xb1\x01\n\x19PickingTypeUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12I\n\x0cpicking_type\x18\x02 \x01(\x0b\x32\x33.pro.omni.oms.api.v1.stock.picking_type.PickingType"^\n\x18PickingTypeDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"f\n\x19PickingTypeDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\x82\x05\n\x12PickingTypeService\x12\x9a\x01\n\x11PickingTypeCreate\x12@.pro.omni.oms.api.v1.stock.picking_type.PickingTypeCreateRequest\x1a\x41.pro.omni.oms.api.v1.stock.picking_type.PickingTypeCreateResponse"\x00\x12\x94\x01\n\x0fPickingTypeRead\x12>.pro.omni.oms.api.v1.stock.picking_type.PickingTypeReadRequest\x1a?.pro.omni.oms.api.v1.stock.picking_type.PickingTypeReadResponse"\x00\x12\x9a\x01\n\x11PickingTypeUpdate\x12@.pro.omni.oms.api.v1.stock.picking_type.PickingTypeUpdateRequest\x1a\x41.pro.omni.oms.api.v1.stock.picking_type.PickingTypeUpdateResponse"\x00\x12\x9a\x01\n\x11PickingTypeDelete\x12@.pro.omni.oms.api.v1.stock.picking_type.PickingTypeDeleteRequest\x1a\x41.pro.omni.oms.api.v1.stock.picking_type.PickingTypeDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.stock.picking_type_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_PICKINGTYPE"]._serialized_start = 173
    _globals["_PICKINGTYPE"]._serialized_end = 806
    _globals["_PICKINGTYPECREATEREQUEST"]._serialized_start = 809
    _globals["_PICKINGTYPECREATEREQUEST"]._serialized_end = 1252
    _globals["_PICKINGTYPECREATERESPONSE"]._serialized_start = 1255
    _globals["_PICKINGTYPECREATERESPONSE"]._serialized_end = 1432
    _globals["_PICKINGTYPEREADREQUEST"]._serialized_start = 1435
    _globals["_PICKINGTYPEREADREQUEST"]._serialized_end = 1807
    _globals["_PICKINGTYPEREADRESPONSE"]._serialized_start = 1810
    _globals["_PICKINGTYPEREADRESPONSE"]._serialized_end = 2045
    _globals["_PICKINGTYPEUPDATEREQUEST"]._serialized_start = 2048
    _globals["_PICKINGTYPEUPDATEREQUEST"]._serialized_end = 2205
    _globals["_PICKINGTYPEUPDATERESPONSE"]._serialized_start = 2208
    _globals["_PICKINGTYPEUPDATERESPONSE"]._serialized_end = 2385
    _globals["_PICKINGTYPEDELETEREQUEST"]._serialized_start = 2387
    _globals["_PICKINGTYPEDELETEREQUEST"]._serialized_end = 2481
    _globals["_PICKINGTYPEDELETERESPONSE"]._serialized_start = 2483
    _globals["_PICKINGTYPEDELETERESPONSE"]._serialized_end = 2585
    _globals["_PICKINGTYPESERVICE"]._serialized_start = 2588
    _globals["_PICKINGTYPESERVICE"]._serialized_end = 3230
# @@protoc_insertion_point(module_scope)
