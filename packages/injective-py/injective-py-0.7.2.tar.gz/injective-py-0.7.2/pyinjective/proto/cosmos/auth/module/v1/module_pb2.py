# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/auth/module/v1/module.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.app.v1alpha1 import module_pb2 as cosmos_dot_app_dot_v1alpha1_dot_module__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"cosmos/auth/module/v1/module.proto\x12\x15\x63osmos.auth.module.v1\x1a cosmos/app/v1alpha1/module.proto\"\xb3\x01\n\x06Module\x12\x15\n\rbech32_prefix\x18\x01 \x01(\t\x12R\n\x1amodule_account_permissions\x18\x02 \x03(\x0b\x32..cosmos.auth.module.v1.ModuleAccountPermission\x12\x11\n\tauthority\x18\x03 \x01(\t:+\xba\xc0\x96\xda\x01%\n#github.com/cosmos/cosmos-sdk/x/auth\"?\n\x17ModuleAccountPermission\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\x12\x13\n\x0bpermissions\x18\x02 \x03(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.auth.module.v1.module_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MODULE._options = None
  _MODULE._serialized_options = b'\272\300\226\332\001%\n#github.com/cosmos/cosmos-sdk/x/auth'
  _MODULE._serialized_start=96
  _MODULE._serialized_end=275
  _MODULEACCOUNTPERMISSION._serialized_start=277
  _MODULEACCOUNTPERMISSION._serialized_end=340
# @@protoc_insertion_point(module_scope)
