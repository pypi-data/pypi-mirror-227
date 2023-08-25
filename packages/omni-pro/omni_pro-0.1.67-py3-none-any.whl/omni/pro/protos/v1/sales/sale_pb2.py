# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/sales/sale.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13v1/sales/sale.proto\x12\x1epro.omni.oms.api.v1.sales.sale\x1a\x11\x63ommon/base.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/protobuf/struct.proto"\xb3\x03\n\x04Sale\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12.\n\ndate_order\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06origin\x18\x04 \x01(\t\x12\x12\n\nchannel_id\x18\x05 \x01(\x05\x12\x13\n\x0b\x63urrency_id\x18\x06 \x01(\x05\x12\x30\n\x0c\x63onfirm_date\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tclient_id\x18\x08 \x01(\x05\x12\x17\n\x0f\x62ill_address_id\x18\t \x01(\x05\x12\x12\n\ncountry_id\x18\n \x01(\x05\x12\x14\n\x0cwarehouse_id\x18\x0b \x01(\x05\x12\x12\n\njson_order\x18\x0c \x01(\t\x12\x10\n\x08state_id\x18\r \x01(\x05\x12\r\n\x05state\x18\x0e \x01(\t\x12*\n\x06\x61\x63tive\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x10 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xa1\x02\n\x0fSaleIntegration\x12.\n\rorder_details\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\toms_rules\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12/\n\x0e\x63lient_details\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x07payment\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0border_items\x18\x05 \x03(\x0b\x32\x17.google.protobuf.Struct\x12)\n\x08shipping\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct"\xff\x02\n\x11SaleCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12.\n\ndate_order\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06origin\x18\x03 \x01(\t\x12\x12\n\nchannel_id\x18\x04 \x01(\x05\x12\x13\n\x0b\x63urrency_id\x18\x05 \x01(\x05\x12\x30\n\x0c\x63onfirm_date\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tclient_id\x18\x07 \x01(\x05\x12\x17\n\x0f\x62ill_address_id\x18\x08 \x01(\x05\x12\x12\n\ncountry_id\x18\t \x01(\x05\x12\x14\n\x0cwarehouse_id\x18\n \x01(\x05\x12\x12\n\njson_order\x18\x0b \x01(\t\x12\x10\n\x08state_id\x18\x0c \x01(\x05\x12\r\n\x05state\x18\r \x01(\t\x12\x36\n\x07\x63ontext\x18\x0e \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x93\x01\n\x12SaleCreateResponse\x12\x32\n\x04sale\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.sale.Sale\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xed\x02\n\x0fSaleReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xcc\x01\n\x10SaleReadResponse\x12\x32\n\x04sale\x18\x01 \x03(\x0b\x32$.pro.omni.oms.api.v1.sales.sale.Sale\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x03 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData"\x7f\n\x11SaleUpdateRequest\x12\x32\n\x04sale\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.sale.Sale\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x93\x01\n\x12SaleUpdateResponse\x12\x32\n\x04sale\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.sale.Sale\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"W\n\x11SaleDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"_\n\x12SaleDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xa1\x01\n\x1cSaleCreateIntegrationRequest\x12I\n\x10sale_integration\x18\x01 \x01(\x0b\x32/.pro.omni.oms.api.v1.sales.sale.SaleIntegration\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9e\x01\n\x1dSaleCreateIntegrationResponse\x12\x32\n\x04sale\x18\x01 \x01(\x0b\x32$.pro.omni.oms.api.v1.sales.sale.Sale\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xfc\x04\n\x0bSaleService\x12u\n\nSaleCreate\x12\x31.pro.omni.oms.api.v1.sales.sale.SaleCreateRequest\x1a\x32.pro.omni.oms.api.v1.sales.sale.SaleCreateResponse"\x00\x12o\n\x08SaleRead\x12/.pro.omni.oms.api.v1.sales.sale.SaleReadRequest\x1a\x30.pro.omni.oms.api.v1.sales.sale.SaleReadResponse"\x00\x12u\n\nSaleUpdate\x12\x31.pro.omni.oms.api.v1.sales.sale.SaleUpdateRequest\x1a\x32.pro.omni.oms.api.v1.sales.sale.SaleUpdateResponse"\x00\x12u\n\nSaleDelete\x12\x31.pro.omni.oms.api.v1.sales.sale.SaleDeleteRequest\x1a\x32.pro.omni.oms.api.v1.sales.sale.SaleDeleteResponse"\x00\x12\x96\x01\n\x15SaleCreateIntegration\x12<.pro.omni.oms.api.v1.sales.sale.SaleCreateIntegrationRequest\x1a=.pro.omni.oms.api.v1.sales.sale.SaleCreateIntegrationResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.sales.sale_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_SALE"]._serialized_start = 170
    _globals["_SALE"]._serialized_end = 605
    _globals["_SALEINTEGRATION"]._serialized_start = 608
    _globals["_SALEINTEGRATION"]._serialized_end = 897
    _globals["_SALECREATEREQUEST"]._serialized_start = 900
    _globals["_SALECREATEREQUEST"]._serialized_end = 1283
    _globals["_SALECREATERESPONSE"]._serialized_start = 1286
    _globals["_SALECREATERESPONSE"]._serialized_end = 1433
    _globals["_SALEREADREQUEST"]._serialized_start = 1436
    _globals["_SALEREADREQUEST"]._serialized_end = 1801
    _globals["_SALEREADRESPONSE"]._serialized_start = 1804
    _globals["_SALEREADRESPONSE"]._serialized_end = 2008
    _globals["_SALEUPDATEREQUEST"]._serialized_start = 2010
    _globals["_SALEUPDATEREQUEST"]._serialized_end = 2137
    _globals["_SALEUPDATERESPONSE"]._serialized_start = 2140
    _globals["_SALEUPDATERESPONSE"]._serialized_end = 2287
    _globals["_SALEDELETEREQUEST"]._serialized_start = 2289
    _globals["_SALEDELETEREQUEST"]._serialized_end = 2376
    _globals["_SALEDELETERESPONSE"]._serialized_start = 2378
    _globals["_SALEDELETERESPONSE"]._serialized_end = 2473
    _globals["_SALECREATEINTEGRATIONREQUEST"]._serialized_start = 2476
    _globals["_SALECREATEINTEGRATIONREQUEST"]._serialized_end = 2637
    _globals["_SALECREATEINTEGRATIONRESPONSE"]._serialized_start = 2640
    _globals["_SALECREATEINTEGRATIONRESPONSE"]._serialized_end = 2798
    _globals["_SALESERVICE"]._serialized_start = 2801
    _globals["_SALESERVICE"]._serialized_end = 3437
# @@protoc_insertion_point(module_scope)
