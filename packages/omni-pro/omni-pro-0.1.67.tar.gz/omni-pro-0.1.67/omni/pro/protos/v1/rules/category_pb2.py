# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/rules/category.proto
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
    b'\n\x17v1/rules/category.proto\x12"pro.omni.oms.api.v1.rules.category\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto"\xb9\x01\n\x08\x43\x61tegory\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x18\n\x10\x61ttribute_doc_id\x18\x04 \x01(\t\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x06 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\x85\x01\n\x15\x43\x61tegoryCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x18\n\x10\x61ttribute_doc_id\x18\x03 \x01(\t\x12\x36\n\x07\x63ontext\x18\x04 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x16\x43\x61tegoryCreateResponse\x12>\n\x08\x63\x61tegory\x18\x01 \x01(\x0b\x32,.pro.omni.oms.api.v1.rules.category.Category\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xf1\x02\n\x13\x43\x61tegoryReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xde\x01\n\x14\x43\x61tegoryReadResponse\x12@\n\ncategories\x18\x01 \x03(\x0b\x32,.pro.omni.oms.api.v1.rules.category.Category\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12I\n\x11response_standard\x18\x03 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\x8f\x01\n\x15\x43\x61tegoryUpdateRequest\x12>\n\x08\x63\x61tegory\x18\x01 \x01(\x0b\x32,.pro.omni.oms.api.v1.rules.category.Category\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x16\x43\x61tegoryUpdateResponse\x12>\n\x08\x63\x61tegory\x18\x01 \x01(\x0b\x32,.pro.omni.oms.api.v1.rules.category.Category\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"[\n\x15\x43\x61tegoryDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"c\n\x16\x43\x61tegoryDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xbb\x04\n\x0f\x43\x61tegoryService\x12\x89\x01\n\x0e\x43\x61tegoryCreate\x12\x39.pro.omni.oms.api.v1.rules.category.CategoryCreateRequest\x1a:.pro.omni.oms.api.v1.rules.category.CategoryCreateResponse"\x00\x12\x83\x01\n\x0c\x43\x61tegoryRead\x12\x37.pro.omni.oms.api.v1.rules.category.CategoryReadRequest\x1a\x38.pro.omni.oms.api.v1.rules.category.CategoryReadResponse"\x00\x12\x89\x01\n\x0e\x43\x61tegoryUpdate\x12\x39.pro.omni.oms.api.v1.rules.category.CategoryUpdateRequest\x1a:.pro.omni.oms.api.v1.rules.category.CategoryUpdateResponse"\x00\x12\x89\x01\n\x0e\x43\x61tegoryDelete\x12\x39.pro.omni.oms.api.v1.rules.category.CategoryDeleteRequest\x1a:.pro.omni.oms.api.v1.rules.category.CategoryDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.rules.category_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_CATEGORY"]._serialized_start = 115
    _globals["_CATEGORY"]._serialized_end = 300
    _globals["_CATEGORYCREATEREQUEST"]._serialized_start = 303
    _globals["_CATEGORYCREATEREQUEST"]._serialized_end = 436
    _globals["_CATEGORYCREATERESPONSE"]._serialized_start = 439
    _globals["_CATEGORYCREATERESPONSE"]._serialized_end = 602
    _globals["_CATEGORYREADREQUEST"]._serialized_start = 605
    _globals["_CATEGORYREADREQUEST"]._serialized_end = 974
    _globals["_CATEGORYREADRESPONSE"]._serialized_start = 977
    _globals["_CATEGORYREADRESPONSE"]._serialized_end = 1199
    _globals["_CATEGORYUPDATEREQUEST"]._serialized_start = 1202
    _globals["_CATEGORYUPDATEREQUEST"]._serialized_end = 1345
    _globals["_CATEGORYUPDATERESPONSE"]._serialized_start = 1348
    _globals["_CATEGORYUPDATERESPONSE"]._serialized_end = 1511
    _globals["_CATEGORYDELETEREQUEST"]._serialized_start = 1513
    _globals["_CATEGORYDELETEREQUEST"]._serialized_end = 1604
    _globals["_CATEGORYDELETERESPONSE"]._serialized_start = 1606
    _globals["_CATEGORYDELETERESPONSE"]._serialized_end = 1705
    _globals["_CATEGORYSERVICE"]._serialized_start = 1708
    _globals["_CATEGORYSERVICE"]._serialized_end = 2279
# @@protoc_insertion_point(module_scope)
