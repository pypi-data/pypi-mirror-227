# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: injective/ocr/v1beta1/genesis.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from injective.ocr.v1beta1 import ocr_pb2 as injective_dot_ocr_dot_v1beta1_dot_ocr__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#injective/ocr/v1beta1/genesis.proto\x12\x15injective.ocr.v1beta1\x1a\x1finjective/ocr/v1beta1/ocr.proto\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\"\xed\x04\n\x0cGenesisState\x12\x33\n\x06params\x18\x01 \x01(\x0b\x32\x1d.injective.ocr.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\x12\x37\n\x0c\x66\x65\x65\x64_configs\x18\x02 \x03(\x0b\x32!.injective.ocr.v1beta1.FeedConfig\x12I\n\x17latest_epoch_and_rounds\x18\x03 \x03(\x0b\x32(.injective.ocr.v1beta1.FeedEpochAndRound\x12\x43\n\x12\x66\x65\x65\x64_transmissions\x18\x04 \x03(\x0b\x32\'.injective.ocr.v1beta1.FeedTransmission\x12X\n\x1blatest_aggregator_round_ids\x18\x05 \x03(\x0b\x32\x33.injective.ocr.v1beta1.FeedLatestAggregatorRoundIDs\x12\x37\n\x0creward_pools\x18\x06 \x03(\x0b\x32!.injective.ocr.v1beta1.RewardPool\x12\x42\n\x17\x66\x65\x65\x64_observation_counts\x18\x07 \x03(\x0b\x32!.injective.ocr.v1beta1.FeedCounts\x12\x43\n\x18\x66\x65\x65\x64_transmission_counts\x18\x08 \x03(\x0b\x32!.injective.ocr.v1beta1.FeedCounts\x12\x43\n\x12pending_payeeships\x18\t \x03(\x0b\x32\'.injective.ocr.v1beta1.PendingPayeeship\"^\n\x10\x46\x65\x65\x64Transmission\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12\x39\n\x0ctransmission\x18\x02 \x01(\x0b\x32#.injective.ocr.v1beta1.Transmission\"c\n\x11\x46\x65\x65\x64\x45pochAndRound\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12=\n\x0f\x65poch_and_round\x18\x02 \x01(\x0b\x32$.injective.ocr.v1beta1.EpochAndRound\"L\n\x1c\x46\x65\x65\x64LatestAggregatorRoundIDs\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12\x1b\n\x13\x61ggregator_round_id\x18\x02 \x01(\x04\"N\n\nRewardPool\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12/\n\x06\x61mount\x18\x02 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\"K\n\nFeedCounts\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12,\n\x06\x63ounts\x18\x02 \x03(\x0b\x32\x1c.injective.ocr.v1beta1.Count\"\'\n\x05\x43ount\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\"P\n\x10PendingPayeeship\x12\x0f\n\x07\x66\x65\x65\x64_id\x18\x01 \x01(\t\x12\x13\n\x0btransmitter\x18\x02 \x01(\t\x12\x16\n\x0eproposed_payee\x18\x03 \x01(\tBKZIgithub.com/InjectiveLabs/injective-core/injective-chain/modules/ocr/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'injective.ocr.v1beta1.genesis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZIgithub.com/InjectiveLabs/injective-core/injective-chain/modules/ocr/types'
  _GENESISSTATE.fields_by_name['params']._options = None
  _GENESISSTATE.fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _REWARDPOOL.fields_by_name['amount']._options = None
  _REWARDPOOL.fields_by_name['amount']._serialized_options = b'\310\336\037\000'
  _GENESISSTATE._serialized_start=150
  _GENESISSTATE._serialized_end=771
  _FEEDTRANSMISSION._serialized_start=773
  _FEEDTRANSMISSION._serialized_end=867
  _FEEDEPOCHANDROUND._serialized_start=869
  _FEEDEPOCHANDROUND._serialized_end=968
  _FEEDLATESTAGGREGATORROUNDIDS._serialized_start=970
  _FEEDLATESTAGGREGATORROUNDIDS._serialized_end=1046
  _REWARDPOOL._serialized_start=1048
  _REWARDPOOL._serialized_end=1126
  _FEEDCOUNTS._serialized_start=1128
  _FEEDCOUNTS._serialized_end=1203
  _COUNT._serialized_start=1205
  _COUNT._serialized_end=1244
  _PENDINGPAYEESHIP._serialized_start=1246
  _PENDINGPAYEESHIP._serialized_end=1326
# @@protoc_insertion_point(module_scope)
