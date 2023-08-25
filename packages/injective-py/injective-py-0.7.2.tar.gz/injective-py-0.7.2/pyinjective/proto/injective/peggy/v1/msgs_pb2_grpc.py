# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from injective.peggy.v1 import msgs_pb2 as injective_dot_peggy_dot_v1_dot_msgs__pb2


class MsgStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValsetConfirm = channel.unary_unary(
                '/injective.peggy.v1.Msg/ValsetConfirm',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirm.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirmResponse.FromString,
                )
        self.SendToEth = channel.unary_unary(
                '/injective.peggy.v1.Msg/SendToEth',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEth.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEthResponse.FromString,
                )
        self.RequestBatch = channel.unary_unary(
                '/injective.peggy.v1.Msg/RequestBatch',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatch.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatchResponse.FromString,
                )
        self.ConfirmBatch = channel.unary_unary(
                '/injective.peggy.v1.Msg/ConfirmBatch',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatch.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatchResponse.FromString,
                )
        self.DepositClaim = channel.unary_unary(
                '/injective.peggy.v1.Msg/DepositClaim',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaim.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaimResponse.FromString,
                )
        self.WithdrawClaim = channel.unary_unary(
                '/injective.peggy.v1.Msg/WithdrawClaim',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaim.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaimResponse.FromString,
                )
        self.ValsetUpdateClaim = channel.unary_unary(
                '/injective.peggy.v1.Msg/ValsetUpdateClaim',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaim.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaimResponse.FromString,
                )
        self.ERC20DeployedClaim = channel.unary_unary(
                '/injective.peggy.v1.Msg/ERC20DeployedClaim',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaim.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaimResponse.FromString,
                )
        self.SetOrchestratorAddresses = channel.unary_unary(
                '/injective.peggy.v1.Msg/SetOrchestratorAddresses',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddresses.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddressesResponse.FromString,
                )
        self.CancelSendToEth = channel.unary_unary(
                '/injective.peggy.v1.Msg/CancelSendToEth',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEth.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEthResponse.FromString,
                )
        self.SubmitBadSignatureEvidence = channel.unary_unary(
                '/injective.peggy.v1.Msg/SubmitBadSignatureEvidence',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidence.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidenceResponse.FromString,
                )
        self.UpdateParams = channel.unary_unary(
                '/injective.peggy.v1.Msg/UpdateParams',
                request_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParams.SerializeToString,
                response_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParamsResponse.FromString,
                )


class MsgServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ValsetConfirm(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendToEth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestBatch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmBatch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DepositClaim(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WithdrawClaim(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValsetUpdateClaim(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ERC20DeployedClaim(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOrchestratorAddresses(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelSendToEth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitBadSignatureEvidence(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateParams(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValsetConfirm': grpc.unary_unary_rpc_method_handler(
                    servicer.ValsetConfirm,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirm.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirmResponse.SerializeToString,
            ),
            'SendToEth': grpc.unary_unary_rpc_method_handler(
                    servicer.SendToEth,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEth.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEthResponse.SerializeToString,
            ),
            'RequestBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestBatch,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatch.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatchResponse.SerializeToString,
            ),
            'ConfirmBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmBatch,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatch.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatchResponse.SerializeToString,
            ),
            'DepositClaim': grpc.unary_unary_rpc_method_handler(
                    servicer.DepositClaim,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaim.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaimResponse.SerializeToString,
            ),
            'WithdrawClaim': grpc.unary_unary_rpc_method_handler(
                    servicer.WithdrawClaim,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaim.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaimResponse.SerializeToString,
            ),
            'ValsetUpdateClaim': grpc.unary_unary_rpc_method_handler(
                    servicer.ValsetUpdateClaim,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaim.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaimResponse.SerializeToString,
            ),
            'ERC20DeployedClaim': grpc.unary_unary_rpc_method_handler(
                    servicer.ERC20DeployedClaim,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaim.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaimResponse.SerializeToString,
            ),
            'SetOrchestratorAddresses': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOrchestratorAddresses,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddresses.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddressesResponse.SerializeToString,
            ),
            'CancelSendToEth': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelSendToEth,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEth.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEthResponse.SerializeToString,
            ),
            'SubmitBadSignatureEvidence': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitBadSignatureEvidence,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidence.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidenceResponse.SerializeToString,
            ),
            'UpdateParams': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateParams,
                    request_deserializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParams.FromString,
                    response_serializer=injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParamsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'injective.peggy.v1.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ValsetConfirm(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/ValsetConfirm',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirm.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetConfirmResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendToEth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/SendToEth',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEth.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSendToEthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/RequestBatch',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatch.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgRequestBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConfirmBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/ConfirmBatch',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatch.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgConfirmBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DepositClaim(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/DepositClaim',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaim.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgDepositClaimResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WithdrawClaim(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/WithdrawClaim',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaim.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgWithdrawClaimResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValsetUpdateClaim(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/ValsetUpdateClaim',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaim.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgValsetUpdatedClaimResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ERC20DeployedClaim(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/ERC20DeployedClaim',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaim.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgERC20DeployedClaimResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetOrchestratorAddresses(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/SetOrchestratorAddresses',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddresses.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSetOrchestratorAddressesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelSendToEth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/CancelSendToEth',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEth.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgCancelSendToEthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitBadSignatureEvidence(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/SubmitBadSignatureEvidence',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidence.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgSubmitBadSignatureEvidenceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateParams(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective.peggy.v1.Msg/UpdateParams',
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParams.SerializeToString,
            injective_dot_peggy_dot_v1_dot_msgs__pb2.MsgUpdateParamsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
