# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/sales/channel.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x16v1/sales/channel.proto\x12!pro.omni.oms.api.v1.sales.channel\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto"\xaf\x01\n\x07\x43hannel\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x0f\n\x07\x66low_id\x18\x04 \x01(\x05\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x06 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"{\n\x14\x43hannelCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0f\n\x07\x66low_id\x18\x03 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x04 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9f\x01\n\x15\x43hannelCreateResponse\x12;\n\x07\x63hannel\x18\x01 \x01(\x0b\x32*.pro.omni.oms.api.v1.sales.channel.Channel\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xf0\x02\n\x12\x43hannelReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xd9\x01\n\x13\x43hannelReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12<\n\x08\x63hannels\x18\x03 \x03(\x0b\x32*.pro.omni.oms.api.v1.sales.channel.Channel"\x8b\x01\n\x14\x43hannelUpdateRequest\x12;\n\x07\x63hannel\x18\x01 \x01(\x0b\x32*.pro.omni.oms.api.v1.sales.channel.Channel\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9f\x01\n\x15\x43hannelUpdateResponse\x12;\n\x07\x63hannel\x18\x01 \x01(\x0b\x32*.pro.omni.oms.api.v1.sales.channel.Channel\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"Z\n\x14\x43hannelDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"b\n\x15\x43hannelDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\x9d\x04\n\x0e\x43hannelService\x12\x82\x01\n\rChannelCreate\x12\x37.pro.omni.oms.api.v1.sales.channel.ChannelCreateRequest\x1a\x38.pro.omni.oms.api.v1.sales.channel.ChannelCreateResponse\x12|\n\x0b\x43hannelRead\x12\x35.pro.omni.oms.api.v1.sales.channel.ChannelReadRequest\x1a\x36.pro.omni.oms.api.v1.sales.channel.ChannelReadResponse\x12\x82\x01\n\rChannelUpdate\x12\x37.pro.omni.oms.api.v1.sales.channel.ChannelUpdateRequest\x1a\x38.pro.omni.oms.api.v1.sales.channel.ChannelUpdateResponse\x12\x82\x01\n\rChannelDelete\x12\x37.pro.omni.oms.api.v1.sales.channel.ChannelDeleteRequest\x1a\x38.pro.omni.oms.api.v1.sales.channel.ChannelDeleteResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.sales.channel_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_CHANNEL"]._serialized_start = 113
    _globals["_CHANNEL"]._serialized_end = 288
    _globals["_CHANNELCREATEREQUEST"]._serialized_start = 290
    _globals["_CHANNELCREATEREQUEST"]._serialized_end = 413
    _globals["_CHANNELCREATERESPONSE"]._serialized_start = 416
    _globals["_CHANNELCREATERESPONSE"]._serialized_end = 575
    _globals["_CHANNELREADREQUEST"]._serialized_start = 578
    _globals["_CHANNELREADREQUEST"]._serialized_end = 946
    _globals["_CHANNELREADRESPONSE"]._serialized_start = 949
    _globals["_CHANNELREADRESPONSE"]._serialized_end = 1166
    _globals["_CHANNELUPDATEREQUEST"]._serialized_start = 1169
    _globals["_CHANNELUPDATEREQUEST"]._serialized_end = 1308
    _globals["_CHANNELUPDATERESPONSE"]._serialized_start = 1311
    _globals["_CHANNELUPDATERESPONSE"]._serialized_end = 1470
    _globals["_CHANNELDELETEREQUEST"]._serialized_start = 1472
    _globals["_CHANNELDELETEREQUEST"]._serialized_end = 1562
    _globals["_CHANNELDELETERESPONSE"]._serialized_start = 1564
    _globals["_CHANNELDELETERESPONSE"]._serialized_end = 1662
    _globals["_CHANNELSERVICE"]._serialized_start = 1665
    _globals["_CHANNELSERVICE"]._serialized_end = 2206
# @@protoc_insertion_point(module_scope)
