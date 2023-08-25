# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/sales/user.proto
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
    b'\n\x13v1/sales/user.proto\x12\x1epro.omni.oms.api.v1.sales.user\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto"\xa2\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x0buser_doc_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12*\n\x06\x61\x63tive\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x05 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"n\n\x11UserCreateRequest\x12\x13\n\x0buser_doc_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x93\x01\n\x12UserCreateResponse\x12\x32\n\x04user\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.user.User\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xed\x02\n\x0fUserReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xcc\x01\n\x10UserReadResponse\x12\x32\n\x04user\x18\x01 \x03(\x0b\x32$.pro.omni.oms.api.v1.sales.user.User\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x03 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData"\x7f\n\x11UserUpdateRequest\x12\x32\n\x04user\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.user.User\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x93\x01\n\x12UserUpdateResponse\x12\x32\n\x04user\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.user.User\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"W\n\x11UserDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"_\n\x12UserDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xe3\x03\n\x0bUserService\x12u\n\nUserCreate\x12\x31.pro.omni.oms.api.v1.sales.user.UserCreateRequest\x1a\x32.pro.omni.oms.api.v1.sales.user.UserCreateResponse"\x00\x12o\n\x08UserRead\x12/.pro.omni.oms.api.v1.sales.user.UserReadRequest\x1a\x30.pro.omni.oms.api.v1.sales.user.UserReadResponse"\x00\x12u\n\nUserUpdate\x12\x31.pro.omni.oms.api.v1.sales.user.UserUpdateRequest\x1a\x32.pro.omni.oms.api.v1.sales.user.UserUpdateResponse"\x00\x12u\n\nUserDelete\x12\x31.pro.omni.oms.api.v1.sales.user.UserDeleteRequest\x1a\x32.pro.omni.oms.api.v1.sales.user.UserDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.sales.user_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_USER"]._serialized_start = 107
    _globals["_USER"]._serialized_end = 269
    _globals["_USERCREATEREQUEST"]._serialized_start = 271
    _globals["_USERCREATEREQUEST"]._serialized_end = 381
    _globals["_USERCREATERESPONSE"]._serialized_start = 384
    _globals["_USERCREATERESPONSE"]._serialized_end = 531
    _globals["_USERREADREQUEST"]._serialized_start = 534
    _globals["_USERREADREQUEST"]._serialized_end = 899
    _globals["_USERREADRESPONSE"]._serialized_start = 902
    _globals["_USERREADRESPONSE"]._serialized_end = 1106
    _globals["_USERUPDATEREQUEST"]._serialized_start = 1108
    _globals["_USERUPDATEREQUEST"]._serialized_end = 1235
    _globals["_USERUPDATERESPONSE"]._serialized_start = 1238
    _globals["_USERUPDATERESPONSE"]._serialized_end = 1385
    _globals["_USERDELETEREQUEST"]._serialized_start = 1387
    _globals["_USERDELETEREQUEST"]._serialized_end = 1474
    _globals["_USERDELETERESPONSE"]._serialized_start = 1476
    _globals["_USERDELETERESPONSE"]._serialized_end = 1571
    _globals["_USERSERVICE"]._serialized_start = 1574
    _globals["_USERSERVICE"]._serialized_end = 2057
# @@protoc_insertion_point(module_scope)
