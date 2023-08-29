"""
Type annotations for connectcampaigns service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectcampaigns.type_defs import AnswerMachineDetectionConfigTypeDef

    data: AnswerMachineDetectionConfigTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CampaignStateType,
    FailureCodeType,
    GetCampaignStateBatchFailureCodeType,
    InstanceOnboardingJobFailureCodeType,
    InstanceOnboardingJobStatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AnswerMachineDetectionConfigTypeDef",
    "InstanceIdFilterTypeDef",
    "CampaignSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "TimestampTypeDef",
    "PredictiveDialerConfigTypeDef",
    "ProgressiveDialerConfigTypeDef",
    "EncryptionConfigTypeDef",
    "FailedCampaignStateResponseTypeDef",
    "FailedRequestTypeDef",
    "GetCampaignStateBatchRequestRequestTypeDef",
    "SuccessfulCampaignStateResponseTypeDef",
    "GetCampaignStateRequestRequestTypeDef",
    "GetConnectInstanceConfigRequestRequestTypeDef",
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    "InstanceOnboardingJobStatusTypeDef",
    "PaginatorConfigTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PauseCampaignRequestRequestTypeDef",
    "SuccessfulRequestTypeDef",
    "ResumeCampaignRequestRequestTypeDef",
    "StartCampaignRequestRequestTypeDef",
    "StopCampaignRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignNameRequestRequestTypeDef",
    "OutboundCallConfigTypeDef",
    "UpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    "CampaignFiltersTypeDef",
    "CreateCampaignResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCampaignStateResponseTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DialRequestTypeDef",
    "DialerConfigTypeDef",
    "InstanceConfigTypeDef",
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    "GetCampaignStateBatchResponseTypeDef",
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    "StartInstanceOnboardingJobResponseTypeDef",
    "PutDialRequestBatchResponseTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "PutDialRequestBatchRequestRequestTypeDef",
    "CampaignTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    "GetConnectInstanceConfigResponseTypeDef",
    "DescribeCampaignResponseTypeDef",
)

AnswerMachineDetectionConfigTypeDef = TypedDict(
    "AnswerMachineDetectionConfigTypeDef",
    {
        "enableAnswerMachineDetection": bool,
    },
)

InstanceIdFilterTypeDef = TypedDict(
    "InstanceIdFilterTypeDef",
    {
        "operator": Literal["Eq"],
        "value": str,
    },
)

CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "arn": str,
        "connectInstanceId": str,
        "id": str,
        "name": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteConnectInstanceConfigRequestRequestTypeDef = TypedDict(
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

DeleteInstanceOnboardingJobRequestRequestTypeDef = TypedDict(
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

DescribeCampaignRequestRequestTypeDef = TypedDict(
    "DescribeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

TimestampTypeDef = Union[datetime, str]
PredictiveDialerConfigTypeDef = TypedDict(
    "PredictiveDialerConfigTypeDef",
    {
        "bandwidthAllocation": float,
    },
)

ProgressiveDialerConfigTypeDef = TypedDict(
    "ProgressiveDialerConfigTypeDef",
    {
        "bandwidthAllocation": float,
    },
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "enabled": bool,
        "encryptionType": NotRequired[Literal["KMS"]],
        "keyArn": NotRequired[str],
    },
)

FailedCampaignStateResponseTypeDef = TypedDict(
    "FailedCampaignStateResponseTypeDef",
    {
        "campaignId": NotRequired[str],
        "failureCode": NotRequired[GetCampaignStateBatchFailureCodeType],
    },
)

FailedRequestTypeDef = TypedDict(
    "FailedRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "failureCode": NotRequired[FailureCodeType],
        "id": NotRequired[str],
    },
)

GetCampaignStateBatchRequestRequestTypeDef = TypedDict(
    "GetCampaignStateBatchRequestRequestTypeDef",
    {
        "campaignIds": Sequence[str],
    },
)

SuccessfulCampaignStateResponseTypeDef = TypedDict(
    "SuccessfulCampaignStateResponseTypeDef",
    {
        "campaignId": NotRequired[str],
        "state": NotRequired[CampaignStateType],
    },
)

GetCampaignStateRequestRequestTypeDef = TypedDict(
    "GetCampaignStateRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetConnectInstanceConfigRequestRequestTypeDef = TypedDict(
    "GetConnectInstanceConfigRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

GetInstanceOnboardingJobStatusRequestRequestTypeDef = TypedDict(
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

InstanceOnboardingJobStatusTypeDef = TypedDict(
    "InstanceOnboardingJobStatusTypeDef",
    {
        "connectInstanceId": str,
        "status": InstanceOnboardingJobStatusCodeType,
        "failureCode": NotRequired[InstanceOnboardingJobFailureCodeType],
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "arn": str,
    },
)

PauseCampaignRequestRequestTypeDef = TypedDict(
    "PauseCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

SuccessfulRequestTypeDef = TypedDict(
    "SuccessfulRequestTypeDef",
    {
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
    },
)

ResumeCampaignRequestRequestTypeDef = TypedDict(
    "ResumeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

StartCampaignRequestRequestTypeDef = TypedDict(
    "StartCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

StopCampaignRequestRequestTypeDef = TypedDict(
    "StopCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateCampaignNameRequestRequestTypeDef = TypedDict(
    "UpdateCampaignNameRequestRequestTypeDef",
    {
        "id": str,
        "name": str,
    },
)

OutboundCallConfigTypeDef = TypedDict(
    "OutboundCallConfigTypeDef",
    {
        "connectContactFlowId": str,
        "connectQueueId": str,
        "answerMachineDetectionConfig": NotRequired[AnswerMachineDetectionConfigTypeDef],
        "connectSourcePhoneNumber": NotRequired[str],
    },
)

UpdateCampaignOutboundCallConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    {
        "id": str,
        "answerMachineDetectionConfig": NotRequired[AnswerMachineDetectionConfigTypeDef],
        "connectContactFlowId": NotRequired[str],
        "connectSourcePhoneNumber": NotRequired[str],
    },
)

CampaignFiltersTypeDef = TypedDict(
    "CampaignFiltersTypeDef",
    {
        "instanceIdFilter": NotRequired[InstanceIdFilterTypeDef],
    },
)

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignStateResponseTypeDef = TypedDict(
    "GetCampaignStateResponseTypeDef",
    {
        "state": CampaignStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCampaignsResponseTypeDef = TypedDict(
    "ListCampaignsResponseTypeDef",
    {
        "campaignSummaryList": List[CampaignSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DialRequestTypeDef = TypedDict(
    "DialRequestTypeDef",
    {
        "attributes": Mapping[str, str],
        "clientToken": str,
        "expirationTime": TimestampTypeDef,
        "phoneNumber": str,
    },
)

DialerConfigTypeDef = TypedDict(
    "DialerConfigTypeDef",
    {
        "predictiveDialerConfig": NotRequired[PredictiveDialerConfigTypeDef],
        "progressiveDialerConfig": NotRequired[ProgressiveDialerConfigTypeDef],
    },
)

InstanceConfigTypeDef = TypedDict(
    "InstanceConfigTypeDef",
    {
        "connectInstanceId": str,
        "encryptionConfig": EncryptionConfigTypeDef,
        "serviceLinkedRoleArn": str,
    },
)

StartInstanceOnboardingJobRequestRequestTypeDef = TypedDict(
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    {
        "connectInstanceId": str,
        "encryptionConfig": EncryptionConfigTypeDef,
    },
)

GetCampaignStateBatchResponseTypeDef = TypedDict(
    "GetCampaignStateBatchResponseTypeDef",
    {
        "failedRequests": List[FailedCampaignStateResponseTypeDef],
        "successfulRequests": List[SuccessfulCampaignStateResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInstanceOnboardingJobStatusResponseTypeDef = TypedDict(
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    {
        "connectInstanceOnboardingJobStatus": InstanceOnboardingJobStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartInstanceOnboardingJobResponseTypeDef = TypedDict(
    "StartInstanceOnboardingJobResponseTypeDef",
    {
        "connectInstanceOnboardingJobStatus": InstanceOnboardingJobStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDialRequestBatchResponseTypeDef = TypedDict(
    "PutDialRequestBatchResponseTypeDef",
    {
        "failedRequests": List[FailedRequestTypeDef],
        "successfulRequests": List[SuccessfulRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCampaignsRequestListCampaignsPaginateTypeDef = TypedDict(
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    {
        "filters": NotRequired[CampaignFiltersTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCampaignsRequestRequestTypeDef = TypedDict(
    "ListCampaignsRequestRequestTypeDef",
    {
        "filters": NotRequired[CampaignFiltersTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

PutDialRequestBatchRequestRequestTypeDef = TypedDict(
    "PutDialRequestBatchRequestRequestTypeDef",
    {
        "dialRequests": Sequence[DialRequestTypeDef],
        "id": str,
    },
)

CampaignTypeDef = TypedDict(
    "CampaignTypeDef",
    {
        "arn": str,
        "connectInstanceId": str,
        "dialerConfig": DialerConfigTypeDef,
        "id": str,
        "name": str,
        "outboundCallConfig": OutboundCallConfigTypeDef,
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateCampaignRequestRequestTypeDef = TypedDict(
    "CreateCampaignRequestRequestTypeDef",
    {
        "connectInstanceId": str,
        "dialerConfig": DialerConfigTypeDef,
        "name": str,
        "outboundCallConfig": OutboundCallConfigTypeDef,
        "tags": NotRequired[Mapping[str, str]],
    },
)

UpdateCampaignDialerConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    {
        "dialerConfig": DialerConfigTypeDef,
        "id": str,
    },
)

GetConnectInstanceConfigResponseTypeDef = TypedDict(
    "GetConnectInstanceConfigResponseTypeDef",
    {
        "connectInstanceConfig": InstanceConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCampaignResponseTypeDef = TypedDict(
    "DescribeCampaignResponseTypeDef",
    {
        "campaign": CampaignTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
