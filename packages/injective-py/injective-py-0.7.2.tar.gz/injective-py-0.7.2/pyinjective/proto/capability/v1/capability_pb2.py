# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: capability/v1/capability.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x63\x61pability/v1/capability.proto\x12\rcapability.v1\x1a\x14gogoproto/gogo.proto\x1a\x11\x61mino/amino.proto\"!\n\nCapability\x12\r\n\x05index\x18\x01 \x01(\x04:\x04\x98\xa0\x1f\x00\"/\n\x05Owner\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t:\x08\x98\xa0\x1f\x00\x88\xa0\x1f\x00\"C\n\x10\x43\x61pabilityOwners\x12/\n\x06owners\x18\x01 \x03(\x0b\x32\x14.capability.v1.OwnerB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x42\x33Z1github.com/cosmos/ibc-go/modules/capability/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'capability.v1.capability_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/cosmos/ibc-go/modules/capability/types'
  _CAPABILITY._options = None
  _CAPABILITY._serialized_options = b'\230\240\037\000'
  _OWNER._options = None
  _OWNER._serialized_options = b'\230\240\037\000\210\240\037\000'
  _CAPABILITYOWNERS.fields_by_name['owners']._options = None
  _CAPABILITYOWNERS.fields_by_name['owners']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _CAPABILITY._serialized_start=90
  _CAPABILITY._serialized_end=123
  _OWNER._serialized_start=125
  _OWNER._serialized_end=172
  _CAPABILITYOWNERS._serialized_start=174
  _CAPABILITYOWNERS._serialized_end=241
# @@protoc_insertion_point(module_scope)
