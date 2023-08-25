# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/slashing/v1beta1/query.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from cosmos.slashing.v1beta1 import slashing_pb2 as cosmos_dot_slashing_dot_v1beta1_dot_slashing__pb2
from cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#cosmos/slashing/v1beta1/query.proto\x12\x17\x63osmos.slashing.v1beta1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a&cosmos/slashing/v1beta1/slashing.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x11\x61mino/amino.proto\"\x14\n\x12QueryParamsRequest\"Q\n\x13QueryParamsResponse\x12:\n\x06params\x18\x01 \x01(\x0b\x32\x1f.cosmos.slashing.v1beta1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\"I\n\x17QuerySigningInfoRequest\x12.\n\x0c\x63ons_address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\"n\n\x18QuerySigningInfoResponse\x12R\n\x10val_signing_info\x18\x01 \x01(\x0b\x32-.cosmos.slashing.v1beta1.ValidatorSigningInfoB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\"V\n\x18QuerySigningInfosRequest\x12:\n\npagination\x18\x01 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\xa0\x01\n\x19QuerySigningInfosResponse\x12\x46\n\x04info\x18\x01 \x03(\x0b\x32-.cosmos.slashing.v1beta1.ValidatorSigningInfoB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse2\xf2\x03\n\x05Query\x12\x8c\x01\n\x06Params\x12+.cosmos.slashing.v1beta1.QueryParamsRequest\x1a,.cosmos.slashing.v1beta1.QueryParamsResponse\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/cosmos/slashing/v1beta1/params\x12\xb1\x01\n\x0bSigningInfo\x12\x30.cosmos.slashing.v1beta1.QuerySigningInfoRequest\x1a\x31.cosmos.slashing.v1beta1.QuerySigningInfoResponse\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/cosmos/slashing/v1beta1/signing_infos/{cons_address}\x12\xa5\x01\n\x0cSigningInfos\x12\x31.cosmos.slashing.v1beta1.QuerySigningInfosRequest\x1a\x32.cosmos.slashing.v1beta1.QuerySigningInfosResponse\".\x82\xd3\xe4\x93\x02(\x12&/cosmos/slashing/v1beta1/signing_infosB/Z-github.com/cosmos/cosmos-sdk/x/slashing/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.slashing.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/cosmos/cosmos-sdk/x/slashing/types'
  _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
  _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _QUERYSIGNINGINFOREQUEST.fields_by_name['cons_address']._options = None
  _QUERYSIGNINGINFOREQUEST.fields_by_name['cons_address']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _QUERYSIGNINGINFORESPONSE.fields_by_name['val_signing_info']._options = None
  _QUERYSIGNINGINFORESPONSE.fields_by_name['val_signing_info']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _QUERYSIGNINGINFOSRESPONSE.fields_by_name['info']._options = None
  _QUERYSIGNINGINFOSRESPONSE.fields_by_name['info']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _QUERY.methods_by_name['Params']._options = None
  _QUERY.methods_by_name['Params']._serialized_options = b'\202\323\344\223\002!\022\037/cosmos/slashing/v1beta1/params'
  _QUERY.methods_by_name['SigningInfo']._options = None
  _QUERY.methods_by_name['SigningInfo']._serialized_options = b'\202\323\344\223\0027\0225/cosmos/slashing/v1beta1/signing_infos/{cons_address}'
  _QUERY.methods_by_name['SigningInfos']._options = None
  _QUERY.methods_by_name['SigningInfos']._serialized_options = b'\202\323\344\223\002(\022&/cosmos/slashing/v1beta1/signing_infos'
  _QUERYPARAMSREQUEST._serialized_start=246
  _QUERYPARAMSREQUEST._serialized_end=266
  _QUERYPARAMSRESPONSE._serialized_start=268
  _QUERYPARAMSRESPONSE._serialized_end=349
  _QUERYSIGNINGINFOREQUEST._serialized_start=351
  _QUERYSIGNINGINFOREQUEST._serialized_end=424
  _QUERYSIGNINGINFORESPONSE._serialized_start=426
  _QUERYSIGNINGINFORESPONSE._serialized_end=536
  _QUERYSIGNINGINFOSREQUEST._serialized_start=538
  _QUERYSIGNINGINFOSREQUEST._serialized_end=624
  _QUERYSIGNINGINFOSRESPONSE._serialized_start=627
  _QUERYSIGNINGINFOSRESPONSE._serialized_end=787
  _QUERY._serialized_start=790
  _QUERY._serialized_end=1288
# @@protoc_insertion_point(module_scope)
