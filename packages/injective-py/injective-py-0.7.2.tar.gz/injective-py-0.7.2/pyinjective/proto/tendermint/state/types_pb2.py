# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tendermint/state/types.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from tendermint.abci import types_pb2 as tendermint_dot_abci_dot_types__pb2
from tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from tendermint.types import validator_pb2 as tendermint_dot_types_dot_validator__pb2
from tendermint.types import params_pb2 as tendermint_dot_types_dot_params__pb2
from tendermint.version import types_pb2 as tendermint_dot_version_dot_types__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ctendermint/state/types.proto\x12\x10tendermint.state\x1a\x14gogoproto/gogo.proto\x1a\x1btendermint/abci/types.proto\x1a\x1ctendermint/types/types.proto\x1a tendermint/types/validator.proto\x1a\x1dtendermint/types/params.proto\x1a\x1etendermint/version/types.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xbb\x01\n\x13LegacyABCIResponses\x12\x32\n\x0b\x64\x65liver_txs\x18\x01 \x03(\x0b\x32\x1d.tendermint.abci.ExecTxResult\x12\x35\n\tend_block\x18\x02 \x01(\x0b\x32\".tendermint.state.ResponseEndBlock\x12\x39\n\x0b\x62\x65gin_block\x18\x03 \x01(\x0b\x32$.tendermint.state.ResponseBeginBlock\"V\n\x12ResponseBeginBlock\x12@\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10\x65vents,omitempty\"\xdb\x01\n\x10ResponseEndBlock\x12\x41\n\x11validator_updates\x18\x01 \x03(\x0b\x32 .tendermint.abci.ValidatorUpdateB\x04\xc8\xde\x1f\x00\x12\x42\n\x17\x63onsensus_param_updates\x18\x02 \x01(\x0b\x32!.tendermint.types.ConsensusParams\x12@\n\x06\x65vents\x18\x03 \x03(\x0b\x32\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10\x65vents,omitempty\"d\n\x0eValidatorsInfo\x12\x35\n\rvalidator_set\x18\x01 \x01(\x0b\x32\x1e.tendermint.types.ValidatorSet\x12\x1b\n\x13last_height_changed\x18\x02 \x01(\x03\"u\n\x13\x43onsensusParamsInfo\x12\x41\n\x10\x63onsensus_params\x18\x01 \x01(\x0b\x32!.tendermint.types.ConsensusParamsB\x04\xc8\xde\x1f\x00\x12\x1b\n\x13last_height_changed\x18\x02 \x01(\x03\"\xb2\x01\n\x11\x41\x42\x43IResponsesInfo\x12\x44\n\x15legacy_abci_responses\x18\x01 \x01(\x0b\x32%.tendermint.state.LegacyABCIResponses\x12\x0e\n\x06height\x18\x02 \x01(\x03\x12G\n\x17response_finalize_block\x18\x03 \x01(\x0b\x32&.tendermint.abci.ResponseFinalizeBlock\"S\n\x07Version\x12\x36\n\tconsensus\x18\x01 \x01(\x0b\x32\x1d.tendermint.version.ConsensusB\x04\xc8\xde\x1f\x00\x12\x10\n\x08software\x18\x02 \x01(\t\"\xfd\x04\n\x05State\x12\x30\n\x07version\x18\x01 \x01(\x0b\x32\x19.tendermint.state.VersionB\x04\xc8\xde\x1f\x00\x12\x1d\n\x08\x63hain_id\x18\x02 \x01(\tB\x0b\xe2\xde\x1f\x07\x43hainID\x12\x16\n\x0einitial_height\x18\x0e \x01(\x03\x12\x19\n\x11last_block_height\x18\x03 \x01(\x03\x12\x45\n\rlast_block_id\x18\x04 \x01(\x0b\x32\x19.tendermint.types.BlockIDB\x13\xc8\xde\x1f\x00\xe2\xde\x1f\x0bLastBlockID\x12=\n\x0flast_block_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12\x37\n\x0fnext_validators\x18\x06 \x01(\x0b\x32\x1e.tendermint.types.ValidatorSet\x12\x32\n\nvalidators\x18\x07 \x01(\x0b\x32\x1e.tendermint.types.ValidatorSet\x12\x37\n\x0flast_validators\x18\x08 \x01(\x0b\x32\x1e.tendermint.types.ValidatorSet\x12&\n\x1elast_height_validators_changed\x18\t \x01(\x03\x12\x41\n\x10\x63onsensus_params\x18\n \x01(\x0b\x32!.tendermint.types.ConsensusParamsB\x04\xc8\xde\x1f\x00\x12,\n$last_height_consensus_params_changed\x18\x0b \x01(\x03\x12\x19\n\x11last_results_hash\x18\x0c \x01(\x0c\x12\x10\n\x08\x61pp_hash\x18\r \x01(\x0c\x42\x35Z3github.com/cometbft/cometbft/proto/tendermint/stateb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tendermint.state.types_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/cometbft/cometbft/proto/tendermint/state'
  _RESPONSEBEGINBLOCK.fields_by_name['events']._options = None
  _RESPONSEBEGINBLOCK.fields_by_name['events']._serialized_options = b'\310\336\037\000\352\336\037\020events,omitempty'
  _RESPONSEENDBLOCK.fields_by_name['validator_updates']._options = None
  _RESPONSEENDBLOCK.fields_by_name['validator_updates']._serialized_options = b'\310\336\037\000'
  _RESPONSEENDBLOCK.fields_by_name['events']._options = None
  _RESPONSEENDBLOCK.fields_by_name['events']._serialized_options = b'\310\336\037\000\352\336\037\020events,omitempty'
  _CONSENSUSPARAMSINFO.fields_by_name['consensus_params']._options = None
  _CONSENSUSPARAMSINFO.fields_by_name['consensus_params']._serialized_options = b'\310\336\037\000'
  _VERSION.fields_by_name['consensus']._options = None
  _VERSION.fields_by_name['consensus']._serialized_options = b'\310\336\037\000'
  _STATE.fields_by_name['version']._options = None
  _STATE.fields_by_name['version']._serialized_options = b'\310\336\037\000'
  _STATE.fields_by_name['chain_id']._options = None
  _STATE.fields_by_name['chain_id']._serialized_options = b'\342\336\037\007ChainID'
  _STATE.fields_by_name['last_block_id']._options = None
  _STATE.fields_by_name['last_block_id']._serialized_options = b'\310\336\037\000\342\336\037\013LastBlockID'
  _STATE.fields_by_name['last_block_time']._options = None
  _STATE.fields_by_name['last_block_time']._serialized_options = b'\310\336\037\000\220\337\037\001'
  _STATE.fields_by_name['consensus_params']._options = None
  _STATE.fields_by_name['consensus_params']._serialized_options = b'\310\336\037\000'
  _LEGACYABCIRESPONSES._serialized_start=262
  _LEGACYABCIRESPONSES._serialized_end=449
  _RESPONSEBEGINBLOCK._serialized_start=451
  _RESPONSEBEGINBLOCK._serialized_end=537
  _RESPONSEENDBLOCK._serialized_start=540
  _RESPONSEENDBLOCK._serialized_end=759
  _VALIDATORSINFO._serialized_start=761
  _VALIDATORSINFO._serialized_end=861
  _CONSENSUSPARAMSINFO._serialized_start=863
  _CONSENSUSPARAMSINFO._serialized_end=980
  _ABCIRESPONSESINFO._serialized_start=983
  _ABCIRESPONSESINFO._serialized_end=1161
  _VERSION._serialized_start=1163
  _VERSION._serialized_end=1246
  _STATE._serialized_start=1249
  _STATE._serialized_end=1886
# @@protoc_insertion_point(module_scope)
