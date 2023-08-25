"""
Type annotations for mediatailor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediatailor.type_defs import SecretsManagerAccessTokenConfigurationTypeDef

    data: SecretsManagerAccessTokenConfigurationTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessTypeType,
    AdMarkupTypeType,
    AlertCategoryType,
    ChannelStateType,
    FillPolicyType,
    MessageTypeType,
    ModeType,
    OriginManifestTypeType,
    PlaybackModeType,
    RelativePositionType,
    ScheduleEntryTypeType,
    TierType,
    TypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "SecretsManagerAccessTokenConfigurationTypeDef",
    "KeyValuePairTypeDef",
    "SlateSourceTypeDef",
    "SpliceInsertMessageTypeDef",
    "AdMarkerPassthroughTypeDef",
    "AlertTypeDef",
    "AvailMatchingCriteriaTypeDef",
    "AvailSuppressionTypeDef",
    "BumperTypeDef",
    "CdnConfigurationTypeDef",
    "LogConfigurationForChannelTypeDef",
    "ClipRangeTypeDef",
    "ConfigureLogsForChannelRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef",
    "HttpPackageConfigurationTypeDef",
    "DefaultSegmentDeliveryConfigurationTypeDef",
    "HttpConfigurationTypeDef",
    "SegmentDeliveryConfigurationTypeDef",
    "DashConfigurationForPutTypeDef",
    "DashConfigurationTypeDef",
    "DashPlaylistSettingsTypeDef",
    "DeleteChannelPolicyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteLiveSourceRequestRequestTypeDef",
    "DeletePlaybackConfigurationRequestRequestTypeDef",
    "DeletePrefetchScheduleRequestRequestTypeDef",
    "DeleteProgramRequestRequestTypeDef",
    "DeleteSourceLocationRequestRequestTypeDef",
    "DeleteVodSourceRequestRequestTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeLiveSourceRequestRequestTypeDef",
    "DescribeProgramRequestRequestTypeDef",
    "DescribeSourceLocationRequestRequestTypeDef",
    "DescribeVodSourceRequestRequestTypeDef",
    "GetChannelPolicyRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetChannelScheduleRequestRequestTypeDef",
    "GetPlaybackConfigurationRequestRequestTypeDef",
    "HlsConfigurationTypeDef",
    "LivePreRollConfigurationTypeDef",
    "LogConfigurationTypeDef",
    "GetPrefetchScheduleRequestRequestTypeDef",
    "HlsPlaylistSettingsPaginatorTypeDef",
    "HlsPlaylistSettingsTypeDef",
    "ListAlertsRequestRequestTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListLiveSourcesRequestRequestTypeDef",
    "ListPlaybackConfigurationsRequestRequestTypeDef",
    "ListPrefetchSchedulesRequestRequestTypeDef",
    "ListSourceLocationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVodSourcesRequestRequestTypeDef",
    "TimestampTypeDef",
    "PrefetchRetrievalPaginatorTypeDef",
    "PutChannelPolicyRequestRequestTypeDef",
    "ScheduleAdBreakTypeDef",
    "TransitionTypeDef",
    "SegmentationDescriptorTypeDef",
    "StartChannelRequestRequestTypeDef",
    "StopChannelRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateProgramTransitionTypeDef",
    "AccessConfigurationTypeDef",
    "ManifestProcessingRulesTypeDef",
    "PrefetchConsumptionPaginatorTypeDef",
    "ConfigureLogsForChannelResponseTypeDef",
    "ConfigureLogsForPlaybackConfigurationResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "ListAlertsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateLiveSourceRequestRequestTypeDef",
    "CreateLiveSourceResponseTypeDef",
    "CreateVodSourceRequestRequestTypeDef",
    "CreateVodSourceResponseTypeDef",
    "DescribeLiveSourceResponseTypeDef",
    "DescribeVodSourceResponseTypeDef",
    "LiveSourceTypeDef",
    "UpdateLiveSourceRequestRequestTypeDef",
    "UpdateLiveSourceResponseTypeDef",
    "UpdateVodSourceRequestRequestTypeDef",
    "UpdateVodSourceResponseTypeDef",
    "VodSourceTypeDef",
    "GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef",
    "ListAlertsRequestListAlertsPaginateTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListLiveSourcesRequestListLiveSourcesPaginateTypeDef",
    "ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef",
    "ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef",
    "ListSourceLocationsRequestListSourceLocationsPaginateTypeDef",
    "ListVodSourcesRequestListVodSourcesPaginateTypeDef",
    "ResponseOutputItemPaginatorTypeDef",
    "RequestOutputItemTypeDef",
    "ResponseOutputItemTypeDef",
    "PrefetchConsumptionTypeDef",
    "PrefetchRetrievalTypeDef",
    "ScheduleEntryTypeDef",
    "ScheduleConfigurationTypeDef",
    "TimeSignalMessageTypeDef",
    "UpdateProgramScheduleConfigurationTypeDef",
    "CreateSourceLocationRequestRequestTypeDef",
    "CreateSourceLocationResponseTypeDef",
    "DescribeSourceLocationResponseTypeDef",
    "SourceLocationTypeDef",
    "UpdateSourceLocationRequestRequestTypeDef",
    "UpdateSourceLocationResponseTypeDef",
    "GetPlaybackConfigurationResponseTypeDef",
    "PlaybackConfigurationTypeDef",
    "PutPlaybackConfigurationRequestRequestTypeDef",
    "PutPlaybackConfigurationResponseTypeDef",
    "PrefetchSchedulePaginatorTypeDef",
    "ListLiveSourcesResponseTypeDef",
    "ListVodSourcesResponseTypeDef",
    "ChannelPaginatorTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "ChannelTypeDef",
    "CreateChannelResponseTypeDef",
    "DescribeChannelResponseTypeDef",
    "UpdateChannelResponseTypeDef",
    "CreatePrefetchScheduleRequestRequestTypeDef",
    "CreatePrefetchScheduleResponseTypeDef",
    "GetPrefetchScheduleResponseTypeDef",
    "PrefetchScheduleTypeDef",
    "GetChannelScheduleResponseTypeDef",
    "AdBreakTypeDef",
    "ListSourceLocationsResponseTypeDef",
    "ListPlaybackConfigurationsResponseTypeDef",
    "ListPrefetchSchedulesResponsePaginatorTypeDef",
    "ListChannelsResponsePaginatorTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPrefetchSchedulesResponseTypeDef",
    "CreateProgramRequestRequestTypeDef",
    "CreateProgramResponseTypeDef",
    "DescribeProgramResponseTypeDef",
    "UpdateProgramRequestRequestTypeDef",
    "UpdateProgramResponseTypeDef",
)

SecretsManagerAccessTokenConfigurationTypeDef = TypedDict(
    "SecretsManagerAccessTokenConfigurationTypeDef",
    {
        "HeaderName": str,
        "SecretArn": str,
        "SecretStringKey": str,
    },
    total=False,
)

KeyValuePairTypeDef = TypedDict(
    "KeyValuePairTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

SlateSourceTypeDef = TypedDict(
    "SlateSourceTypeDef",
    {
        "SourceLocationName": str,
        "VodSourceName": str,
    },
    total=False,
)

SpliceInsertMessageTypeDef = TypedDict(
    "SpliceInsertMessageTypeDef",
    {
        "AvailNum": int,
        "AvailsExpected": int,
        "SpliceEventId": int,
        "UniqueProgramId": int,
    },
    total=False,
)

AdMarkerPassthroughTypeDef = TypedDict(
    "AdMarkerPassthroughTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

_RequiredAlertTypeDef = TypedDict(
    "_RequiredAlertTypeDef",
    {
        "AlertCode": str,
        "AlertMessage": str,
        "LastModifiedTime": datetime,
        "RelatedResourceArns": List[str],
        "ResourceArn": str,
    },
)
_OptionalAlertTypeDef = TypedDict(
    "_OptionalAlertTypeDef",
    {
        "Category": AlertCategoryType,
    },
    total=False,
)


class AlertTypeDef(_RequiredAlertTypeDef, _OptionalAlertTypeDef):
    pass


AvailMatchingCriteriaTypeDef = TypedDict(
    "AvailMatchingCriteriaTypeDef",
    {
        "DynamicVariable": str,
        "Operator": Literal["EQUALS"],
    },
)

AvailSuppressionTypeDef = TypedDict(
    "AvailSuppressionTypeDef",
    {
        "FillPolicy": FillPolicyType,
        "Mode": ModeType,
        "Value": str,
    },
    total=False,
)

BumperTypeDef = TypedDict(
    "BumperTypeDef",
    {
        "EndUrl": str,
        "StartUrl": str,
    },
    total=False,
)

CdnConfigurationTypeDef = TypedDict(
    "CdnConfigurationTypeDef",
    {
        "AdSegmentUrlPrefix": str,
        "ContentSegmentUrlPrefix": str,
    },
    total=False,
)

LogConfigurationForChannelTypeDef = TypedDict(
    "LogConfigurationForChannelTypeDef",
    {
        "LogTypes": List[Literal["AS_RUN"]],
    },
    total=False,
)

ClipRangeTypeDef = TypedDict(
    "ClipRangeTypeDef",
    {
        "EndOffsetMillis": int,
    },
)

ConfigureLogsForChannelRequestRequestTypeDef = TypedDict(
    "ConfigureLogsForChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
        "LogTypes": Sequence[Literal["AS_RUN"]],
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

ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef = TypedDict(
    "ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef",
    {
        "PercentEnabled": int,
        "PlaybackConfigurationName": str,
    },
)

HttpPackageConfigurationTypeDef = TypedDict(
    "HttpPackageConfigurationTypeDef",
    {
        "Path": str,
        "SourceGroup": str,
        "Type": TypeType,
    },
)

DefaultSegmentDeliveryConfigurationTypeDef = TypedDict(
    "DefaultSegmentDeliveryConfigurationTypeDef",
    {
        "BaseUrl": str,
    },
    total=False,
)

HttpConfigurationTypeDef = TypedDict(
    "HttpConfigurationTypeDef",
    {
        "BaseUrl": str,
    },
)

SegmentDeliveryConfigurationTypeDef = TypedDict(
    "SegmentDeliveryConfigurationTypeDef",
    {
        "BaseUrl": str,
        "Name": str,
    },
    total=False,
)

DashConfigurationForPutTypeDef = TypedDict(
    "DashConfigurationForPutTypeDef",
    {
        "MpdLocation": str,
        "OriginManifestType": OriginManifestTypeType,
    },
    total=False,
)

DashConfigurationTypeDef = TypedDict(
    "DashConfigurationTypeDef",
    {
        "ManifestEndpointPrefix": str,
        "MpdLocation": str,
        "OriginManifestType": OriginManifestTypeType,
    },
    total=False,
)

DashPlaylistSettingsTypeDef = TypedDict(
    "DashPlaylistSettingsTypeDef",
    {
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)

DeleteChannelPolicyRequestRequestTypeDef = TypedDict(
    "DeleteChannelPolicyRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

DeleteChannelRequestRequestTypeDef = TypedDict(
    "DeleteChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

DeleteLiveSourceRequestRequestTypeDef = TypedDict(
    "DeleteLiveSourceRequestRequestTypeDef",
    {
        "LiveSourceName": str,
        "SourceLocationName": str,
    },
)

DeletePlaybackConfigurationRequestRequestTypeDef = TypedDict(
    "DeletePlaybackConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeletePrefetchScheduleRequestRequestTypeDef = TypedDict(
    "DeletePrefetchScheduleRequestRequestTypeDef",
    {
        "Name": str,
        "PlaybackConfigurationName": str,
    },
)

DeleteProgramRequestRequestTypeDef = TypedDict(
    "DeleteProgramRequestRequestTypeDef",
    {
        "ChannelName": str,
        "ProgramName": str,
    },
)

DeleteSourceLocationRequestRequestTypeDef = TypedDict(
    "DeleteSourceLocationRequestRequestTypeDef",
    {
        "SourceLocationName": str,
    },
)

DeleteVodSourceRequestRequestTypeDef = TypedDict(
    "DeleteVodSourceRequestRequestTypeDef",
    {
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)

DescribeChannelRequestRequestTypeDef = TypedDict(
    "DescribeChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

DescribeLiveSourceRequestRequestTypeDef = TypedDict(
    "DescribeLiveSourceRequestRequestTypeDef",
    {
        "LiveSourceName": str,
        "SourceLocationName": str,
    },
)

DescribeProgramRequestRequestTypeDef = TypedDict(
    "DescribeProgramRequestRequestTypeDef",
    {
        "ChannelName": str,
        "ProgramName": str,
    },
)

DescribeSourceLocationRequestRequestTypeDef = TypedDict(
    "DescribeSourceLocationRequestRequestTypeDef",
    {
        "SourceLocationName": str,
    },
)

DescribeVodSourceRequestRequestTypeDef = TypedDict(
    "DescribeVodSourceRequestRequestTypeDef",
    {
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)

GetChannelPolicyRequestRequestTypeDef = TypedDict(
    "GetChannelPolicyRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredGetChannelScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredGetChannelScheduleRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)
_OptionalGetChannelScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalGetChannelScheduleRequestRequestTypeDef",
    {
        "DurationMinutes": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetChannelScheduleRequestRequestTypeDef(
    _RequiredGetChannelScheduleRequestRequestTypeDef,
    _OptionalGetChannelScheduleRequestRequestTypeDef,
):
    pass


GetPlaybackConfigurationRequestRequestTypeDef = TypedDict(
    "GetPlaybackConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

HlsConfigurationTypeDef = TypedDict(
    "HlsConfigurationTypeDef",
    {
        "ManifestEndpointPrefix": str,
    },
    total=False,
)

LivePreRollConfigurationTypeDef = TypedDict(
    "LivePreRollConfigurationTypeDef",
    {
        "AdDecisionServerUrl": str,
        "MaxDurationSeconds": int,
    },
    total=False,
)

LogConfigurationTypeDef = TypedDict(
    "LogConfigurationTypeDef",
    {
        "PercentEnabled": int,
    },
)

GetPrefetchScheduleRequestRequestTypeDef = TypedDict(
    "GetPrefetchScheduleRequestRequestTypeDef",
    {
        "Name": str,
        "PlaybackConfigurationName": str,
    },
)

HlsPlaylistSettingsPaginatorTypeDef = TypedDict(
    "HlsPlaylistSettingsPaginatorTypeDef",
    {
        "AdMarkupType": List[AdMarkupTypeType],
        "ManifestWindowSeconds": int,
    },
    total=False,
)

HlsPlaylistSettingsTypeDef = TypedDict(
    "HlsPlaylistSettingsTypeDef",
    {
        "AdMarkupType": Sequence[AdMarkupTypeType],
        "ManifestWindowSeconds": int,
    },
    total=False,
)

_RequiredListAlertsRequestRequestTypeDef = TypedDict(
    "_RequiredListAlertsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListAlertsRequestRequestTypeDef = TypedDict(
    "_OptionalListAlertsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAlertsRequestRequestTypeDef(
    _RequiredListAlertsRequestRequestTypeDef, _OptionalListAlertsRequestRequestTypeDef
):
    pass


ListChannelsRequestRequestTypeDef = TypedDict(
    "ListChannelsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListLiveSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListLiveSourcesRequestRequestTypeDef",
    {
        "SourceLocationName": str,
    },
)
_OptionalListLiveSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListLiveSourcesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListLiveSourcesRequestRequestTypeDef(
    _RequiredListLiveSourcesRequestRequestTypeDef, _OptionalListLiveSourcesRequestRequestTypeDef
):
    pass


ListPlaybackConfigurationsRequestRequestTypeDef = TypedDict(
    "ListPlaybackConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListPrefetchSchedulesRequestRequestTypeDef = TypedDict(
    "_RequiredListPrefetchSchedulesRequestRequestTypeDef",
    {
        "PlaybackConfigurationName": str,
    },
)
_OptionalListPrefetchSchedulesRequestRequestTypeDef = TypedDict(
    "_OptionalListPrefetchSchedulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "StreamId": str,
    },
    total=False,
)


class ListPrefetchSchedulesRequestRequestTypeDef(
    _RequiredListPrefetchSchedulesRequestRequestTypeDef,
    _OptionalListPrefetchSchedulesRequestRequestTypeDef,
):
    pass


ListSourceLocationsRequestRequestTypeDef = TypedDict(
    "ListSourceLocationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListVodSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListVodSourcesRequestRequestTypeDef",
    {
        "SourceLocationName": str,
    },
)
_OptionalListVodSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListVodSourcesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListVodSourcesRequestRequestTypeDef(
    _RequiredListVodSourcesRequestRequestTypeDef, _OptionalListVodSourcesRequestRequestTypeDef
):
    pass


TimestampTypeDef = Union[datetime, str]
_RequiredPrefetchRetrievalPaginatorTypeDef = TypedDict(
    "_RequiredPrefetchRetrievalPaginatorTypeDef",
    {
        "EndTime": datetime,
    },
)
_OptionalPrefetchRetrievalPaginatorTypeDef = TypedDict(
    "_OptionalPrefetchRetrievalPaginatorTypeDef",
    {
        "DynamicVariables": Dict[str, str],
        "StartTime": datetime,
    },
    total=False,
)


class PrefetchRetrievalPaginatorTypeDef(
    _RequiredPrefetchRetrievalPaginatorTypeDef, _OptionalPrefetchRetrievalPaginatorTypeDef
):
    pass


PutChannelPolicyRequestRequestTypeDef = TypedDict(
    "PutChannelPolicyRequestRequestTypeDef",
    {
        "ChannelName": str,
        "Policy": str,
    },
)

ScheduleAdBreakTypeDef = TypedDict(
    "ScheduleAdBreakTypeDef",
    {
        "ApproximateDurationSeconds": int,
        "ApproximateStartTime": datetime,
        "SourceLocationName": str,
        "VodSourceName": str,
    },
    total=False,
)

_RequiredTransitionTypeDef = TypedDict(
    "_RequiredTransitionTypeDef",
    {
        "RelativePosition": RelativePositionType,
        "Type": str,
    },
)
_OptionalTransitionTypeDef = TypedDict(
    "_OptionalTransitionTypeDef",
    {
        "DurationMillis": int,
        "RelativeProgram": str,
        "ScheduledStartTimeMillis": int,
    },
    total=False,
)


class TransitionTypeDef(_RequiredTransitionTypeDef, _OptionalTransitionTypeDef):
    pass


SegmentationDescriptorTypeDef = TypedDict(
    "SegmentationDescriptorTypeDef",
    {
        "SegmentNum": int,
        "SegmentationEventId": int,
        "SegmentationTypeId": int,
        "SegmentationUpid": str,
        "SegmentationUpidType": int,
        "SegmentsExpected": int,
        "SubSegmentNum": int,
        "SubSegmentsExpected": int,
    },
    total=False,
)

StartChannelRequestRequestTypeDef = TypedDict(
    "StartChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

StopChannelRequestRequestTypeDef = TypedDict(
    "StopChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateProgramTransitionTypeDef = TypedDict(
    "UpdateProgramTransitionTypeDef",
    {
        "DurationMillis": int,
        "ScheduledStartTimeMillis": int,
    },
    total=False,
)

AccessConfigurationTypeDef = TypedDict(
    "AccessConfigurationTypeDef",
    {
        "AccessType": AccessTypeType,
        "SecretsManagerAccessTokenConfiguration": SecretsManagerAccessTokenConfigurationTypeDef,
    },
    total=False,
)

ManifestProcessingRulesTypeDef = TypedDict(
    "ManifestProcessingRulesTypeDef",
    {
        "AdMarkerPassthrough": AdMarkerPassthroughTypeDef,
    },
    total=False,
)

_RequiredPrefetchConsumptionPaginatorTypeDef = TypedDict(
    "_RequiredPrefetchConsumptionPaginatorTypeDef",
    {
        "EndTime": datetime,
    },
)
_OptionalPrefetchConsumptionPaginatorTypeDef = TypedDict(
    "_OptionalPrefetchConsumptionPaginatorTypeDef",
    {
        "AvailMatchingCriteria": List[AvailMatchingCriteriaTypeDef],
        "StartTime": datetime,
    },
    total=False,
)


class PrefetchConsumptionPaginatorTypeDef(
    _RequiredPrefetchConsumptionPaginatorTypeDef, _OptionalPrefetchConsumptionPaginatorTypeDef
):
    pass


ConfigureLogsForChannelResponseTypeDef = TypedDict(
    "ConfigureLogsForChannelResponseTypeDef",
    {
        "ChannelName": str,
        "LogTypes": List[Literal["AS_RUN"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigureLogsForPlaybackConfigurationResponseTypeDef = TypedDict(
    "ConfigureLogsForPlaybackConfigurationResponseTypeDef",
    {
        "PercentEnabled": int,
        "PlaybackConfigurationName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChannelPolicyResponseTypeDef = TypedDict(
    "GetChannelPolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAlertsResponseTypeDef = TypedDict(
    "ListAlertsResponseTypeDef",
    {
        "Items": List[AlertTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLiveSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLiveSourceRequestRequestTypeDef",
    {
        "HttpPackageConfigurations": Sequence[HttpPackageConfigurationTypeDef],
        "LiveSourceName": str,
        "SourceLocationName": str,
    },
)
_OptionalCreateLiveSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLiveSourceRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateLiveSourceRequestRequestTypeDef(
    _RequiredCreateLiveSourceRequestRequestTypeDef, _OptionalCreateLiveSourceRequestRequestTypeDef
):
    pass


CreateLiveSourceResponseTypeDef = TypedDict(
    "CreateLiveSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "LiveSourceName": str,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateVodSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVodSourceRequestRequestTypeDef",
    {
        "HttpPackageConfigurations": Sequence[HttpPackageConfigurationTypeDef],
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)
_OptionalCreateVodSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVodSourceRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateVodSourceRequestRequestTypeDef(
    _RequiredCreateVodSourceRequestRequestTypeDef, _OptionalCreateVodSourceRequestRequestTypeDef
):
    pass


CreateVodSourceResponseTypeDef = TypedDict(
    "CreateVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLiveSourceResponseTypeDef = TypedDict(
    "DescribeLiveSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "LiveSourceName": str,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVodSourceResponseTypeDef = TypedDict(
    "DescribeVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredLiveSourceTypeDef = TypedDict(
    "_RequiredLiveSourceTypeDef",
    {
        "Arn": str,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LiveSourceName": str,
        "SourceLocationName": str,
    },
)
_OptionalLiveSourceTypeDef = TypedDict(
    "_OptionalLiveSourceTypeDef",
    {
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)


class LiveSourceTypeDef(_RequiredLiveSourceTypeDef, _OptionalLiveSourceTypeDef):
    pass


UpdateLiveSourceRequestRequestTypeDef = TypedDict(
    "UpdateLiveSourceRequestRequestTypeDef",
    {
        "HttpPackageConfigurations": Sequence[HttpPackageConfigurationTypeDef],
        "LiveSourceName": str,
        "SourceLocationName": str,
    },
)

UpdateLiveSourceResponseTypeDef = TypedDict(
    "UpdateLiveSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "LiveSourceName": str,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVodSourceRequestRequestTypeDef = TypedDict(
    "UpdateVodSourceRequestRequestTypeDef",
    {
        "HttpPackageConfigurations": Sequence[HttpPackageConfigurationTypeDef],
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)

UpdateVodSourceResponseTypeDef = TypedDict(
    "UpdateVodSourceResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "LastModifiedTime": datetime,
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredVodSourceTypeDef = TypedDict(
    "_RequiredVodSourceTypeDef",
    {
        "Arn": str,
        "HttpPackageConfigurations": List[HttpPackageConfigurationTypeDef],
        "SourceLocationName": str,
        "VodSourceName": str,
    },
)
_OptionalVodSourceTypeDef = TypedDict(
    "_OptionalVodSourceTypeDef",
    {
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)


class VodSourceTypeDef(_RequiredVodSourceTypeDef, _OptionalVodSourceTypeDef):
    pass


_RequiredGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef = TypedDict(
    "_RequiredGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef",
    {
        "ChannelName": str,
    },
)
_OptionalGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef = TypedDict(
    "_OptionalGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef",
    {
        "DurationMinutes": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef(
    _RequiredGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef,
    _OptionalGetChannelScheduleRequestGetChannelSchedulePaginateTypeDef,
):
    pass


_RequiredListAlertsRequestListAlertsPaginateTypeDef = TypedDict(
    "_RequiredListAlertsRequestListAlertsPaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListAlertsRequestListAlertsPaginateTypeDef = TypedDict(
    "_OptionalListAlertsRequestListAlertsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAlertsRequestListAlertsPaginateTypeDef(
    _RequiredListAlertsRequestListAlertsPaginateTypeDef,
    _OptionalListAlertsRequestListAlertsPaginateTypeDef,
):
    pass


ListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "ListChannelsRequestListChannelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListLiveSourcesRequestListLiveSourcesPaginateTypeDef = TypedDict(
    "_RequiredListLiveSourcesRequestListLiveSourcesPaginateTypeDef",
    {
        "SourceLocationName": str,
    },
)
_OptionalListLiveSourcesRequestListLiveSourcesPaginateTypeDef = TypedDict(
    "_OptionalListLiveSourcesRequestListLiveSourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListLiveSourcesRequestListLiveSourcesPaginateTypeDef(
    _RequiredListLiveSourcesRequestListLiveSourcesPaginateTypeDef,
    _OptionalListLiveSourcesRequestListLiveSourcesPaginateTypeDef,
):
    pass


ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef = TypedDict(
    "ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef = TypedDict(
    "_RequiredListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef",
    {
        "PlaybackConfigurationName": str,
    },
)
_OptionalListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef = TypedDict(
    "_OptionalListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef",
    {
        "StreamId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef(
    _RequiredListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef,
    _OptionalListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef,
):
    pass


ListSourceLocationsRequestListSourceLocationsPaginateTypeDef = TypedDict(
    "ListSourceLocationsRequestListSourceLocationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListVodSourcesRequestListVodSourcesPaginateTypeDef = TypedDict(
    "_RequiredListVodSourcesRequestListVodSourcesPaginateTypeDef",
    {
        "SourceLocationName": str,
    },
)
_OptionalListVodSourcesRequestListVodSourcesPaginateTypeDef = TypedDict(
    "_OptionalListVodSourcesRequestListVodSourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVodSourcesRequestListVodSourcesPaginateTypeDef(
    _RequiredListVodSourcesRequestListVodSourcesPaginateTypeDef,
    _OptionalListVodSourcesRequestListVodSourcesPaginateTypeDef,
):
    pass


_RequiredResponseOutputItemPaginatorTypeDef = TypedDict(
    "_RequiredResponseOutputItemPaginatorTypeDef",
    {
        "ManifestName": str,
        "PlaybackUrl": str,
        "SourceGroup": str,
    },
)
_OptionalResponseOutputItemPaginatorTypeDef = TypedDict(
    "_OptionalResponseOutputItemPaginatorTypeDef",
    {
        "DashPlaylistSettings": DashPlaylistSettingsTypeDef,
        "HlsPlaylistSettings": HlsPlaylistSettingsPaginatorTypeDef,
    },
    total=False,
)


class ResponseOutputItemPaginatorTypeDef(
    _RequiredResponseOutputItemPaginatorTypeDef, _OptionalResponseOutputItemPaginatorTypeDef
):
    pass


_RequiredRequestOutputItemTypeDef = TypedDict(
    "_RequiredRequestOutputItemTypeDef",
    {
        "ManifestName": str,
        "SourceGroup": str,
    },
)
_OptionalRequestOutputItemTypeDef = TypedDict(
    "_OptionalRequestOutputItemTypeDef",
    {
        "DashPlaylistSettings": DashPlaylistSettingsTypeDef,
        "HlsPlaylistSettings": HlsPlaylistSettingsTypeDef,
    },
    total=False,
)


class RequestOutputItemTypeDef(
    _RequiredRequestOutputItemTypeDef, _OptionalRequestOutputItemTypeDef
):
    pass


_RequiredResponseOutputItemTypeDef = TypedDict(
    "_RequiredResponseOutputItemTypeDef",
    {
        "ManifestName": str,
        "PlaybackUrl": str,
        "SourceGroup": str,
    },
)
_OptionalResponseOutputItemTypeDef = TypedDict(
    "_OptionalResponseOutputItemTypeDef",
    {
        "DashPlaylistSettings": DashPlaylistSettingsTypeDef,
        "HlsPlaylistSettings": HlsPlaylistSettingsTypeDef,
    },
    total=False,
)


class ResponseOutputItemTypeDef(
    _RequiredResponseOutputItemTypeDef, _OptionalResponseOutputItemTypeDef
):
    pass


_RequiredPrefetchConsumptionTypeDef = TypedDict(
    "_RequiredPrefetchConsumptionTypeDef",
    {
        "EndTime": TimestampTypeDef,
    },
)
_OptionalPrefetchConsumptionTypeDef = TypedDict(
    "_OptionalPrefetchConsumptionTypeDef",
    {
        "AvailMatchingCriteria": Sequence[AvailMatchingCriteriaTypeDef],
        "StartTime": TimestampTypeDef,
    },
    total=False,
)


class PrefetchConsumptionTypeDef(
    _RequiredPrefetchConsumptionTypeDef, _OptionalPrefetchConsumptionTypeDef
):
    pass


_RequiredPrefetchRetrievalTypeDef = TypedDict(
    "_RequiredPrefetchRetrievalTypeDef",
    {
        "EndTime": TimestampTypeDef,
    },
)
_OptionalPrefetchRetrievalTypeDef = TypedDict(
    "_OptionalPrefetchRetrievalTypeDef",
    {
        "DynamicVariables": Mapping[str, str],
        "StartTime": TimestampTypeDef,
    },
    total=False,
)


class PrefetchRetrievalTypeDef(
    _RequiredPrefetchRetrievalTypeDef, _OptionalPrefetchRetrievalTypeDef
):
    pass


_RequiredScheduleEntryTypeDef = TypedDict(
    "_RequiredScheduleEntryTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ProgramName": str,
        "SourceLocationName": str,
    },
)
_OptionalScheduleEntryTypeDef = TypedDict(
    "_OptionalScheduleEntryTypeDef",
    {
        "ApproximateDurationSeconds": int,
        "ApproximateStartTime": datetime,
        "LiveSourceName": str,
        "ScheduleAdBreaks": List[ScheduleAdBreakTypeDef],
        "ScheduleEntryType": ScheduleEntryTypeType,
        "VodSourceName": str,
    },
    total=False,
)


class ScheduleEntryTypeDef(_RequiredScheduleEntryTypeDef, _OptionalScheduleEntryTypeDef):
    pass


_RequiredScheduleConfigurationTypeDef = TypedDict(
    "_RequiredScheduleConfigurationTypeDef",
    {
        "Transition": TransitionTypeDef,
    },
)
_OptionalScheduleConfigurationTypeDef = TypedDict(
    "_OptionalScheduleConfigurationTypeDef",
    {
        "ClipRange": ClipRangeTypeDef,
    },
    total=False,
)


class ScheduleConfigurationTypeDef(
    _RequiredScheduleConfigurationTypeDef, _OptionalScheduleConfigurationTypeDef
):
    pass


TimeSignalMessageTypeDef = TypedDict(
    "TimeSignalMessageTypeDef",
    {
        "SegmentationDescriptors": Sequence[SegmentationDescriptorTypeDef],
    },
    total=False,
)

UpdateProgramScheduleConfigurationTypeDef = TypedDict(
    "UpdateProgramScheduleConfigurationTypeDef",
    {
        "ClipRange": ClipRangeTypeDef,
        "Transition": UpdateProgramTransitionTypeDef,
    },
    total=False,
)

_RequiredCreateSourceLocationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSourceLocationRequestRequestTypeDef",
    {
        "HttpConfiguration": HttpConfigurationTypeDef,
        "SourceLocationName": str,
    },
)
_OptionalCreateSourceLocationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSourceLocationRequestRequestTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "SegmentDeliveryConfigurations": Sequence[SegmentDeliveryConfigurationTypeDef],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateSourceLocationRequestRequestTypeDef(
    _RequiredCreateSourceLocationRequestRequestTypeDef,
    _OptionalCreateSourceLocationRequestRequestTypeDef,
):
    pass


CreateSourceLocationResponseTypeDef = TypedDict(
    "CreateSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "HttpConfiguration": HttpConfigurationTypeDef,
        "LastModifiedTime": datetime,
        "SegmentDeliveryConfigurations": List[SegmentDeliveryConfigurationTypeDef],
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSourceLocationResponseTypeDef = TypedDict(
    "DescribeSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "HttpConfiguration": HttpConfigurationTypeDef,
        "LastModifiedTime": datetime,
        "SegmentDeliveryConfigurations": List[SegmentDeliveryConfigurationTypeDef],
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSourceLocationTypeDef = TypedDict(
    "_RequiredSourceLocationTypeDef",
    {
        "Arn": str,
        "HttpConfiguration": HttpConfigurationTypeDef,
        "SourceLocationName": str,
    },
)
_OptionalSourceLocationTypeDef = TypedDict(
    "_OptionalSourceLocationTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "LastModifiedTime": datetime,
        "SegmentDeliveryConfigurations": List[SegmentDeliveryConfigurationTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)


class SourceLocationTypeDef(_RequiredSourceLocationTypeDef, _OptionalSourceLocationTypeDef):
    pass


_RequiredUpdateSourceLocationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSourceLocationRequestRequestTypeDef",
    {
        "HttpConfiguration": HttpConfigurationTypeDef,
        "SourceLocationName": str,
    },
)
_OptionalUpdateSourceLocationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSourceLocationRequestRequestTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "SegmentDeliveryConfigurations": Sequence[SegmentDeliveryConfigurationTypeDef],
    },
    total=False,
)


class UpdateSourceLocationRequestRequestTypeDef(
    _RequiredUpdateSourceLocationRequestRequestTypeDef,
    _OptionalUpdateSourceLocationRequestRequestTypeDef,
):
    pass


UpdateSourceLocationResponseTypeDef = TypedDict(
    "UpdateSourceLocationResponseTypeDef",
    {
        "AccessConfiguration": AccessConfigurationTypeDef,
        "Arn": str,
        "CreationTime": datetime,
        "DefaultSegmentDeliveryConfiguration": DefaultSegmentDeliveryConfigurationTypeDef,
        "HttpConfiguration": HttpConfigurationTypeDef,
        "LastModifiedTime": datetime,
        "SegmentDeliveryConfigurations": List[SegmentDeliveryConfigurationTypeDef],
        "SourceLocationName": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPlaybackConfigurationResponseTypeDef = TypedDict(
    "GetPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": AvailSuppressionTypeDef,
        "Bumper": BumperTypeDef,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "LogConfiguration": LogConfigurationTypeDef,
        "ManifestProcessingRules": ManifestProcessingRulesTypeDef,
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PlaybackConfigurationTypeDef = TypedDict(
    "PlaybackConfigurationTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": AvailSuppressionTypeDef,
        "Bumper": BumperTypeDef,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "LogConfiguration": LogConfigurationTypeDef,
        "ManifestProcessingRules": ManifestProcessingRulesTypeDef,
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

_RequiredPutPlaybackConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutPlaybackConfigurationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalPutPlaybackConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutPlaybackConfigurationRequestRequestTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": AvailSuppressionTypeDef,
        "Bumper": BumperTypeDef,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "ConfigurationAliases": Mapping[str, Mapping[str, str]],
        "DashConfiguration": DashConfigurationForPutTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "ManifestProcessingRules": ManifestProcessingRulesTypeDef,
        "PersonalizationThresholdSeconds": int,
        "SlateAdUrl": str,
        "Tags": Mapping[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)


class PutPlaybackConfigurationRequestRequestTypeDef(
    _RequiredPutPlaybackConfigurationRequestRequestTypeDef,
    _OptionalPutPlaybackConfigurationRequestRequestTypeDef,
):
    pass


PutPlaybackConfigurationResponseTypeDef = TypedDict(
    "PutPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "AvailSuppression": AvailSuppressionTypeDef,
        "Bumper": BumperTypeDef,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "ConfigurationAliases": Dict[str, Dict[str, str]],
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "LogConfiguration": LogConfigurationTypeDef,
        "ManifestProcessingRules": ManifestProcessingRulesTypeDef,
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPrefetchSchedulePaginatorTypeDef = TypedDict(
    "_RequiredPrefetchSchedulePaginatorTypeDef",
    {
        "Arn": str,
        "Consumption": PrefetchConsumptionPaginatorTypeDef,
        "Name": str,
        "PlaybackConfigurationName": str,
        "Retrieval": PrefetchRetrievalPaginatorTypeDef,
    },
)
_OptionalPrefetchSchedulePaginatorTypeDef = TypedDict(
    "_OptionalPrefetchSchedulePaginatorTypeDef",
    {
        "StreamId": str,
    },
    total=False,
)


class PrefetchSchedulePaginatorTypeDef(
    _RequiredPrefetchSchedulePaginatorTypeDef, _OptionalPrefetchSchedulePaginatorTypeDef
):
    pass


ListLiveSourcesResponseTypeDef = TypedDict(
    "ListLiveSourcesResponseTypeDef",
    {
        "Items": List[LiveSourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVodSourcesResponseTypeDef = TypedDict(
    "ListVodSourcesResponseTypeDef",
    {
        "Items": List[VodSourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredChannelPaginatorTypeDef = TypedDict(
    "_RequiredChannelPaginatorTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": str,
        "LogConfiguration": LogConfigurationForChannelTypeDef,
        "Outputs": List[ResponseOutputItemPaginatorTypeDef],
        "PlaybackMode": str,
        "Tier": str,
    },
)
_OptionalChannelPaginatorTypeDef = TypedDict(
    "_OptionalChannelPaginatorTypeDef",
    {
        "CreationTime": datetime,
        "FillerSlate": SlateSourceTypeDef,
        "LastModifiedTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ChannelPaginatorTypeDef(_RequiredChannelPaginatorTypeDef, _OptionalChannelPaginatorTypeDef):
    pass


_RequiredCreateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
        "Outputs": Sequence[RequestOutputItemTypeDef],
        "PlaybackMode": PlaybackModeType,
    },
)
_OptionalCreateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateChannelRequestRequestTypeDef",
    {
        "FillerSlate": SlateSourceTypeDef,
        "Tags": Mapping[str, str],
        "Tier": TierType,
    },
    total=False,
)


class CreateChannelRequestRequestTypeDef(
    _RequiredCreateChannelRequestRequestTypeDef, _OptionalCreateChannelRequestRequestTypeDef
):
    pass


_RequiredUpdateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateChannelRequestRequestTypeDef",
    {
        "ChannelName": str,
        "Outputs": Sequence[RequestOutputItemTypeDef],
    },
)
_OptionalUpdateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateChannelRequestRequestTypeDef",
    {
        "FillerSlate": SlateSourceTypeDef,
    },
    total=False,
)


class UpdateChannelRequestRequestTypeDef(
    _RequiredUpdateChannelRequestRequestTypeDef, _OptionalUpdateChannelRequestRequestTypeDef
):
    pass


_RequiredChannelTypeDef = TypedDict(
    "_RequiredChannelTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": str,
        "LogConfiguration": LogConfigurationForChannelTypeDef,
        "Outputs": List[ResponseOutputItemTypeDef],
        "PlaybackMode": str,
        "Tier": str,
    },
)
_OptionalChannelTypeDef = TypedDict(
    "_OptionalChannelTypeDef",
    {
        "CreationTime": datetime,
        "FillerSlate": SlateSourceTypeDef,
        "LastModifiedTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ChannelTypeDef(_RequiredChannelTypeDef, _OptionalChannelTypeDef):
    pass


CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": ChannelStateType,
        "CreationTime": datetime,
        "FillerSlate": SlateSourceTypeDef,
        "LastModifiedTime": datetime,
        "Outputs": List[ResponseOutputItemTypeDef],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
        "Tier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeChannelResponseTypeDef = TypedDict(
    "DescribeChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": ChannelStateType,
        "CreationTime": datetime,
        "FillerSlate": SlateSourceTypeDef,
        "LastModifiedTime": datetime,
        "LogConfiguration": LogConfigurationForChannelTypeDef,
        "Outputs": List[ResponseOutputItemTypeDef],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
        "Tier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelState": ChannelStateType,
        "CreationTime": datetime,
        "FillerSlate": SlateSourceTypeDef,
        "LastModifiedTime": datetime,
        "Outputs": List[ResponseOutputItemTypeDef],
        "PlaybackMode": str,
        "Tags": Dict[str, str],
        "Tier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePrefetchScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePrefetchScheduleRequestRequestTypeDef",
    {
        "Consumption": PrefetchConsumptionTypeDef,
        "Name": str,
        "PlaybackConfigurationName": str,
        "Retrieval": PrefetchRetrievalTypeDef,
    },
)
_OptionalCreatePrefetchScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePrefetchScheduleRequestRequestTypeDef",
    {
        "StreamId": str,
    },
    total=False,
)


class CreatePrefetchScheduleRequestRequestTypeDef(
    _RequiredCreatePrefetchScheduleRequestRequestTypeDef,
    _OptionalCreatePrefetchScheduleRequestRequestTypeDef,
):
    pass


CreatePrefetchScheduleResponseTypeDef = TypedDict(
    "CreatePrefetchScheduleResponseTypeDef",
    {
        "Arn": str,
        "Consumption": PrefetchConsumptionTypeDef,
        "Name": str,
        "PlaybackConfigurationName": str,
        "Retrieval": PrefetchRetrievalTypeDef,
        "StreamId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPrefetchScheduleResponseTypeDef = TypedDict(
    "GetPrefetchScheduleResponseTypeDef",
    {
        "Arn": str,
        "Consumption": PrefetchConsumptionTypeDef,
        "Name": str,
        "PlaybackConfigurationName": str,
        "Retrieval": PrefetchRetrievalTypeDef,
        "StreamId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPrefetchScheduleTypeDef = TypedDict(
    "_RequiredPrefetchScheduleTypeDef",
    {
        "Arn": str,
        "Consumption": PrefetchConsumptionTypeDef,
        "Name": str,
        "PlaybackConfigurationName": str,
        "Retrieval": PrefetchRetrievalTypeDef,
    },
)
_OptionalPrefetchScheduleTypeDef = TypedDict(
    "_OptionalPrefetchScheduleTypeDef",
    {
        "StreamId": str,
    },
    total=False,
)


class PrefetchScheduleTypeDef(_RequiredPrefetchScheduleTypeDef, _OptionalPrefetchScheduleTypeDef):
    pass


GetChannelScheduleResponseTypeDef = TypedDict(
    "GetChannelScheduleResponseTypeDef",
    {
        "Items": List[ScheduleEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AdBreakTypeDef = TypedDict(
    "AdBreakTypeDef",
    {
        "AdBreakMetadata": Sequence[KeyValuePairTypeDef],
        "MessageType": MessageTypeType,
        "OffsetMillis": int,
        "Slate": SlateSourceTypeDef,
        "SpliceInsertMessage": SpliceInsertMessageTypeDef,
        "TimeSignalMessage": TimeSignalMessageTypeDef,
    },
    total=False,
)

ListSourceLocationsResponseTypeDef = TypedDict(
    "ListSourceLocationsResponseTypeDef",
    {
        "Items": List[SourceLocationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPlaybackConfigurationsResponseTypeDef = TypedDict(
    "ListPlaybackConfigurationsResponseTypeDef",
    {
        "Items": List[PlaybackConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPrefetchSchedulesResponsePaginatorTypeDef = TypedDict(
    "ListPrefetchSchedulesResponsePaginatorTypeDef",
    {
        "Items": List[PrefetchSchedulePaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelsResponsePaginatorTypeDef = TypedDict(
    "ListChannelsResponsePaginatorTypeDef",
    {
        "Items": List[ChannelPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {
        "Items": List[ChannelTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPrefetchSchedulesResponseTypeDef = TypedDict(
    "ListPrefetchSchedulesResponseTypeDef",
    {
        "Items": List[PrefetchScheduleTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateProgramRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProgramRequestRequestTypeDef",
    {
        "ChannelName": str,
        "ProgramName": str,
        "ScheduleConfiguration": ScheduleConfigurationTypeDef,
        "SourceLocationName": str,
    },
)
_OptionalCreateProgramRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProgramRequestRequestTypeDef",
    {
        "AdBreaks": Sequence[AdBreakTypeDef],
        "LiveSourceName": str,
        "VodSourceName": str,
    },
    total=False,
)


class CreateProgramRequestRequestTypeDef(
    _RequiredCreateProgramRequestRequestTypeDef, _OptionalCreateProgramRequestRequestTypeDef
):
    pass


CreateProgramResponseTypeDef = TypedDict(
    "CreateProgramResponseTypeDef",
    {
        "AdBreaks": List[AdBreakTypeDef],
        "Arn": str,
        "ChannelName": str,
        "ClipRange": ClipRangeTypeDef,
        "CreationTime": datetime,
        "DurationMillis": int,
        "LiveSourceName": str,
        "ProgramName": str,
        "ScheduledStartTime": datetime,
        "SourceLocationName": str,
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProgramResponseTypeDef = TypedDict(
    "DescribeProgramResponseTypeDef",
    {
        "AdBreaks": List[AdBreakTypeDef],
        "Arn": str,
        "ChannelName": str,
        "ClipRange": ClipRangeTypeDef,
        "CreationTime": datetime,
        "DurationMillis": int,
        "LiveSourceName": str,
        "ProgramName": str,
        "ScheduledStartTime": datetime,
        "SourceLocationName": str,
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateProgramRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProgramRequestRequestTypeDef",
    {
        "ChannelName": str,
        "ProgramName": str,
        "ScheduleConfiguration": UpdateProgramScheduleConfigurationTypeDef,
    },
)
_OptionalUpdateProgramRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProgramRequestRequestTypeDef",
    {
        "AdBreaks": Sequence[AdBreakTypeDef],
    },
    total=False,
)


class UpdateProgramRequestRequestTypeDef(
    _RequiredUpdateProgramRequestRequestTypeDef, _OptionalUpdateProgramRequestRequestTypeDef
):
    pass


UpdateProgramResponseTypeDef = TypedDict(
    "UpdateProgramResponseTypeDef",
    {
        "AdBreaks": List[AdBreakTypeDef],
        "Arn": str,
        "ChannelName": str,
        "ClipRange": ClipRangeTypeDef,
        "CreationTime": datetime,
        "DurationMillis": int,
        "LiveSourceName": str,
        "ProgramName": str,
        "ScheduledStartTime": datetime,
        "SourceLocationName": str,
        "VodSourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
