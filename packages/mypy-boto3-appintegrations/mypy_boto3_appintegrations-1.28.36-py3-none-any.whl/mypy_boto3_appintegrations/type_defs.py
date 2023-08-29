"""
Type annotations for appintegrations service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/type_defs/)

Usage::

    ```python
    from mypy_boto3_appintegrations.type_defs import FileConfigurationTypeDef

    data: FileConfigurationTypeDef = ...
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FileConfigurationTypeDef",
    "ScheduleConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "EventFilterTypeDef",
    "DataIntegrationAssociationSummaryTypeDef",
    "DataIntegrationSummaryTypeDef",
    "DeleteDataIntegrationRequestRequestTypeDef",
    "DeleteEventIntegrationRequestRequestTypeDef",
    "EventIntegrationAssociationTypeDef",
    "GetDataIntegrationRequestRequestTypeDef",
    "GetEventIntegrationRequestRequestTypeDef",
    "ListDataIntegrationAssociationsRequestRequestTypeDef",
    "ListDataIntegrationsRequestRequestTypeDef",
    "ListEventIntegrationAssociationsRequestRequestTypeDef",
    "ListEventIntegrationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDataIntegrationRequestRequestTypeDef",
    "UpdateEventIntegrationRequestRequestTypeDef",
    "CreateDataIntegrationRequestRequestTypeDef",
    "CreateDataIntegrationResponseTypeDef",
    "CreateEventIntegrationResponseTypeDef",
    "GetDataIntegrationResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateEventIntegrationRequestRequestTypeDef",
    "EventIntegrationTypeDef",
    "GetEventIntegrationResponseTypeDef",
    "ListDataIntegrationAssociationsResponseTypeDef",
    "ListDataIntegrationsResponseTypeDef",
    "ListEventIntegrationAssociationsResponseTypeDef",
    "ListEventIntegrationsResponseTypeDef",
)

FileConfigurationTypeDef = TypedDict(
    "FileConfigurationTypeDef",
    {
        "Folders": Sequence[str],
        "Filters": NotRequired[Mapping[str, Sequence[str]]],
    },
)

ScheduleConfigurationTypeDef = TypedDict(
    "ScheduleConfigurationTypeDef",
    {
        "ScheduleExpression": str,
        "FirstExecutionFrom": NotRequired[str],
        "Object": NotRequired[str],
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

EventFilterTypeDef = TypedDict(
    "EventFilterTypeDef",
    {
        "Source": str,
    },
)

DataIntegrationAssociationSummaryTypeDef = TypedDict(
    "DataIntegrationAssociationSummaryTypeDef",
    {
        "DataIntegrationAssociationArn": NotRequired[str],
        "DataIntegrationArn": NotRequired[str],
        "ClientId": NotRequired[str],
    },
)

DataIntegrationSummaryTypeDef = TypedDict(
    "DataIntegrationSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "SourceURI": NotRequired[str],
    },
)

DeleteDataIntegrationRequestRequestTypeDef = TypedDict(
    "DeleteDataIntegrationRequestRequestTypeDef",
    {
        "DataIntegrationIdentifier": str,
    },
)

DeleteEventIntegrationRequestRequestTypeDef = TypedDict(
    "DeleteEventIntegrationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

EventIntegrationAssociationTypeDef = TypedDict(
    "EventIntegrationAssociationTypeDef",
    {
        "EventIntegrationAssociationArn": NotRequired[str],
        "EventIntegrationAssociationId": NotRequired[str],
        "EventIntegrationName": NotRequired[str],
        "ClientId": NotRequired[str],
        "EventBridgeRuleName": NotRequired[str],
        "ClientAssociationMetadata": NotRequired[Dict[str, str]],
    },
)

GetDataIntegrationRequestRequestTypeDef = TypedDict(
    "GetDataIntegrationRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetEventIntegrationRequestRequestTypeDef = TypedDict(
    "GetEventIntegrationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ListDataIntegrationAssociationsRequestRequestTypeDef = TypedDict(
    "ListDataIntegrationAssociationsRequestRequestTypeDef",
    {
        "DataIntegrationIdentifier": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListDataIntegrationsRequestRequestTypeDef = TypedDict(
    "ListDataIntegrationsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListEventIntegrationAssociationsRequestRequestTypeDef = TypedDict(
    "ListEventIntegrationAssociationsRequestRequestTypeDef",
    {
        "EventIntegrationName": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListEventIntegrationsRequestRequestTypeDef = TypedDict(
    "ListEventIntegrationsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateDataIntegrationRequestRequestTypeDef = TypedDict(
    "UpdateDataIntegrationRequestRequestTypeDef",
    {
        "Identifier": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)

UpdateEventIntegrationRequestRequestTypeDef = TypedDict(
    "UpdateEventIntegrationRequestRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
    },
)

CreateDataIntegrationRequestRequestTypeDef = TypedDict(
    "CreateDataIntegrationRequestRequestTypeDef",
    {
        "Name": str,
        "KmsKey": str,
        "SourceURI": str,
        "ScheduleConfig": ScheduleConfigurationTypeDef,
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "ClientToken": NotRequired[str],
        "FileConfiguration": NotRequired[FileConfigurationTypeDef],
        "ObjectConfiguration": NotRequired[Mapping[str, Mapping[str, Sequence[str]]]],
    },
)

CreateDataIntegrationResponseTypeDef = TypedDict(
    "CreateDataIntegrationResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "KmsKey": str,
        "SourceURI": str,
        "ScheduleConfiguration": ScheduleConfigurationTypeDef,
        "Tags": Dict[str, str],
        "ClientToken": str,
        "FileConfiguration": FileConfigurationTypeDef,
        "ObjectConfiguration": Dict[str, Dict[str, List[str]]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEventIntegrationResponseTypeDef = TypedDict(
    "CreateEventIntegrationResponseTypeDef",
    {
        "EventIntegrationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataIntegrationResponseTypeDef = TypedDict(
    "GetDataIntegrationResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "KmsKey": str,
        "SourceURI": str,
        "ScheduleConfiguration": ScheduleConfigurationTypeDef,
        "Tags": Dict[str, str],
        "FileConfiguration": FileConfigurationTypeDef,
        "ObjectConfiguration": Dict[str, Dict[str, List[str]]],
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

CreateEventIntegrationRequestRequestTypeDef = TypedDict(
    "CreateEventIntegrationRequestRequestTypeDef",
    {
        "Name": str,
        "EventFilter": EventFilterTypeDef,
        "EventBridgeBus": str,
        "Description": NotRequired[str],
        "ClientToken": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

EventIntegrationTypeDef = TypedDict(
    "EventIntegrationTypeDef",
    {
        "EventIntegrationArn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "EventFilter": NotRequired[EventFilterTypeDef],
        "EventBridgeBus": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
    },
)

GetEventIntegrationResponseTypeDef = TypedDict(
    "GetEventIntegrationResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "EventIntegrationArn": str,
        "EventBridgeBus": str,
        "EventFilter": EventFilterTypeDef,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataIntegrationAssociationsResponseTypeDef = TypedDict(
    "ListDataIntegrationAssociationsResponseTypeDef",
    {
        "DataIntegrationAssociations": List[DataIntegrationAssociationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataIntegrationsResponseTypeDef = TypedDict(
    "ListDataIntegrationsResponseTypeDef",
    {
        "DataIntegrations": List[DataIntegrationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventIntegrationAssociationsResponseTypeDef = TypedDict(
    "ListEventIntegrationAssociationsResponseTypeDef",
    {
        "EventIntegrationAssociations": List[EventIntegrationAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventIntegrationsResponseTypeDef = TypedDict(
    "ListEventIntegrationsResponseTypeDef",
    {
        "EventIntegrations": List[EventIntegrationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
