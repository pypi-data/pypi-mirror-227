# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/msg/v1/msg.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x63osmos/msg/v1/msg.proto\x12\rcosmos.msg.v1\x1a google/protobuf/descriptor.proto:3\n\x07service\x12\x1f.google.protobuf.ServiceOptions\x18\xf0\x8c\xa6\x05 \x01(\x08:2\n\x06signer\x12\x1f.google.protobuf.MessageOptions\x18\xf0\x8c\xa6\x05 \x03(\tB/Z-github.com/cosmos/cosmos-sdk/types/msgserviceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.msg.v1.msg_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.ServiceOptions.RegisterExtension(service)
  google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(signer)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/cosmos/cosmos-sdk/types/msgservice'
# @@protoc_insertion_point(module_scope)
