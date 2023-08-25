# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/staking/v1beta1/authz.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"cosmos/staking/v1beta1/authz.proto\x12\x16\x63osmos.staking.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x11\x61mino/amino.proto\"\xe1\x03\n\x12StakeAuthorization\x12Z\n\nmax_tokens\x18\x01 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB+\xaa\xdf\x1f\'github.com/cosmos/cosmos-sdk/types.Coin\x12K\n\nallow_list\x18\x02 \x01(\x0b\x32\x35.cosmos.staking.v1beta1.StakeAuthorization.ValidatorsH\x00\x12J\n\tdeny_list\x18\x03 \x01(\x0b\x32\x35.cosmos.staking.v1beta1.StakeAuthorization.ValidatorsH\x00\x12\x45\n\x12\x61uthorization_type\x18\x04 \x01(\x0e\x32).cosmos.staking.v1beta1.AuthorizationType\x1a\x37\n\nValidators\x12)\n\x07\x61\x64\x64ress\x18\x01 \x03(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString:H\xca\xb4-\"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*\x1d\x63osmos-sdk/StakeAuthorizationB\x0c\n\nvalidators*\x9e\x01\n\x11\x41uthorizationType\x12\"\n\x1e\x41UTHORIZATION_TYPE_UNSPECIFIED\x10\x00\x12\x1f\n\x1b\x41UTHORIZATION_TYPE_DELEGATE\x10\x01\x12!\n\x1d\x41UTHORIZATION_TYPE_UNDELEGATE\x10\x02\x12!\n\x1d\x41UTHORIZATION_TYPE_REDELEGATE\x10\x03\x42.Z,github.com/cosmos/cosmos-sdk/x/staking/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.staking.v1beta1.authz_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z,github.com/cosmos/cosmos-sdk/x/staking/types'
  _STAKEAUTHORIZATION_VALIDATORS.fields_by_name['address']._options = None
  _STAKEAUTHORIZATION_VALIDATORS.fields_by_name['address']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _STAKEAUTHORIZATION.fields_by_name['max_tokens']._options = None
  _STAKEAUTHORIZATION.fields_by_name['max_tokens']._serialized_options = b'\252\337\037\'github.com/cosmos/cosmos-sdk/types.Coin'
  _STAKEAUTHORIZATION._options = None
  _STAKEAUTHORIZATION._serialized_options = b'\312\264-\"cosmos.authz.v1beta1.Authorization\212\347\260*\035cosmos-sdk/StakeAuthorization'
  _AUTHORIZATIONTYPE._serialized_start=647
  _AUTHORIZATIONTYPE._serialized_end=805
  _STAKEAUTHORIZATION._serialized_start=163
  _STAKEAUTHORIZATION._serialized_end=644
  _STAKEAUTHORIZATION_VALIDATORS._serialized_start=501
  _STAKEAUTHORIZATION_VALIDATORS._serialized_end=556
# @@protoc_insertion_point(module_scope)
