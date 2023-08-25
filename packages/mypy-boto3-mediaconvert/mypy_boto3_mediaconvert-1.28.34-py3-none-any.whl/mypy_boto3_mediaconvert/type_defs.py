"""
Type annotations for mediaconvert service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconvert/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediaconvert.type_defs import AacSettingsTypeDef

    data: AacSettingsTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AacAudioDescriptionBroadcasterMixType,
    AacCodecProfileType,
    AacCodingModeType,
    AacRateControlModeType,
    AacRawFormatType,
    AacSpecificationType,
    AacVbrQualityType,
    Ac3BitstreamModeType,
    Ac3CodingModeType,
    Ac3DynamicRangeCompressionLineType,
    Ac3DynamicRangeCompressionProfileType,
    Ac3DynamicRangeCompressionRfType,
    Ac3LfeFilterType,
    Ac3MetadataControlType,
    AccelerationModeType,
    AccelerationStatusType,
    AdvancedInputFilterAddTextureType,
    AdvancedInputFilterSharpenType,
    AdvancedInputFilterType,
    AfdSignalingType,
    AlphaBehaviorType,
    AncillaryConvert608To708Type,
    AncillaryTerminateCaptionsType,
    AntiAliasType,
    AudioChannelTagType,
    AudioCodecType,
    AudioDefaultSelectionType,
    AudioDurationCorrectionType,
    AudioLanguageCodeControlType,
    AudioNormalizationAlgorithmControlType,
    AudioNormalizationAlgorithmType,
    AudioNormalizationLoudnessLoggingType,
    AudioNormalizationPeakCalculationType,
    AudioSelectorTypeType,
    AudioTypeControlType,
    Av1AdaptiveQuantizationType,
    Av1BitDepthType,
    Av1FilmGrainSynthesisType,
    Av1FramerateControlType,
    Av1FramerateConversionAlgorithmType,
    Av1SpatialAdaptiveQuantizationType,
    AvcIntraClassType,
    AvcIntraFramerateControlType,
    AvcIntraFramerateConversionAlgorithmType,
    AvcIntraInterlaceModeType,
    AvcIntraScanTypeConversionModeType,
    AvcIntraSlowPalType,
    AvcIntraTelecineType,
    AvcIntraUhdQualityTuningLevelType,
    BandwidthReductionFilterSharpeningType,
    BandwidthReductionFilterStrengthType,
    BillingTagsSourceType,
    BurninSubtitleAlignmentType,
    BurninSubtitleApplyFontColorType,
    BurninSubtitleBackgroundColorType,
    BurninSubtitleFallbackFontType,
    BurninSubtitleFontColorType,
    BurninSubtitleOutlineColorType,
    BurninSubtitleShadowColorType,
    BurnInSubtitleStylePassthroughType,
    BurninSubtitleTeletextSpacingType,
    CaptionDestinationTypeType,
    CaptionSourceConvertPaintOnToPopOnType,
    CaptionSourceTypeType,
    CmafClientCacheType,
    CmafCodecSpecificationType,
    CmafEncryptionTypeType,
    CmafImageBasedTrickPlayType,
    CmafInitializationVectorInManifestType,
    CmafIntervalCadenceType,
    CmafKeyProviderTypeType,
    CmafManifestCompressionType,
    CmafManifestDurationFormatType,
    CmafMpdManifestBandwidthTypeType,
    CmafMpdProfileType,
    CmafPtsOffsetHandlingForBFramesType,
    CmafSegmentControlType,
    CmafSegmentLengthControlType,
    CmafStreamInfResolutionType,
    CmafTargetDurationCompatibilityModeType,
    CmafVideoCompositionOffsetsType,
    CmafWriteDASHManifestType,
    CmafWriteHLSManifestType,
    CmafWriteSegmentTimelineInRepresentationType,
    CmfcAudioDurationType,
    CmfcAudioTrackTypeType,
    CmfcDescriptiveVideoServiceFlagType,
    CmfcIFrameOnlyManifestType,
    CmfcKlvMetadataType,
    CmfcManifestMetadataSignalingType,
    CmfcScte35EsamType,
    CmfcScte35SourceType,
    CmfcTimedMetadataBoxVersionType,
    CmfcTimedMetadataType,
    ColorMetadataType,
    ColorSpaceConversionType,
    ColorSpaceType,
    ColorSpaceUsageType,
    ContainerTypeType,
    CopyProtectionActionType,
    DashIsoGroupAudioChannelConfigSchemeIdUriType,
    DashIsoHbbtvComplianceType,
    DashIsoImageBasedTrickPlayType,
    DashIsoIntervalCadenceType,
    DashIsoMpdManifestBandwidthTypeType,
    DashIsoMpdProfileType,
    DashIsoPlaybackDeviceCompatibilityType,
    DashIsoPtsOffsetHandlingForBFramesType,
    DashIsoSegmentControlType,
    DashIsoSegmentLengthControlType,
    DashIsoVideoCompositionOffsetsType,
    DashIsoWriteSegmentTimelineInRepresentationType,
    DashManifestStyleType,
    DecryptionModeType,
    DeinterlaceAlgorithmType,
    DeinterlacerControlType,
    DeinterlacerModeType,
    DescribeEndpointsModeType,
    DolbyVisionLevel6ModeType,
    DolbyVisionMappingType,
    DolbyVisionProfileType,
    DropFrameTimecodeType,
    DvbddsHandlingType,
    DvbSubSubtitleFallbackFontType,
    DvbSubtitleAlignmentType,
    DvbSubtitleApplyFontColorType,
    DvbSubtitleBackgroundColorType,
    DvbSubtitleFontColorType,
    DvbSubtitleOutlineColorType,
    DvbSubtitleShadowColorType,
    DvbSubtitleStylePassthroughType,
    DvbSubtitleTeletextSpacingType,
    DvbSubtitlingTypeType,
    Eac3AtmosCodingModeType,
    Eac3AtmosDialogueIntelligenceType,
    Eac3AtmosDownmixControlType,
    Eac3AtmosDynamicRangeCompressionLineType,
    Eac3AtmosDynamicRangeCompressionRfType,
    Eac3AtmosDynamicRangeControlType,
    Eac3AtmosMeteringModeType,
    Eac3AtmosStereoDownmixType,
    Eac3AtmosSurroundExModeType,
    Eac3AttenuationControlType,
    Eac3BitstreamModeType,
    Eac3CodingModeType,
    Eac3DcFilterType,
    Eac3DynamicRangeCompressionLineType,
    Eac3DynamicRangeCompressionRfType,
    Eac3LfeControlType,
    Eac3LfeFilterType,
    Eac3MetadataControlType,
    Eac3PassthroughControlType,
    Eac3PhaseControlType,
    Eac3StereoDownmixType,
    Eac3SurroundExModeType,
    Eac3SurroundModeType,
    EmbeddedConvert608To708Type,
    EmbeddedTerminateCaptionsType,
    EmbeddedTimecodeOverrideType,
    F4vMoovPlacementType,
    FileSourceConvert608To708Type,
    FileSourceTimeDeltaUnitsType,
    FontScriptType,
    H264AdaptiveQuantizationType,
    H264CodecLevelType,
    H264CodecProfileType,
    H264DynamicSubGopType,
    H264EntropyEncodingType,
    H264FieldEncodingType,
    H264FlickerAdaptiveQuantizationType,
    H264FramerateControlType,
    H264FramerateConversionAlgorithmType,
    H264GopBReferenceType,
    H264GopSizeUnitsType,
    H264InterlaceModeType,
    H264ParControlType,
    H264QualityTuningLevelType,
    H264RateControlModeType,
    H264RepeatPpsType,
    H264ScanTypeConversionModeType,
    H264SceneChangeDetectType,
    H264SlowPalType,
    H264SpatialAdaptiveQuantizationType,
    H264SyntaxType,
    H264TelecineType,
    H264TemporalAdaptiveQuantizationType,
    H264UnregisteredSeiTimecodeType,
    H265AdaptiveQuantizationType,
    H265AlternateTransferFunctionSeiType,
    H265CodecLevelType,
    H265CodecProfileType,
    H265DynamicSubGopType,
    H265FlickerAdaptiveQuantizationType,
    H265FramerateControlType,
    H265FramerateConversionAlgorithmType,
    H265GopBReferenceType,
    H265GopSizeUnitsType,
    H265InterlaceModeType,
    H265ParControlType,
    H265QualityTuningLevelType,
    H265RateControlModeType,
    H265SampleAdaptiveOffsetFilterModeType,
    H265ScanTypeConversionModeType,
    H265SceneChangeDetectType,
    H265SlowPalType,
    H265SpatialAdaptiveQuantizationType,
    H265TelecineType,
    H265TemporalAdaptiveQuantizationType,
    H265TemporalIdsType,
    H265TilesType,
    H265UnregisteredSeiTimecodeType,
    H265WriteMp4PackagingTypeType,
    HDRToSDRToneMapperType,
    HlsAdMarkersType,
    HlsAudioOnlyContainerType,
    HlsAudioOnlyHeaderType,
    HlsAudioTrackTypeType,
    HlsCaptionLanguageSettingType,
    HlsCaptionSegmentLengthControlType,
    HlsClientCacheType,
    HlsCodecSpecificationType,
    HlsDescriptiveVideoServiceFlagType,
    HlsDirectoryStructureType,
    HlsEncryptionTypeType,
    HlsIFrameOnlyManifestType,
    HlsImageBasedTrickPlayType,
    HlsInitializationVectorInManifestType,
    HlsIntervalCadenceType,
    HlsKeyProviderTypeType,
    HlsManifestCompressionType,
    HlsManifestDurationFormatType,
    HlsOfflineEncryptedType,
    HlsOutputSelectionType,
    HlsProgramDateTimeType,
    HlsProgressiveWriteHlsManifestType,
    HlsSegmentControlType,
    HlsSegmentLengthControlType,
    HlsStreamInfResolutionType,
    HlsTargetDurationCompatibilityModeType,
    HlsTimedMetadataId3FrameType,
    ImscAccessibilitySubsType,
    ImscStylePassthroughType,
    InputDeblockFilterType,
    InputDenoiseFilterType,
    InputFilterEnableType,
    InputPolicyType,
    InputPsiControlType,
    InputRotateType,
    InputSampleRangeType,
    InputScanTypeType,
    InputTimecodeSourceType,
    JobPhaseType,
    JobStatusType,
    JobTemplateListByType,
    LanguageCodeType,
    M2tsAudioBufferModelType,
    M2tsAudioDurationType,
    M2tsBufferModelType,
    M2tsDataPtsControlType,
    M2tsEbpAudioIntervalType,
    M2tsEbpPlacementType,
    M2tsEsRateInPesType,
    M2tsForceTsVideoEbpOrderType,
    M2tsKlvMetadataType,
    M2tsNielsenId3Type,
    M2tsPcrControlType,
    M2tsRateModeType,
    M2tsScte35SourceType,
    M2tsSegmentationMarkersType,
    M2tsSegmentationStyleType,
    M3u8AudioDurationType,
    M3u8DataPtsControlType,
    M3u8NielsenId3Type,
    M3u8PcrControlType,
    M3u8Scte35SourceType,
    MotionImageInsertionModeType,
    MotionImagePlaybackType,
    MovClapAtomType,
    MovCslgAtomType,
    MovMpeg2FourCCControlType,
    MovPaddingControlType,
    MovReferenceType,
    Mp3RateControlModeType,
    Mp4CslgAtomType,
    Mp4FreeSpaceBoxType,
    Mp4MoovPlacementType,
    MpdAccessibilityCaptionHintsType,
    MpdAudioDurationType,
    MpdCaptionContainerTypeType,
    MpdKlvMetadataType,
    MpdManifestMetadataSignalingType,
    MpdScte35EsamType,
    MpdScte35SourceType,
    MpdTimedMetadataBoxVersionType,
    MpdTimedMetadataType,
    Mpeg2AdaptiveQuantizationType,
    Mpeg2CodecLevelType,
    Mpeg2CodecProfileType,
    Mpeg2DynamicSubGopType,
    Mpeg2FramerateControlType,
    Mpeg2FramerateConversionAlgorithmType,
    Mpeg2GopSizeUnitsType,
    Mpeg2InterlaceModeType,
    Mpeg2IntraDcPrecisionType,
    Mpeg2ParControlType,
    Mpeg2QualityTuningLevelType,
    Mpeg2RateControlModeType,
    Mpeg2ScanTypeConversionModeType,
    Mpeg2SceneChangeDetectType,
    Mpeg2SlowPalType,
    Mpeg2SpatialAdaptiveQuantizationType,
    Mpeg2SyntaxType,
    Mpeg2TelecineType,
    Mpeg2TemporalAdaptiveQuantizationType,
    MsSmoothAudioDeduplicationType,
    MsSmoothFragmentLengthControlType,
    MsSmoothManifestEncodingType,
    MxfAfdSignalingType,
    MxfProfileType,
    MxfXavcDurationModeType,
    NielsenActiveWatermarkProcessTypeType,
    NielsenSourceWatermarkStatusTypeType,
    NielsenUniqueTicPerAudioTrackTypeType,
    NoiseFilterPostTemporalSharpeningStrengthType,
    NoiseFilterPostTemporalSharpeningType,
    NoiseReducerFilterType,
    OrderType,
    OutputGroupTypeType,
    OutputSdtType,
    PadVideoType,
    PresetListByType,
    PricingPlanType,
    ProresChromaSamplingType,
    ProresCodecProfileType,
    ProresFramerateControlType,
    ProresFramerateConversionAlgorithmType,
    ProresInterlaceModeType,
    ProresParControlType,
    ProresScanTypeConversionModeType,
    ProresSlowPalType,
    ProresTelecineType,
    QueueListByType,
    QueueStatusType,
    RenewalTypeType,
    RequiredFlagType,
    ReservationPlanStatusType,
    RespondToAfdType,
    RuleTypeType,
    S3ObjectCannedAclType,
    S3ServerSideEncryptionTypeType,
    S3StorageClassType,
    SampleRangeConversionType,
    ScalingBehaviorType,
    SccDestinationFramerateType,
    SimulateReservedQueueType,
    SrtStylePassthroughType,
    StatusUpdateIntervalType,
    TeletextPageTypeType,
    TimecodeBurninPositionType,
    TimecodeSourceType,
    TimedMetadataType,
    TsPtsOffsetType,
    TtmlStylePassthroughType,
    TypeType,
    Vc3ClassType,
    Vc3FramerateControlType,
    Vc3FramerateConversionAlgorithmType,
    Vc3InterlaceModeType,
    Vc3ScanTypeConversionModeType,
    Vc3SlowPalType,
    Vc3TelecineType,
    VchipActionType,
    VideoCodecType,
    VideoTimecodeInsertionType,
    Vp8FramerateControlType,
    Vp8FramerateConversionAlgorithmType,
    Vp8ParControlType,
    Vp8QualityTuningLevelType,
    Vp9FramerateControlType,
    Vp9FramerateConversionAlgorithmType,
    Vp9ParControlType,
    Vp9QualityTuningLevelType,
    WatermarkingStrengthType,
    WavFormatType,
    WebvttAccessibilitySubsType,
    WebvttStylePassthroughType,
    Xavc4kIntraCbgProfileClassType,
    Xavc4kIntraVbrProfileClassType,
    Xavc4kProfileBitrateClassType,
    Xavc4kProfileCodecProfileType,
    Xavc4kProfileQualityTuningLevelType,
    XavcAdaptiveQuantizationType,
    XavcEntropyEncodingType,
    XavcFlickerAdaptiveQuantizationType,
    XavcFramerateControlType,
    XavcFramerateConversionAlgorithmType,
    XavcGopBReferenceType,
    XavcHdIntraCbgProfileClassType,
    XavcHdProfileBitrateClassType,
    XavcHdProfileQualityTuningLevelType,
    XavcHdProfileTelecineType,
    XavcInterlaceModeType,
    XavcProfileType,
    XavcSlowPalType,
    XavcSpatialAdaptiveQuantizationType,
    XavcTemporalAdaptiveQuantizationType,
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
    "AacSettingsTypeDef",
    "Ac3SettingsTypeDef",
    "AccelerationSettingsTypeDef",
    "AdvancedInputFilterSettingsTypeDef",
    "AiffSettingsTypeDef",
    "AllowedRenditionSizeTypeDef",
    "AncillarySourceSettingsTypeDef",
    "AssociateCertificateRequestRequestTypeDef",
    "AudioChannelTaggingSettingsTypeDef",
    "Eac3AtmosSettingsTypeDef",
    "Eac3SettingsTypeDef",
    "FlacSettingsTypeDef",
    "Mp2SettingsTypeDef",
    "Mp3SettingsTypeDef",
    "OpusSettingsTypeDef",
    "VorbisSettingsTypeDef",
    "WavSettingsTypeDef",
    "AudioNormalizationSettingsTypeDef",
    "AudioSelectorGroupPaginatorTypeDef",
    "AudioSelectorGroupTypeDef",
    "HlsRenditionGroupSettingsTypeDef",
    "ForceIncludeRenditionSizeTypeDef",
    "MinBottomRenditionSizeTypeDef",
    "MinTopRenditionSizeTypeDef",
    "Av1QvbrSettingsTypeDef",
    "AvailBlankingTypeDef",
    "AvcIntraUhdSettingsTypeDef",
    "BandwidthReductionFilterTypeDef",
    "BurninDestinationSettingsTypeDef",
    "CancelJobRequestRequestTypeDef",
    "DvbSubDestinationSettingsTypeDef",
    "EmbeddedDestinationSettingsTypeDef",
    "ImscDestinationSettingsTypeDef",
    "SccDestinationSettingsTypeDef",
    "SrtDestinationSettingsTypeDef",
    "TeletextDestinationSettingsPaginatorTypeDef",
    "TtmlDestinationSettingsTypeDef",
    "WebvttDestinationSettingsTypeDef",
    "TeletextDestinationSettingsTypeDef",
    "CaptionSourceFramerateTypeDef",
    "DvbSubSourceSettingsTypeDef",
    "EmbeddedSourceSettingsTypeDef",
    "TeletextSourceSettingsTypeDef",
    "TrackSourceSettingsTypeDef",
    "WebvttHlsSourceSettingsTypeDef",
    "OutputChannelMappingPaginatorTypeDef",
    "OutputChannelMappingTypeDef",
    "ClipLimitsTypeDef",
    "CmafAdditionalManifestPaginatorTypeDef",
    "CmafAdditionalManifestTypeDef",
    "SpekeKeyProviderCmafPaginatorTypeDef",
    "StaticKeyProviderTypeDef",
    "SpekeKeyProviderCmafTypeDef",
    "CmafImageBasedTrickPlaySettingsTypeDef",
    "CmfcSettingsTypeDef",
    "Hdr10MetadataTypeDef",
    "F4vSettingsTypeDef",
    "M3u8SettingsPaginatorTypeDef",
    "MovSettingsTypeDef",
    "Mp4SettingsTypeDef",
    "MpdSettingsTypeDef",
    "M3u8SettingsTypeDef",
    "HopDestinationTypeDef",
    "ResponseMetadataTypeDef",
    "ReservationPlanSettingsTypeDef",
    "DashAdditionalManifestPaginatorTypeDef",
    "DashAdditionalManifestTypeDef",
    "SpekeKeyProviderPaginatorTypeDef",
    "SpekeKeyProviderTypeDef",
    "DashIsoImageBasedTrickPlaySettingsTypeDef",
    "DeinterlacerTypeDef",
    "DeleteJobTemplateRequestRequestTypeDef",
    "DeletePresetRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeEndpointsRequestRequestTypeDef",
    "EndpointTypeDef",
    "DisassociateCertificateRequestRequestTypeDef",
    "DolbyVisionLevel6MetadataTypeDef",
    "DvbNitSettingsTypeDef",
    "DvbSdtSettingsTypeDef",
    "DvbTdtSettingsTypeDef",
    "EsamManifestConfirmConditionNotificationTypeDef",
    "EsamSignalProcessingNotificationTypeDef",
    "ExtendedDataServicesTypeDef",
    "FrameCaptureSettingsTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobTemplateRequestRequestTypeDef",
    "PolicyTypeDef",
    "GetPresetRequestRequestTypeDef",
    "GetQueueRequestRequestTypeDef",
    "H264QvbrSettingsTypeDef",
    "H265QvbrSettingsTypeDef",
    "Hdr10PlusTypeDef",
    "HlsAdditionalManifestPaginatorTypeDef",
    "HlsAdditionalManifestTypeDef",
    "HlsCaptionLanguageMappingTypeDef",
    "HlsImageBasedTrickPlaySettingsTypeDef",
    "HlsSettingsTypeDef",
    "Id3InsertionTypeDef",
    "InsertableImageTypeDef",
    "InputClippingTypeDef",
    "InputDecryptionSettingsTypeDef",
    "InputVideoGeneratorTypeDef",
    "RectangleTypeDef",
    "JobMessagesTypeDef",
    "QueueTransitionTypeDef",
    "TimingTypeDef",
    "WarningGroupTypeDef",
    "KantarWatermarkSettingsTypeDef",
    "NielsenConfigurationTypeDef",
    "NielsenNonLinearWatermarkSettingsTypeDef",
    "TimecodeConfigTypeDef",
    "ListJobTemplatesRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListPresetsRequestRequestTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResourceTagsTypeDef",
    "M2tsScte35EsamTypeDef",
    "MotionImageInsertionFramerateTypeDef",
    "MotionImageInsertionOffsetTypeDef",
    "Mpeg2SettingsTypeDef",
    "MsSmoothAdditionalManifestPaginatorTypeDef",
    "MsSmoothAdditionalManifestTypeDef",
    "MxfXavcProfileSettingsTypeDef",
    "NexGuardFileMarkerSettingsTypeDef",
    "NoiseReducerFilterSettingsTypeDef",
    "NoiseReducerSpatialFilterSettingsTypeDef",
    "NoiseReducerTemporalFilterSettingsTypeDef",
    "VideoDetailTypeDef",
    "ProresSettingsTypeDef",
    "ReservationPlanTypeDef",
    "S3DestinationAccessControlTypeDef",
    "S3EncryptionSettingsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimecodeBurninTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "Vc3SettingsTypeDef",
    "Vp8SettingsTypeDef",
    "Vp9SettingsTypeDef",
    "Xavc4kIntraCbgProfileSettingsTypeDef",
    "Xavc4kIntraVbrProfileSettingsTypeDef",
    "Xavc4kProfileSettingsTypeDef",
    "XavcHdIntraCbgProfileSettingsTypeDef",
    "XavcHdProfileSettingsTypeDef",
    "AudioCodecSettingsTypeDef",
    "AutomatedAbrRulePaginatorTypeDef",
    "AutomatedAbrRuleTypeDef",
    "Av1SettingsTypeDef",
    "AvcIntraSettingsTypeDef",
    "CaptionDestinationSettingsPaginatorTypeDef",
    "CaptionDestinationSettingsTypeDef",
    "FileSourceSettingsTypeDef",
    "ChannelMappingPaginatorTypeDef",
    "ChannelMappingTypeDef",
    "CmafEncryptionSettingsPaginatorTypeDef",
    "CmafEncryptionSettingsTypeDef",
    "ColorCorrectorTypeDef",
    "VideoSelectorTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "UpdateQueueRequestRequestTypeDef",
    "DashIsoEncryptionSettingsPaginatorTypeDef",
    "HlsEncryptionSettingsPaginatorTypeDef",
    "MsSmoothEncryptionSettingsPaginatorTypeDef",
    "DashIsoEncryptionSettingsTypeDef",
    "HlsEncryptionSettingsTypeDef",
    "MsSmoothEncryptionSettingsTypeDef",
    "DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef",
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListPresetsRequestListPresetsPaginateTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DolbyVisionTypeDef",
    "EsamSettingsTypeDef",
    "GetPolicyResponseTypeDef",
    "PutPolicyRequestRequestTypeDef",
    "PutPolicyResponseTypeDef",
    "H264SettingsTypeDef",
    "H265SettingsTypeDef",
    "OutputSettingsTypeDef",
    "TimedMetadataInsertionPaginatorTypeDef",
    "TimedMetadataInsertionTypeDef",
    "ImageInserterPaginatorTypeDef",
    "ImageInserterTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "M2tsSettingsPaginatorTypeDef",
    "M2tsSettingsTypeDef",
    "MotionImageInserterTypeDef",
    "MxfSettingsTypeDef",
    "PartnerWatermarkingTypeDef",
    "NoiseReducerTypeDef",
    "OutputDetailTypeDef",
    "QueueTypeDef",
    "S3DestinationSettingsTypeDef",
    "XavcSettingsTypeDef",
    "AutomatedAbrSettingsPaginatorTypeDef",
    "AutomatedAbrSettingsTypeDef",
    "CaptionDescriptionPaginatorTypeDef",
    "CaptionDescriptionPresetPaginatorTypeDef",
    "CaptionDescriptionPresetTypeDef",
    "CaptionDescriptionTypeDef",
    "CaptionSourceSettingsTypeDef",
    "RemixSettingsPaginatorTypeDef",
    "RemixSettingsTypeDef",
    "ContainerSettingsPaginatorTypeDef",
    "ContainerSettingsTypeDef",
    "VideoPreprocessorPaginatorTypeDef",
    "VideoPreprocessorTypeDef",
    "OutputGroupDetailTypeDef",
    "CreateQueueResponseTypeDef",
    "GetQueueResponseTypeDef",
    "ListQueuesResponseTypeDef",
    "UpdateQueueResponseTypeDef",
    "DestinationSettingsTypeDef",
    "VideoCodecSettingsTypeDef",
    "AutomatedEncodingSettingsPaginatorTypeDef",
    "AutomatedEncodingSettingsTypeDef",
    "CaptionSelectorTypeDef",
    "AudioDescriptionPaginatorTypeDef",
    "AudioSelectorPaginatorTypeDef",
    "AudioDescriptionTypeDef",
    "AudioSelectorTypeDef",
    "CmafGroupSettingsPaginatorTypeDef",
    "CmafGroupSettingsTypeDef",
    "DashIsoGroupSettingsPaginatorTypeDef",
    "DashIsoGroupSettingsTypeDef",
    "FileGroupSettingsTypeDef",
    "HlsGroupSettingsPaginatorTypeDef",
    "HlsGroupSettingsTypeDef",
    "MsSmoothGroupSettingsPaginatorTypeDef",
    "MsSmoothGroupSettingsTypeDef",
    "VideoDescriptionPaginatorTypeDef",
    "VideoDescriptionTypeDef",
    "InputPaginatorTypeDef",
    "InputTemplatePaginatorTypeDef",
    "InputTemplateTypeDef",
    "InputTypeDef",
    "OutputGroupSettingsPaginatorTypeDef",
    "OutputGroupSettingsTypeDef",
    "OutputPaginatorTypeDef",
    "PresetSettingsPaginatorTypeDef",
    "OutputTypeDef",
    "PresetSettingsTypeDef",
    "OutputGroupPaginatorTypeDef",
    "PresetPaginatorTypeDef",
    "OutputGroupTypeDef",
    "CreatePresetRequestRequestTypeDef",
    "PresetTypeDef",
    "UpdatePresetRequestRequestTypeDef",
    "JobSettingsPaginatorTypeDef",
    "JobTemplateSettingsPaginatorTypeDef",
    "ListPresetsResponsePaginatorTypeDef",
    "JobSettingsTypeDef",
    "JobTemplateSettingsTypeDef",
    "CreatePresetResponseTypeDef",
    "GetPresetResponseTypeDef",
    "ListPresetsResponseTypeDef",
    "UpdatePresetResponseTypeDef",
    "JobPaginatorTypeDef",
    "JobTemplatePaginatorTypeDef",
    "CreateJobRequestRequestTypeDef",
    "JobTypeDef",
    "CreateJobTemplateRequestRequestTypeDef",
    "JobTemplateTypeDef",
    "UpdateJobTemplateRequestRequestTypeDef",
    "ListJobsResponsePaginatorTypeDef",
    "ListJobTemplatesResponsePaginatorTypeDef",
    "CreateJobResponseTypeDef",
    "GetJobResponseTypeDef",
    "ListJobsResponseTypeDef",
    "CreateJobTemplateResponseTypeDef",
    "GetJobTemplateResponseTypeDef",
    "ListJobTemplatesResponseTypeDef",
    "UpdateJobTemplateResponseTypeDef",
)

AacSettingsTypeDef = TypedDict(
    "AacSettingsTypeDef",
    {
        "AudioDescriptionBroadcasterMix": AacAudioDescriptionBroadcasterMixType,
        "Bitrate": int,
        "CodecProfile": AacCodecProfileType,
        "CodingMode": AacCodingModeType,
        "RateControlMode": AacRateControlModeType,
        "RawFormat": AacRawFormatType,
        "SampleRate": int,
        "Specification": AacSpecificationType,
        "VbrQuality": AacVbrQualityType,
    },
    total=False,
)

Ac3SettingsTypeDef = TypedDict(
    "Ac3SettingsTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Ac3BitstreamModeType,
        "CodingMode": Ac3CodingModeType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Ac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionProfile": Ac3DynamicRangeCompressionProfileType,
        "DynamicRangeCompressionRf": Ac3DynamicRangeCompressionRfType,
        "LfeFilter": Ac3LfeFilterType,
        "MetadataControl": Ac3MetadataControlType,
        "SampleRate": int,
    },
    total=False,
)

AccelerationSettingsTypeDef = TypedDict(
    "AccelerationSettingsTypeDef",
    {
        "Mode": AccelerationModeType,
    },
)

AdvancedInputFilterSettingsTypeDef = TypedDict(
    "AdvancedInputFilterSettingsTypeDef",
    {
        "AddTexture": AdvancedInputFilterAddTextureType,
        "Sharpening": AdvancedInputFilterSharpenType,
    },
    total=False,
)

AiffSettingsTypeDef = TypedDict(
    "AiffSettingsTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

AllowedRenditionSizeTypeDef = TypedDict(
    "AllowedRenditionSizeTypeDef",
    {
        "Height": int,
        "Required": RequiredFlagType,
        "Width": int,
    },
    total=False,
)

AncillarySourceSettingsTypeDef = TypedDict(
    "AncillarySourceSettingsTypeDef",
    {
        "Convert608To708": AncillaryConvert608To708Type,
        "SourceAncillaryChannelNumber": int,
        "TerminateCaptions": AncillaryTerminateCaptionsType,
    },
    total=False,
)

AssociateCertificateRequestRequestTypeDef = TypedDict(
    "AssociateCertificateRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

AudioChannelTaggingSettingsTypeDef = TypedDict(
    "AudioChannelTaggingSettingsTypeDef",
    {
        "ChannelTag": AudioChannelTagType,
    },
    total=False,
)

Eac3AtmosSettingsTypeDef = TypedDict(
    "Eac3AtmosSettingsTypeDef",
    {
        "Bitrate": int,
        "BitstreamMode": Literal["COMPLETE_MAIN"],
        "CodingMode": Eac3AtmosCodingModeType,
        "DialogueIntelligence": Eac3AtmosDialogueIntelligenceType,
        "DownmixControl": Eac3AtmosDownmixControlType,
        "DynamicRangeCompressionLine": Eac3AtmosDynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3AtmosDynamicRangeCompressionRfType,
        "DynamicRangeControl": Eac3AtmosDynamicRangeControlType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MeteringMode": Eac3AtmosMeteringModeType,
        "SampleRate": int,
        "SpeechThreshold": int,
        "StereoDownmix": Eac3AtmosStereoDownmixType,
        "SurroundExMode": Eac3AtmosSurroundExModeType,
    },
    total=False,
)

Eac3SettingsTypeDef = TypedDict(
    "Eac3SettingsTypeDef",
    {
        "AttenuationControl": Eac3AttenuationControlType,
        "Bitrate": int,
        "BitstreamMode": Eac3BitstreamModeType,
        "CodingMode": Eac3CodingModeType,
        "DcFilter": Eac3DcFilterType,
        "Dialnorm": int,
        "DynamicRangeCompressionLine": Eac3DynamicRangeCompressionLineType,
        "DynamicRangeCompressionRf": Eac3DynamicRangeCompressionRfType,
        "LfeControl": Eac3LfeControlType,
        "LfeFilter": Eac3LfeFilterType,
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MetadataControl": Eac3MetadataControlType,
        "PassthroughControl": Eac3PassthroughControlType,
        "PhaseControl": Eac3PhaseControlType,
        "SampleRate": int,
        "StereoDownmix": Eac3StereoDownmixType,
        "SurroundExMode": Eac3SurroundExModeType,
        "SurroundMode": Eac3SurroundModeType,
    },
    total=False,
)

FlacSettingsTypeDef = TypedDict(
    "FlacSettingsTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

Mp2SettingsTypeDef = TypedDict(
    "Mp2SettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

Mp3SettingsTypeDef = TypedDict(
    "Mp3SettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "RateControlMode": Mp3RateControlModeType,
        "SampleRate": int,
        "VbrQuality": int,
    },
    total=False,
)

OpusSettingsTypeDef = TypedDict(
    "OpusSettingsTypeDef",
    {
        "Bitrate": int,
        "Channels": int,
        "SampleRate": int,
    },
    total=False,
)

VorbisSettingsTypeDef = TypedDict(
    "VorbisSettingsTypeDef",
    {
        "Channels": int,
        "SampleRate": int,
        "VbrQuality": int,
    },
    total=False,
)

WavSettingsTypeDef = TypedDict(
    "WavSettingsTypeDef",
    {
        "BitDepth": int,
        "Channels": int,
        "Format": WavFormatType,
        "SampleRate": int,
    },
    total=False,
)

AudioNormalizationSettingsTypeDef = TypedDict(
    "AudioNormalizationSettingsTypeDef",
    {
        "Algorithm": AudioNormalizationAlgorithmType,
        "AlgorithmControl": AudioNormalizationAlgorithmControlType,
        "CorrectionGateLevel": int,
        "LoudnessLogging": AudioNormalizationLoudnessLoggingType,
        "PeakCalculation": AudioNormalizationPeakCalculationType,
        "TargetLkfs": float,
        "TruePeakLimiterThreshold": float,
    },
    total=False,
)

AudioSelectorGroupPaginatorTypeDef = TypedDict(
    "AudioSelectorGroupPaginatorTypeDef",
    {
        "AudioSelectorNames": List[str],
    },
    total=False,
)

AudioSelectorGroupTypeDef = TypedDict(
    "AudioSelectorGroupTypeDef",
    {
        "AudioSelectorNames": Sequence[str],
    },
    total=False,
)

HlsRenditionGroupSettingsTypeDef = TypedDict(
    "HlsRenditionGroupSettingsTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
    total=False,
)

ForceIncludeRenditionSizeTypeDef = TypedDict(
    "ForceIncludeRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

MinBottomRenditionSizeTypeDef = TypedDict(
    "MinBottomRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

MinTopRenditionSizeTypeDef = TypedDict(
    "MinTopRenditionSizeTypeDef",
    {
        "Height": int,
        "Width": int,
    },
    total=False,
)

Av1QvbrSettingsTypeDef = TypedDict(
    "Av1QvbrSettingsTypeDef",
    {
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

AvailBlankingTypeDef = TypedDict(
    "AvailBlankingTypeDef",
    {
        "AvailBlankingImage": str,
    },
    total=False,
)

AvcIntraUhdSettingsTypeDef = TypedDict(
    "AvcIntraUhdSettingsTypeDef",
    {
        "QualityTuningLevel": AvcIntraUhdQualityTuningLevelType,
    },
    total=False,
)

BandwidthReductionFilterTypeDef = TypedDict(
    "BandwidthReductionFilterTypeDef",
    {
        "Sharpening": BandwidthReductionFilterSharpeningType,
        "Strength": BandwidthReductionFilterStrengthType,
    },
    total=False,
)

BurninDestinationSettingsTypeDef = TypedDict(
    "BurninDestinationSettingsTypeDef",
    {
        "Alignment": BurninSubtitleAlignmentType,
        "ApplyFontColor": BurninSubtitleApplyFontColorType,
        "BackgroundColor": BurninSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "FallbackFont": BurninSubtitleFallbackFontType,
        "FontColor": BurninSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "HexFontColor": str,
        "OutlineColor": BurninSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": BurninSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": BurnInSubtitleStylePassthroughType,
        "TeletextSpacing": BurninSubtitleTeletextSpacingType,
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DvbSubDestinationSettingsTypeDef = TypedDict(
    "DvbSubDestinationSettingsTypeDef",
    {
        "Alignment": DvbSubtitleAlignmentType,
        "ApplyFontColor": DvbSubtitleApplyFontColorType,
        "BackgroundColor": DvbSubtitleBackgroundColorType,
        "BackgroundOpacity": int,
        "DdsHandling": DvbddsHandlingType,
        "DdsXCoordinate": int,
        "DdsYCoordinate": int,
        "FallbackFont": DvbSubSubtitleFallbackFontType,
        "FontColor": DvbSubtitleFontColorType,
        "FontOpacity": int,
        "FontResolution": int,
        "FontScript": FontScriptType,
        "FontSize": int,
        "Height": int,
        "HexFontColor": str,
        "OutlineColor": DvbSubtitleOutlineColorType,
        "OutlineSize": int,
        "ShadowColor": DvbSubtitleShadowColorType,
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "StylePassthrough": DvbSubtitleStylePassthroughType,
        "SubtitlingType": DvbSubtitlingTypeType,
        "TeletextSpacing": DvbSubtitleTeletextSpacingType,
        "Width": int,
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

EmbeddedDestinationSettingsTypeDef = TypedDict(
    "EmbeddedDestinationSettingsTypeDef",
    {
        "Destination608ChannelNumber": int,
        "Destination708ServiceNumber": int,
    },
    total=False,
)

ImscDestinationSettingsTypeDef = TypedDict(
    "ImscDestinationSettingsTypeDef",
    {
        "Accessibility": ImscAccessibilitySubsType,
        "StylePassthrough": ImscStylePassthroughType,
    },
    total=False,
)

SccDestinationSettingsTypeDef = TypedDict(
    "SccDestinationSettingsTypeDef",
    {
        "Framerate": SccDestinationFramerateType,
    },
    total=False,
)

SrtDestinationSettingsTypeDef = TypedDict(
    "SrtDestinationSettingsTypeDef",
    {
        "StylePassthrough": SrtStylePassthroughType,
    },
    total=False,
)

TeletextDestinationSettingsPaginatorTypeDef = TypedDict(
    "TeletextDestinationSettingsPaginatorTypeDef",
    {
        "PageNumber": str,
        "PageTypes": List[TeletextPageTypeType],
    },
    total=False,
)

TtmlDestinationSettingsTypeDef = TypedDict(
    "TtmlDestinationSettingsTypeDef",
    {
        "StylePassthrough": TtmlStylePassthroughType,
    },
    total=False,
)

WebvttDestinationSettingsTypeDef = TypedDict(
    "WebvttDestinationSettingsTypeDef",
    {
        "Accessibility": WebvttAccessibilitySubsType,
        "StylePassthrough": WebvttStylePassthroughType,
    },
    total=False,
)

TeletextDestinationSettingsTypeDef = TypedDict(
    "TeletextDestinationSettingsTypeDef",
    {
        "PageNumber": str,
        "PageTypes": Sequence[TeletextPageTypeType],
    },
    total=False,
)

CaptionSourceFramerateTypeDef = TypedDict(
    "CaptionSourceFramerateTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
    total=False,
)

DvbSubSourceSettingsTypeDef = TypedDict(
    "DvbSubSourceSettingsTypeDef",
    {
        "Pid": int,
    },
    total=False,
)

EmbeddedSourceSettingsTypeDef = TypedDict(
    "EmbeddedSourceSettingsTypeDef",
    {
        "Convert608To708": EmbeddedConvert608To708Type,
        "Source608ChannelNumber": int,
        "Source608TrackNumber": int,
        "TerminateCaptions": EmbeddedTerminateCaptionsType,
    },
    total=False,
)

TeletextSourceSettingsTypeDef = TypedDict(
    "TeletextSourceSettingsTypeDef",
    {
        "PageNumber": str,
    },
    total=False,
)

TrackSourceSettingsTypeDef = TypedDict(
    "TrackSourceSettingsTypeDef",
    {
        "TrackNumber": int,
    },
    total=False,
)

WebvttHlsSourceSettingsTypeDef = TypedDict(
    "WebvttHlsSourceSettingsTypeDef",
    {
        "RenditionGroupId": str,
        "RenditionLanguageCode": LanguageCodeType,
        "RenditionName": str,
    },
    total=False,
)

OutputChannelMappingPaginatorTypeDef = TypedDict(
    "OutputChannelMappingPaginatorTypeDef",
    {
        "InputChannels": List[int],
        "InputChannelsFineTune": List[float],
    },
    total=False,
)

OutputChannelMappingTypeDef = TypedDict(
    "OutputChannelMappingTypeDef",
    {
        "InputChannels": Sequence[int],
        "InputChannelsFineTune": Sequence[float],
    },
    total=False,
)

ClipLimitsTypeDef = TypedDict(
    "ClipLimitsTypeDef",
    {
        "MaximumRGBTolerance": int,
        "MaximumYUV": int,
        "MinimumRGBTolerance": int,
        "MinimumYUV": int,
    },
    total=False,
)

CmafAdditionalManifestPaginatorTypeDef = TypedDict(
    "CmafAdditionalManifestPaginatorTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
    total=False,
)

CmafAdditionalManifestTypeDef = TypedDict(
    "CmafAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

SpekeKeyProviderCmafPaginatorTypeDef = TypedDict(
    "SpekeKeyProviderCmafPaginatorTypeDef",
    {
        "CertificateArn": str,
        "DashSignaledSystemIds": List[str],
        "HlsSignaledSystemIds": List[str],
        "ResourceId": str,
        "Url": str,
    },
    total=False,
)

StaticKeyProviderTypeDef = TypedDict(
    "StaticKeyProviderTypeDef",
    {
        "KeyFormat": str,
        "KeyFormatVersions": str,
        "StaticKeyValue": str,
        "Url": str,
    },
    total=False,
)

SpekeKeyProviderCmafTypeDef = TypedDict(
    "SpekeKeyProviderCmafTypeDef",
    {
        "CertificateArn": str,
        "DashSignaledSystemIds": Sequence[str],
        "HlsSignaledSystemIds": Sequence[str],
        "ResourceId": str,
        "Url": str,
    },
    total=False,
)

CmafImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "CmafImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": CmafIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

CmfcSettingsTypeDef = TypedDict(
    "CmfcSettingsTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "AudioGroupId": str,
        "AudioRenditionSets": str,
        "AudioTrackType": CmfcAudioTrackTypeType,
        "DescriptiveVideoServiceFlag": CmfcDescriptiveVideoServiceFlagType,
        "IFrameOnlyManifest": CmfcIFrameOnlyManifestType,
        "KlvMetadata": CmfcKlvMetadataType,
        "ManifestMetadataSignaling": CmfcManifestMetadataSignalingType,
        "Scte35Esam": CmfcScte35EsamType,
        "Scte35Source": CmfcScte35SourceType,
        "TimedMetadata": CmfcTimedMetadataType,
        "TimedMetadataBoxVersion": CmfcTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
    total=False,
)

Hdr10MetadataTypeDef = TypedDict(
    "Hdr10MetadataTypeDef",
    {
        "BluePrimaryX": int,
        "BluePrimaryY": int,
        "GreenPrimaryX": int,
        "GreenPrimaryY": int,
        "MaxContentLightLevel": int,
        "MaxFrameAverageLightLevel": int,
        "MaxLuminance": int,
        "MinLuminance": int,
        "RedPrimaryX": int,
        "RedPrimaryY": int,
        "WhitePointX": int,
        "WhitePointY": int,
    },
    total=False,
)

F4vSettingsTypeDef = TypedDict(
    "F4vSettingsTypeDef",
    {
        "MoovPlacement": F4vMoovPlacementType,
    },
    total=False,
)

M3u8SettingsPaginatorTypeDef = TypedDict(
    "M3u8SettingsPaginatorTypeDef",
    {
        "AudioDuration": M3u8AudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": List[int],
        "DataPTSControl": M3u8DataPtsControlType,
        "MaxPcrInterval": int,
        "NielsenId3": M3u8NielsenId3Type,
        "PatInterval": int,
        "PcrControl": M3u8PcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "PtsOffset": int,
        "PtsOffsetMode": TsPtsOffsetType,
        "Scte35Pid": int,
        "Scte35Source": M3u8Scte35SourceType,
        "TimedMetadata": TimedMetadataType,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

MovSettingsTypeDef = TypedDict(
    "MovSettingsTypeDef",
    {
        "ClapAtom": MovClapAtomType,
        "CslgAtom": MovCslgAtomType,
        "Mpeg2FourCCControl": MovMpeg2FourCCControlType,
        "PaddingControl": MovPaddingControlType,
        "Reference": MovReferenceType,
    },
    total=False,
)

Mp4SettingsTypeDef = TypedDict(
    "Mp4SettingsTypeDef",
    {
        "AudioDuration": CmfcAudioDurationType,
        "CslgAtom": Mp4CslgAtomType,
        "CttsVersion": int,
        "FreeSpaceBox": Mp4FreeSpaceBoxType,
        "MoovPlacement": Mp4MoovPlacementType,
        "Mp4MajorBrand": str,
    },
    total=False,
)

MpdSettingsTypeDef = TypedDict(
    "MpdSettingsTypeDef",
    {
        "AccessibilityCaptionHints": MpdAccessibilityCaptionHintsType,
        "AudioDuration": MpdAudioDurationType,
        "CaptionContainerType": MpdCaptionContainerTypeType,
        "KlvMetadata": MpdKlvMetadataType,
        "ManifestMetadataSignaling": MpdManifestMetadataSignalingType,
        "Scte35Esam": MpdScte35EsamType,
        "Scte35Source": MpdScte35SourceType,
        "TimedMetadata": MpdTimedMetadataType,
        "TimedMetadataBoxVersion": MpdTimedMetadataBoxVersionType,
        "TimedMetadataSchemeIdUri": str,
        "TimedMetadataValue": str,
    },
    total=False,
)

M3u8SettingsTypeDef = TypedDict(
    "M3u8SettingsTypeDef",
    {
        "AudioDuration": M3u8AudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": Sequence[int],
        "DataPTSControl": M3u8DataPtsControlType,
        "MaxPcrInterval": int,
        "NielsenId3": M3u8NielsenId3Type,
        "PatInterval": int,
        "PcrControl": M3u8PcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "PtsOffset": int,
        "PtsOffsetMode": TsPtsOffsetType,
        "Scte35Pid": int,
        "Scte35Source": M3u8Scte35SourceType,
        "TimedMetadata": TimedMetadataType,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

HopDestinationTypeDef = TypedDict(
    "HopDestinationTypeDef",
    {
        "Priority": int,
        "Queue": str,
        "WaitMinutes": int,
    },
    total=False,
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

ReservationPlanSettingsTypeDef = TypedDict(
    "ReservationPlanSettingsTypeDef",
    {
        "Commitment": Literal["ONE_YEAR"],
        "RenewalType": RenewalTypeType,
        "ReservedSlots": int,
    },
)

DashAdditionalManifestPaginatorTypeDef = TypedDict(
    "DashAdditionalManifestPaginatorTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
    total=False,
)

DashAdditionalManifestTypeDef = TypedDict(
    "DashAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

SpekeKeyProviderPaginatorTypeDef = TypedDict(
    "SpekeKeyProviderPaginatorTypeDef",
    {
        "CertificateArn": str,
        "ResourceId": str,
        "SystemIds": List[str],
        "Url": str,
    },
    total=False,
)

SpekeKeyProviderTypeDef = TypedDict(
    "SpekeKeyProviderTypeDef",
    {
        "CertificateArn": str,
        "ResourceId": str,
        "SystemIds": Sequence[str],
        "Url": str,
    },
    total=False,
)

DashIsoImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "DashIsoImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": DashIsoIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

DeinterlacerTypeDef = TypedDict(
    "DeinterlacerTypeDef",
    {
        "Algorithm": DeinterlaceAlgorithmType,
        "Control": DeinterlacerControlType,
        "Mode": DeinterlacerModeType,
    },
    total=False,
)

DeleteJobTemplateRequestRequestTypeDef = TypedDict(
    "DeleteJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeletePresetRequestRequestTypeDef = TypedDict(
    "DeletePresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteQueueRequestRequestTypeDef = TypedDict(
    "DeleteQueueRequestRequestTypeDef",
    {
        "Name": str,
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

DescribeEndpointsRequestRequestTypeDef = TypedDict(
    "DescribeEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "Mode": DescribeEndpointsModeType,
        "NextToken": str,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Url": str,
    },
    total=False,
)

DisassociateCertificateRequestRequestTypeDef = TypedDict(
    "DisassociateCertificateRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

DolbyVisionLevel6MetadataTypeDef = TypedDict(
    "DolbyVisionLevel6MetadataTypeDef",
    {
        "MaxCll": int,
        "MaxFall": int,
    },
    total=False,
)

DvbNitSettingsTypeDef = TypedDict(
    "DvbNitSettingsTypeDef",
    {
        "NetworkId": int,
        "NetworkName": str,
        "NitInterval": int,
    },
    total=False,
)

DvbSdtSettingsTypeDef = TypedDict(
    "DvbSdtSettingsTypeDef",
    {
        "OutputSdt": OutputSdtType,
        "SdtInterval": int,
        "ServiceName": str,
        "ServiceProviderName": str,
    },
    total=False,
)

DvbTdtSettingsTypeDef = TypedDict(
    "DvbTdtSettingsTypeDef",
    {
        "TdtInterval": int,
    },
    total=False,
)

EsamManifestConfirmConditionNotificationTypeDef = TypedDict(
    "EsamManifestConfirmConditionNotificationTypeDef",
    {
        "MccXml": str,
    },
    total=False,
)

EsamSignalProcessingNotificationTypeDef = TypedDict(
    "EsamSignalProcessingNotificationTypeDef",
    {
        "SccXml": str,
    },
    total=False,
)

ExtendedDataServicesTypeDef = TypedDict(
    "ExtendedDataServicesTypeDef",
    {
        "CopyProtectionAction": CopyProtectionActionType,
        "VchipAction": VchipActionType,
    },
    total=False,
)

FrameCaptureSettingsTypeDef = TypedDict(
    "FrameCaptureSettingsTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "MaxCaptures": int,
        "Quality": int,
    },
    total=False,
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetJobTemplateRequestRequestTypeDef = TypedDict(
    "GetJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "HttpInputs": InputPolicyType,
        "HttpsInputs": InputPolicyType,
        "S3Inputs": InputPolicyType,
    },
    total=False,
)

GetPresetRequestRequestTypeDef = TypedDict(
    "GetPresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetQueueRequestRequestTypeDef = TypedDict(
    "GetQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)

H264QvbrSettingsTypeDef = TypedDict(
    "H264QvbrSettingsTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

H265QvbrSettingsTypeDef = TypedDict(
    "H265QvbrSettingsTypeDef",
    {
        "MaxAverageBitrate": int,
        "QvbrQualityLevel": int,
        "QvbrQualityLevelFineTune": float,
    },
    total=False,
)

Hdr10PlusTypeDef = TypedDict(
    "Hdr10PlusTypeDef",
    {
        "MasteringMonitorNits": int,
        "TargetMonitorNits": int,
    },
    total=False,
)

HlsAdditionalManifestPaginatorTypeDef = TypedDict(
    "HlsAdditionalManifestPaginatorTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
    total=False,
)

HlsAdditionalManifestTypeDef = TypedDict(
    "HlsAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

HlsCaptionLanguageMappingTypeDef = TypedDict(
    "HlsCaptionLanguageMappingTypeDef",
    {
        "CaptionChannel": int,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

HlsImageBasedTrickPlaySettingsTypeDef = TypedDict(
    "HlsImageBasedTrickPlaySettingsTypeDef",
    {
        "IntervalCadence": HlsIntervalCadenceType,
        "ThumbnailHeight": int,
        "ThumbnailInterval": float,
        "ThumbnailWidth": int,
        "TileHeight": int,
        "TileWidth": int,
    },
    total=False,
)

HlsSettingsTypeDef = TypedDict(
    "HlsSettingsTypeDef",
    {
        "AudioGroupId": str,
        "AudioOnlyContainer": HlsAudioOnlyContainerType,
        "AudioRenditionSets": str,
        "AudioTrackType": HlsAudioTrackTypeType,
        "DescriptiveVideoServiceFlag": HlsDescriptiveVideoServiceFlagType,
        "IFrameOnlyManifest": HlsIFrameOnlyManifestType,
        "SegmentModifier": str,
    },
    total=False,
)

Id3InsertionTypeDef = TypedDict(
    "Id3InsertionTypeDef",
    {
        "Id3": str,
        "Timecode": str,
    },
    total=False,
)

InsertableImageTypeDef = TypedDict(
    "InsertableImageTypeDef",
    {
        "Duration": int,
        "FadeIn": int,
        "FadeOut": int,
        "Height": int,
        "ImageInserterInput": str,
        "ImageX": int,
        "ImageY": int,
        "Layer": int,
        "Opacity": int,
        "StartTime": str,
        "Width": int,
    },
    total=False,
)

InputClippingTypeDef = TypedDict(
    "InputClippingTypeDef",
    {
        "EndTimecode": str,
        "StartTimecode": str,
    },
    total=False,
)

InputDecryptionSettingsTypeDef = TypedDict(
    "InputDecryptionSettingsTypeDef",
    {
        "DecryptionMode": DecryptionModeType,
        "EncryptedDecryptionKey": str,
        "InitializationVector": str,
        "KmsKeyRegion": str,
    },
    total=False,
)

InputVideoGeneratorTypeDef = TypedDict(
    "InputVideoGeneratorTypeDef",
    {
        "Duration": int,
    },
    total=False,
)

RectangleTypeDef = TypedDict(
    "RectangleTypeDef",
    {
        "Height": int,
        "Width": int,
        "X": int,
        "Y": int,
    },
    total=False,
)

JobMessagesTypeDef = TypedDict(
    "JobMessagesTypeDef",
    {
        "Info": List[str],
        "Warning": List[str],
    },
    total=False,
)

QueueTransitionTypeDef = TypedDict(
    "QueueTransitionTypeDef",
    {
        "DestinationQueue": str,
        "SourceQueue": str,
        "Timestamp": datetime,
    },
    total=False,
)

TimingTypeDef = TypedDict(
    "TimingTypeDef",
    {
        "FinishTime": datetime,
        "StartTime": datetime,
        "SubmitTime": datetime,
    },
    total=False,
)

WarningGroupTypeDef = TypedDict(
    "WarningGroupTypeDef",
    {
        "Code": int,
        "Count": int,
    },
)

KantarWatermarkSettingsTypeDef = TypedDict(
    "KantarWatermarkSettingsTypeDef",
    {
        "ChannelName": str,
        "ContentReference": str,
        "CredentialsSecretName": str,
        "FileOffset": float,
        "KantarLicenseId": int,
        "KantarServerUrl": str,
        "LogDestination": str,
        "Metadata3": str,
        "Metadata4": str,
        "Metadata5": str,
        "Metadata6": str,
        "Metadata7": str,
        "Metadata8": str,
    },
    total=False,
)

NielsenConfigurationTypeDef = TypedDict(
    "NielsenConfigurationTypeDef",
    {
        "BreakoutCode": int,
        "DistributorId": str,
    },
    total=False,
)

NielsenNonLinearWatermarkSettingsTypeDef = TypedDict(
    "NielsenNonLinearWatermarkSettingsTypeDef",
    {
        "ActiveWatermarkProcess": NielsenActiveWatermarkProcessTypeType,
        "AdiFilename": str,
        "AssetId": str,
        "AssetName": str,
        "CbetSourceId": str,
        "EpisodeId": str,
        "MetadataDestination": str,
        "SourceId": int,
        "SourceWatermarkStatus": NielsenSourceWatermarkStatusTypeType,
        "TicServerUrl": str,
        "UniqueTicPerAudioTrack": NielsenUniqueTicPerAudioTrackTypeType,
    },
    total=False,
)

TimecodeConfigTypeDef = TypedDict(
    "TimecodeConfigTypeDef",
    {
        "Anchor": str,
        "Source": TimecodeSourceType,
        "Start": str,
        "TimestampOffset": str,
    },
    total=False,
)

ListJobTemplatesRequestRequestTypeDef = TypedDict(
    "ListJobTemplatesRequestRequestTypeDef",
    {
        "Category": str,
        "ListBy": JobTemplateListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
        "Queue": str,
        "Status": JobStatusType,
    },
    total=False,
)

ListPresetsRequestRequestTypeDef = TypedDict(
    "ListPresetsRequestRequestTypeDef",
    {
        "Category": str,
        "ListBy": PresetListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListQueuesRequestRequestTypeDef = TypedDict(
    "ListQueuesRequestRequestTypeDef",
    {
        "ListBy": QueueListByType,
        "MaxResults": int,
        "NextToken": str,
        "Order": OrderType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

ResourceTagsTypeDef = TypedDict(
    "ResourceTagsTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

M2tsScte35EsamTypeDef = TypedDict(
    "M2tsScte35EsamTypeDef",
    {
        "Scte35EsamPid": int,
    },
    total=False,
)

MotionImageInsertionFramerateTypeDef = TypedDict(
    "MotionImageInsertionFramerateTypeDef",
    {
        "FramerateDenominator": int,
        "FramerateNumerator": int,
    },
    total=False,
)

MotionImageInsertionOffsetTypeDef = TypedDict(
    "MotionImageInsertionOffsetTypeDef",
    {
        "ImageX": int,
        "ImageY": int,
    },
    total=False,
)

Mpeg2SettingsTypeDef = TypedDict(
    "Mpeg2SettingsTypeDef",
    {
        "AdaptiveQuantization": Mpeg2AdaptiveQuantizationType,
        "Bitrate": int,
        "CodecLevel": Mpeg2CodecLevelType,
        "CodecProfile": Mpeg2CodecProfileType,
        "DynamicSubGop": Mpeg2DynamicSubGopType,
        "FramerateControl": Mpeg2FramerateControlType,
        "FramerateConversionAlgorithm": Mpeg2FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": Mpeg2GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": Mpeg2InterlaceModeType,
        "IntraDcPrecision": Mpeg2IntraDcPrecisionType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "ParControl": Mpeg2ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Mpeg2QualityTuningLevelType,
        "RateControlMode": Mpeg2RateControlModeType,
        "ScanTypeConversionMode": Mpeg2ScanTypeConversionModeType,
        "SceneChangeDetect": Mpeg2SceneChangeDetectType,
        "SlowPal": Mpeg2SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": Mpeg2SpatialAdaptiveQuantizationType,
        "Syntax": Mpeg2SyntaxType,
        "Telecine": Mpeg2TelecineType,
        "TemporalAdaptiveQuantization": Mpeg2TemporalAdaptiveQuantizationType,
    },
    total=False,
)

MsSmoothAdditionalManifestPaginatorTypeDef = TypedDict(
    "MsSmoothAdditionalManifestPaginatorTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": List[str],
    },
    total=False,
)

MsSmoothAdditionalManifestTypeDef = TypedDict(
    "MsSmoothAdditionalManifestTypeDef",
    {
        "ManifestNameModifier": str,
        "SelectedOutputs": Sequence[str],
    },
    total=False,
)

MxfXavcProfileSettingsTypeDef = TypedDict(
    "MxfXavcProfileSettingsTypeDef",
    {
        "DurationMode": MxfXavcDurationModeType,
        "MaxAncDataSize": int,
    },
    total=False,
)

NexGuardFileMarkerSettingsTypeDef = TypedDict(
    "NexGuardFileMarkerSettingsTypeDef",
    {
        "License": str,
        "Payload": int,
        "Preset": str,
        "Strength": WatermarkingStrengthType,
    },
    total=False,
)

NoiseReducerFilterSettingsTypeDef = TypedDict(
    "NoiseReducerFilterSettingsTypeDef",
    {
        "Strength": int,
    },
    total=False,
)

NoiseReducerSpatialFilterSettingsTypeDef = TypedDict(
    "NoiseReducerSpatialFilterSettingsTypeDef",
    {
        "PostFilterSharpenStrength": int,
        "Speed": int,
        "Strength": int,
    },
    total=False,
)

NoiseReducerTemporalFilterSettingsTypeDef = TypedDict(
    "NoiseReducerTemporalFilterSettingsTypeDef",
    {
        "AggressiveMode": int,
        "PostTemporalSharpening": NoiseFilterPostTemporalSharpeningType,
        "PostTemporalSharpeningStrength": NoiseFilterPostTemporalSharpeningStrengthType,
        "Speed": int,
        "Strength": int,
    },
    total=False,
)

VideoDetailTypeDef = TypedDict(
    "VideoDetailTypeDef",
    {
        "HeightInPx": int,
        "WidthInPx": int,
    },
    total=False,
)

ProresSettingsTypeDef = TypedDict(
    "ProresSettingsTypeDef",
    {
        "ChromaSampling": ProresChromaSamplingType,
        "CodecProfile": ProresCodecProfileType,
        "FramerateControl": ProresFramerateControlType,
        "FramerateConversionAlgorithm": ProresFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": ProresInterlaceModeType,
        "ParControl": ProresParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "ScanTypeConversionMode": ProresScanTypeConversionModeType,
        "SlowPal": ProresSlowPalType,
        "Telecine": ProresTelecineType,
    },
    total=False,
)

ReservationPlanTypeDef = TypedDict(
    "ReservationPlanTypeDef",
    {
        "Commitment": Literal["ONE_YEAR"],
        "ExpiresAt": datetime,
        "PurchasedAt": datetime,
        "RenewalType": RenewalTypeType,
        "ReservedSlots": int,
        "Status": ReservationPlanStatusType,
    },
    total=False,
)

S3DestinationAccessControlTypeDef = TypedDict(
    "S3DestinationAccessControlTypeDef",
    {
        "CannedAcl": S3ObjectCannedAclType,
    },
    total=False,
)

S3EncryptionSettingsTypeDef = TypedDict(
    "S3EncryptionSettingsTypeDef",
    {
        "EncryptionType": S3ServerSideEncryptionTypeType,
        "KmsEncryptionContext": str,
        "KmsKeyArn": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Mapping[str, str],
    },
)

TimecodeBurninTypeDef = TypedDict(
    "TimecodeBurninTypeDef",
    {
        "FontSize": int,
        "Position": TimecodeBurninPositionType,
        "Prefix": str,
    },
    total=False,
)

_RequiredUntagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)
_OptionalUntagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUntagResourceRequestRequestTypeDef",
    {
        "TagKeys": Sequence[str],
    },
    total=False,
)


class UntagResourceRequestRequestTypeDef(
    _RequiredUntagResourceRequestRequestTypeDef, _OptionalUntagResourceRequestRequestTypeDef
):
    pass


Vc3SettingsTypeDef = TypedDict(
    "Vc3SettingsTypeDef",
    {
        "FramerateControl": Vc3FramerateControlType,
        "FramerateConversionAlgorithm": Vc3FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": Vc3InterlaceModeType,
        "ScanTypeConversionMode": Vc3ScanTypeConversionModeType,
        "SlowPal": Vc3SlowPalType,
        "Telecine": Vc3TelecineType,
        "Vc3Class": Vc3ClassType,
    },
    total=False,
)

Vp8SettingsTypeDef = TypedDict(
    "Vp8SettingsTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp8FramerateControlType,
        "FramerateConversionAlgorithm": Vp8FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp8ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp8QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
    total=False,
)

Vp9SettingsTypeDef = TypedDict(
    "Vp9SettingsTypeDef",
    {
        "Bitrate": int,
        "FramerateControl": Vp9FramerateControlType,
        "FramerateConversionAlgorithm": Vp9FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "HrdBufferSize": int,
        "MaxBitrate": int,
        "ParControl": Vp9ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": Vp9QualityTuningLevelType,
        "RateControlMode": Literal["VBR"],
    },
    total=False,
)

Xavc4kIntraCbgProfileSettingsTypeDef = TypedDict(
    "Xavc4kIntraCbgProfileSettingsTypeDef",
    {
        "XavcClass": Xavc4kIntraCbgProfileClassType,
    },
    total=False,
)

Xavc4kIntraVbrProfileSettingsTypeDef = TypedDict(
    "Xavc4kIntraVbrProfileSettingsTypeDef",
    {
        "XavcClass": Xavc4kIntraVbrProfileClassType,
    },
    total=False,
)

Xavc4kProfileSettingsTypeDef = TypedDict(
    "Xavc4kProfileSettingsTypeDef",
    {
        "BitrateClass": Xavc4kProfileBitrateClassType,
        "CodecProfile": Xavc4kProfileCodecProfileType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "QualityTuningLevel": Xavc4kProfileQualityTuningLevelType,
        "Slices": int,
    },
    total=False,
)

XavcHdIntraCbgProfileSettingsTypeDef = TypedDict(
    "XavcHdIntraCbgProfileSettingsTypeDef",
    {
        "XavcClass": XavcHdIntraCbgProfileClassType,
    },
    total=False,
)

XavcHdProfileSettingsTypeDef = TypedDict(
    "XavcHdProfileSettingsTypeDef",
    {
        "BitrateClass": XavcHdProfileBitrateClassType,
        "FlickerAdaptiveQuantization": XavcFlickerAdaptiveQuantizationType,
        "GopBReference": XavcGopBReferenceType,
        "GopClosedCadence": int,
        "HrdBufferSize": int,
        "InterlaceMode": XavcInterlaceModeType,
        "QualityTuningLevel": XavcHdProfileQualityTuningLevelType,
        "Slices": int,
        "Telecine": XavcHdProfileTelecineType,
    },
    total=False,
)

AudioCodecSettingsTypeDef = TypedDict(
    "AudioCodecSettingsTypeDef",
    {
        "AacSettings": AacSettingsTypeDef,
        "Ac3Settings": Ac3SettingsTypeDef,
        "AiffSettings": AiffSettingsTypeDef,
        "Codec": AudioCodecType,
        "Eac3AtmosSettings": Eac3AtmosSettingsTypeDef,
        "Eac3Settings": Eac3SettingsTypeDef,
        "FlacSettings": FlacSettingsTypeDef,
        "Mp2Settings": Mp2SettingsTypeDef,
        "Mp3Settings": Mp3SettingsTypeDef,
        "OpusSettings": OpusSettingsTypeDef,
        "VorbisSettings": VorbisSettingsTypeDef,
        "WavSettings": WavSettingsTypeDef,
    },
    total=False,
)

AutomatedAbrRulePaginatorTypeDef = TypedDict(
    "AutomatedAbrRulePaginatorTypeDef",
    {
        "AllowedRenditions": List[AllowedRenditionSizeTypeDef],
        "ForceIncludeRenditions": List[ForceIncludeRenditionSizeTypeDef],
        "MinBottomRenditionSize": MinBottomRenditionSizeTypeDef,
        "MinTopRenditionSize": MinTopRenditionSizeTypeDef,
        "Type": RuleTypeType,
    },
    total=False,
)

AutomatedAbrRuleTypeDef = TypedDict(
    "AutomatedAbrRuleTypeDef",
    {
        "AllowedRenditions": Sequence[AllowedRenditionSizeTypeDef],
        "ForceIncludeRenditions": Sequence[ForceIncludeRenditionSizeTypeDef],
        "MinBottomRenditionSize": MinBottomRenditionSizeTypeDef,
        "MinTopRenditionSize": MinTopRenditionSizeTypeDef,
        "Type": RuleTypeType,
    },
    total=False,
)

Av1SettingsTypeDef = TypedDict(
    "Av1SettingsTypeDef",
    {
        "AdaptiveQuantization": Av1AdaptiveQuantizationType,
        "BitDepth": Av1BitDepthType,
        "FilmGrainSynthesis": Av1FilmGrainSynthesisType,
        "FramerateControl": Av1FramerateControlType,
        "FramerateConversionAlgorithm": Av1FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopSize": float,
        "MaxBitrate": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "QvbrSettings": Av1QvbrSettingsTypeDef,
        "RateControlMode": Literal["QVBR"],
        "Slices": int,
        "SpatialAdaptiveQuantization": Av1SpatialAdaptiveQuantizationType,
    },
    total=False,
)

AvcIntraSettingsTypeDef = TypedDict(
    "AvcIntraSettingsTypeDef",
    {
        "AvcIntraClass": AvcIntraClassType,
        "AvcIntraUhdSettings": AvcIntraUhdSettingsTypeDef,
        "FramerateControl": AvcIntraFramerateControlType,
        "FramerateConversionAlgorithm": AvcIntraFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "InterlaceMode": AvcIntraInterlaceModeType,
        "ScanTypeConversionMode": AvcIntraScanTypeConversionModeType,
        "SlowPal": AvcIntraSlowPalType,
        "Telecine": AvcIntraTelecineType,
    },
    total=False,
)

CaptionDestinationSettingsPaginatorTypeDef = TypedDict(
    "CaptionDestinationSettingsPaginatorTypeDef",
    {
        "BurninDestinationSettings": BurninDestinationSettingsTypeDef,
        "DestinationType": CaptionDestinationTypeType,
        "DvbSubDestinationSettings": DvbSubDestinationSettingsTypeDef,
        "EmbeddedDestinationSettings": EmbeddedDestinationSettingsTypeDef,
        "ImscDestinationSettings": ImscDestinationSettingsTypeDef,
        "SccDestinationSettings": SccDestinationSettingsTypeDef,
        "SrtDestinationSettings": SrtDestinationSettingsTypeDef,
        "TeletextDestinationSettings": TeletextDestinationSettingsPaginatorTypeDef,
        "TtmlDestinationSettings": TtmlDestinationSettingsTypeDef,
        "WebvttDestinationSettings": WebvttDestinationSettingsTypeDef,
    },
    total=False,
)

CaptionDestinationSettingsTypeDef = TypedDict(
    "CaptionDestinationSettingsTypeDef",
    {
        "BurninDestinationSettings": BurninDestinationSettingsTypeDef,
        "DestinationType": CaptionDestinationTypeType,
        "DvbSubDestinationSettings": DvbSubDestinationSettingsTypeDef,
        "EmbeddedDestinationSettings": EmbeddedDestinationSettingsTypeDef,
        "ImscDestinationSettings": ImscDestinationSettingsTypeDef,
        "SccDestinationSettings": SccDestinationSettingsTypeDef,
        "SrtDestinationSettings": SrtDestinationSettingsTypeDef,
        "TeletextDestinationSettings": TeletextDestinationSettingsTypeDef,
        "TtmlDestinationSettings": TtmlDestinationSettingsTypeDef,
        "WebvttDestinationSettings": WebvttDestinationSettingsTypeDef,
    },
    total=False,
)

FileSourceSettingsTypeDef = TypedDict(
    "FileSourceSettingsTypeDef",
    {
        "Convert608To708": FileSourceConvert608To708Type,
        "ConvertPaintToPop": CaptionSourceConvertPaintOnToPopOnType,
        "Framerate": CaptionSourceFramerateTypeDef,
        "SourceFile": str,
        "TimeDelta": int,
        "TimeDeltaUnits": FileSourceTimeDeltaUnitsType,
    },
    total=False,
)

ChannelMappingPaginatorTypeDef = TypedDict(
    "ChannelMappingPaginatorTypeDef",
    {
        "OutputChannels": List[OutputChannelMappingPaginatorTypeDef],
    },
    total=False,
)

ChannelMappingTypeDef = TypedDict(
    "ChannelMappingTypeDef",
    {
        "OutputChannels": Sequence[OutputChannelMappingTypeDef],
    },
    total=False,
)

CmafEncryptionSettingsPaginatorTypeDef = TypedDict(
    "CmafEncryptionSettingsPaginatorTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": CmafEncryptionTypeType,
        "InitializationVectorInManifest": CmafInitializationVectorInManifestType,
        "SpekeKeyProvider": SpekeKeyProviderCmafPaginatorTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": CmafKeyProviderTypeType,
    },
    total=False,
)

CmafEncryptionSettingsTypeDef = TypedDict(
    "CmafEncryptionSettingsTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": CmafEncryptionTypeType,
        "InitializationVectorInManifest": CmafInitializationVectorInManifestType,
        "SpekeKeyProvider": SpekeKeyProviderCmafTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": CmafKeyProviderTypeType,
    },
    total=False,
)

ColorCorrectorTypeDef = TypedDict(
    "ColorCorrectorTypeDef",
    {
        "Brightness": int,
        "ClipLimits": ClipLimitsTypeDef,
        "ColorSpaceConversion": ColorSpaceConversionType,
        "Contrast": int,
        "Hdr10Metadata": Hdr10MetadataTypeDef,
        "HdrToSdrToneMapper": HDRToSDRToneMapperType,
        "Hue": int,
        "SampleRangeConversion": SampleRangeConversionType,
        "Saturation": int,
        "SdrReferenceWhiteLevel": int,
    },
    total=False,
)

VideoSelectorTypeDef = TypedDict(
    "VideoSelectorTypeDef",
    {
        "AlphaBehavior": AlphaBehaviorType,
        "ColorSpace": ColorSpaceType,
        "ColorSpaceUsage": ColorSpaceUsageType,
        "EmbeddedTimecodeOverride": EmbeddedTimecodeOverrideType,
        "Hdr10Metadata": Hdr10MetadataTypeDef,
        "PadVideo": PadVideoType,
        "Pid": int,
        "ProgramNumber": int,
        "Rotate": InputRotateType,
        "SampleRange": InputSampleRangeType,
    },
    total=False,
)

_RequiredCreateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQueueRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
        "ReservationPlanSettings": ReservationPlanSettingsTypeDef,
        "Status": QueueStatusType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateQueueRequestRequestTypeDef(
    _RequiredCreateQueueRequestRequestTypeDef, _OptionalCreateQueueRequestRequestTypeDef
):
    pass


_RequiredUpdateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQueueRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQueueRequestRequestTypeDef",
    {
        "Description": str,
        "ReservationPlanSettings": ReservationPlanSettingsTypeDef,
        "Status": QueueStatusType,
    },
    total=False,
)


class UpdateQueueRequestRequestTypeDef(
    _RequiredUpdateQueueRequestRequestTypeDef, _OptionalUpdateQueueRequestRequestTypeDef
):
    pass


DashIsoEncryptionSettingsPaginatorTypeDef = TypedDict(
    "DashIsoEncryptionSettingsPaginatorTypeDef",
    {
        "PlaybackDeviceCompatibility": DashIsoPlaybackDeviceCompatibilityType,
        "SpekeKeyProvider": SpekeKeyProviderPaginatorTypeDef,
    },
    total=False,
)

HlsEncryptionSettingsPaginatorTypeDef = TypedDict(
    "HlsEncryptionSettingsPaginatorTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": HlsEncryptionTypeType,
        "InitializationVectorInManifest": HlsInitializationVectorInManifestType,
        "OfflineEncrypted": HlsOfflineEncryptedType,
        "SpekeKeyProvider": SpekeKeyProviderPaginatorTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": HlsKeyProviderTypeType,
    },
    total=False,
)

MsSmoothEncryptionSettingsPaginatorTypeDef = TypedDict(
    "MsSmoothEncryptionSettingsPaginatorTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderPaginatorTypeDef,
    },
    total=False,
)

DashIsoEncryptionSettingsTypeDef = TypedDict(
    "DashIsoEncryptionSettingsTypeDef",
    {
        "PlaybackDeviceCompatibility": DashIsoPlaybackDeviceCompatibilityType,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
    total=False,
)

HlsEncryptionSettingsTypeDef = TypedDict(
    "HlsEncryptionSettingsTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": HlsEncryptionTypeType,
        "InitializationVectorInManifest": HlsInitializationVectorInManifestType,
        "OfflineEncrypted": HlsOfflineEncryptedType,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
        "StaticKeyProvider": StaticKeyProviderTypeDef,
        "Type": HlsKeyProviderTypeType,
    },
    total=False,
)

MsSmoothEncryptionSettingsTypeDef = TypedDict(
    "MsSmoothEncryptionSettingsTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
    total=False,
)

DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef = TypedDict(
    "DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef",
    {
        "Mode": DescribeEndpointsModeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobTemplatesRequestListJobTemplatesPaginateTypeDef = TypedDict(
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    {
        "Category": str,
        "ListBy": JobTemplateListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "Order": OrderType,
        "Queue": str,
        "Status": JobStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPresetsRequestListPresetsPaginateTypeDef = TypedDict(
    "ListPresetsRequestListPresetsPaginateTypeDef",
    {
        "Category": str,
        "ListBy": PresetListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "ListQueuesRequestListQueuesPaginateTypeDef",
    {
        "ListBy": QueueListByType,
        "Order": OrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DolbyVisionTypeDef = TypedDict(
    "DolbyVisionTypeDef",
    {
        "L6Metadata": DolbyVisionLevel6MetadataTypeDef,
        "L6Mode": DolbyVisionLevel6ModeType,
        "Mapping": DolbyVisionMappingType,
        "Profile": DolbyVisionProfileType,
    },
    total=False,
)

EsamSettingsTypeDef = TypedDict(
    "EsamSettingsTypeDef",
    {
        "ManifestConfirmConditionNotification": EsamManifestConfirmConditionNotificationTypeDef,
        "ResponseSignalPreroll": int,
        "SignalProcessingNotification": EsamSignalProcessingNotificationTypeDef,
    },
    total=False,
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPolicyRequestRequestTypeDef = TypedDict(
    "PutPolicyRequestRequestTypeDef",
    {
        "Policy": PolicyTypeDef,
    },
)

PutPolicyResponseTypeDef = TypedDict(
    "PutPolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

H264SettingsTypeDef = TypedDict(
    "H264SettingsTypeDef",
    {
        "AdaptiveQuantization": H264AdaptiveQuantizationType,
        "BandwidthReductionFilter": BandwidthReductionFilterTypeDef,
        "Bitrate": int,
        "CodecLevel": H264CodecLevelType,
        "CodecProfile": H264CodecProfileType,
        "DynamicSubGop": H264DynamicSubGopType,
        "EntropyEncoding": H264EntropyEncodingType,
        "FieldEncoding": H264FieldEncodingType,
        "FlickerAdaptiveQuantization": H264FlickerAdaptiveQuantizationType,
        "FramerateControl": H264FramerateControlType,
        "FramerateConversionAlgorithm": H264FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H264GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H264GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H264InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H264ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H264QualityTuningLevelType,
        "QvbrSettings": H264QvbrSettingsTypeDef,
        "RateControlMode": H264RateControlModeType,
        "RepeatPps": H264RepeatPpsType,
        "ScanTypeConversionMode": H264ScanTypeConversionModeType,
        "SceneChangeDetect": H264SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H264SlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": H264SpatialAdaptiveQuantizationType,
        "Syntax": H264SyntaxType,
        "Telecine": H264TelecineType,
        "TemporalAdaptiveQuantization": H264TemporalAdaptiveQuantizationType,
        "UnregisteredSeiTimecode": H264UnregisteredSeiTimecodeType,
    },
    total=False,
)

H265SettingsTypeDef = TypedDict(
    "H265SettingsTypeDef",
    {
        "AdaptiveQuantization": H265AdaptiveQuantizationType,
        "AlternateTransferFunctionSei": H265AlternateTransferFunctionSeiType,
        "BandwidthReductionFilter": BandwidthReductionFilterTypeDef,
        "Bitrate": int,
        "CodecLevel": H265CodecLevelType,
        "CodecProfile": H265CodecProfileType,
        "DynamicSubGop": H265DynamicSubGopType,
        "FlickerAdaptiveQuantization": H265FlickerAdaptiveQuantizationType,
        "FramerateControl": H265FramerateControlType,
        "FramerateConversionAlgorithm": H265FramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": H265GopBReferenceType,
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": H265GopSizeUnitsType,
        "HrdBufferFinalFillPercentage": int,
        "HrdBufferInitialFillPercentage": int,
        "HrdBufferSize": int,
        "InterlaceMode": H265InterlaceModeType,
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumberBFramesBetweenReferenceFrames": int,
        "NumberReferenceFrames": int,
        "ParControl": H265ParControlType,
        "ParDenominator": int,
        "ParNumerator": int,
        "QualityTuningLevel": H265QualityTuningLevelType,
        "QvbrSettings": H265QvbrSettingsTypeDef,
        "RateControlMode": H265RateControlModeType,
        "SampleAdaptiveOffsetFilterMode": H265SampleAdaptiveOffsetFilterModeType,
        "ScanTypeConversionMode": H265ScanTypeConversionModeType,
        "SceneChangeDetect": H265SceneChangeDetectType,
        "Slices": int,
        "SlowPal": H265SlowPalType,
        "SpatialAdaptiveQuantization": H265SpatialAdaptiveQuantizationType,
        "Telecine": H265TelecineType,
        "TemporalAdaptiveQuantization": H265TemporalAdaptiveQuantizationType,
        "TemporalIds": H265TemporalIdsType,
        "Tiles": H265TilesType,
        "UnregisteredSeiTimecode": H265UnregisteredSeiTimecodeType,
        "WriteMp4PackagingType": H265WriteMp4PackagingTypeType,
    },
    total=False,
)

OutputSettingsTypeDef = TypedDict(
    "OutputSettingsTypeDef",
    {
        "HlsSettings": HlsSettingsTypeDef,
    },
    total=False,
)

TimedMetadataInsertionPaginatorTypeDef = TypedDict(
    "TimedMetadataInsertionPaginatorTypeDef",
    {
        "Id3Insertions": List[Id3InsertionTypeDef],
    },
    total=False,
)

TimedMetadataInsertionTypeDef = TypedDict(
    "TimedMetadataInsertionTypeDef",
    {
        "Id3Insertions": Sequence[Id3InsertionTypeDef],
    },
    total=False,
)

ImageInserterPaginatorTypeDef = TypedDict(
    "ImageInserterPaginatorTypeDef",
    {
        "InsertableImages": List[InsertableImageTypeDef],
        "SdrReferenceWhiteLevel": int,
    },
    total=False,
)

ImageInserterTypeDef = TypedDict(
    "ImageInserterTypeDef",
    {
        "InsertableImages": Sequence[InsertableImageTypeDef],
        "SdrReferenceWhiteLevel": int,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceTags": ResourceTagsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

M2tsSettingsPaginatorTypeDef = TypedDict(
    "M2tsSettingsPaginatorTypeDef",
    {
        "AudioBufferModel": M2tsAudioBufferModelType,
        "AudioDuration": M2tsAudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": List[int],
        "Bitrate": int,
        "BufferModel": M2tsBufferModelType,
        "DataPTSControl": M2tsDataPtsControlType,
        "DvbNitSettings": DvbNitSettingsTypeDef,
        "DvbSdtSettings": DvbSdtSettingsTypeDef,
        "DvbSubPids": List[int],
        "DvbTdtSettings": DvbTdtSettingsTypeDef,
        "DvbTeletextPid": int,
        "EbpAudioInterval": M2tsEbpAudioIntervalType,
        "EbpPlacement": M2tsEbpPlacementType,
        "EsRateInPes": M2tsEsRateInPesType,
        "ForceTsVideoEbpOrder": M2tsForceTsVideoEbpOrderType,
        "FragmentTime": float,
        "KlvMetadata": M2tsKlvMetadataType,
        "MaxPcrInterval": int,
        "MinEbpInterval": int,
        "NielsenId3": M2tsNielsenId3Type,
        "NullPacketBitrate": float,
        "PatInterval": int,
        "PcrControl": M2tsPcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "PtsOffset": int,
        "PtsOffsetMode": TsPtsOffsetType,
        "RateMode": M2tsRateModeType,
        "Scte35Esam": M2tsScte35EsamTypeDef,
        "Scte35Pid": int,
        "Scte35Source": M2tsScte35SourceType,
        "SegmentationMarkers": M2tsSegmentationMarkersType,
        "SegmentationStyle": M2tsSegmentationStyleType,
        "SegmentationTime": float,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

M2tsSettingsTypeDef = TypedDict(
    "M2tsSettingsTypeDef",
    {
        "AudioBufferModel": M2tsAudioBufferModelType,
        "AudioDuration": M2tsAudioDurationType,
        "AudioFramesPerPes": int,
        "AudioPids": Sequence[int],
        "Bitrate": int,
        "BufferModel": M2tsBufferModelType,
        "DataPTSControl": M2tsDataPtsControlType,
        "DvbNitSettings": DvbNitSettingsTypeDef,
        "DvbSdtSettings": DvbSdtSettingsTypeDef,
        "DvbSubPids": Sequence[int],
        "DvbTdtSettings": DvbTdtSettingsTypeDef,
        "DvbTeletextPid": int,
        "EbpAudioInterval": M2tsEbpAudioIntervalType,
        "EbpPlacement": M2tsEbpPlacementType,
        "EsRateInPes": M2tsEsRateInPesType,
        "ForceTsVideoEbpOrder": M2tsForceTsVideoEbpOrderType,
        "FragmentTime": float,
        "KlvMetadata": M2tsKlvMetadataType,
        "MaxPcrInterval": int,
        "MinEbpInterval": int,
        "NielsenId3": M2tsNielsenId3Type,
        "NullPacketBitrate": float,
        "PatInterval": int,
        "PcrControl": M2tsPcrControlType,
        "PcrPid": int,
        "PmtInterval": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "ProgramNumber": int,
        "PtsOffset": int,
        "PtsOffsetMode": TsPtsOffsetType,
        "RateMode": M2tsRateModeType,
        "Scte35Esam": M2tsScte35EsamTypeDef,
        "Scte35Pid": int,
        "Scte35Source": M2tsScte35SourceType,
        "SegmentationMarkers": M2tsSegmentationMarkersType,
        "SegmentationStyle": M2tsSegmentationStyleType,
        "SegmentationTime": float,
        "TimedMetadataPid": int,
        "TransportStreamId": int,
        "VideoPid": int,
    },
    total=False,
)

MotionImageInserterTypeDef = TypedDict(
    "MotionImageInserterTypeDef",
    {
        "Framerate": MotionImageInsertionFramerateTypeDef,
        "Input": str,
        "InsertionMode": MotionImageInsertionModeType,
        "Offset": MotionImageInsertionOffsetTypeDef,
        "Playback": MotionImagePlaybackType,
        "StartTime": str,
    },
    total=False,
)

MxfSettingsTypeDef = TypedDict(
    "MxfSettingsTypeDef",
    {
        "AfdSignaling": MxfAfdSignalingType,
        "Profile": MxfProfileType,
        "XavcProfileSettings": MxfXavcProfileSettingsTypeDef,
    },
    total=False,
)

PartnerWatermarkingTypeDef = TypedDict(
    "PartnerWatermarkingTypeDef",
    {
        "NexguardFileMarkerSettings": NexGuardFileMarkerSettingsTypeDef,
    },
    total=False,
)

NoiseReducerTypeDef = TypedDict(
    "NoiseReducerTypeDef",
    {
        "Filter": NoiseReducerFilterType,
        "FilterSettings": NoiseReducerFilterSettingsTypeDef,
        "SpatialFilterSettings": NoiseReducerSpatialFilterSettingsTypeDef,
        "TemporalFilterSettings": NoiseReducerTemporalFilterSettingsTypeDef,
    },
    total=False,
)

OutputDetailTypeDef = TypedDict(
    "OutputDetailTypeDef",
    {
        "DurationInMs": int,
        "VideoDetails": VideoDetailTypeDef,
    },
    total=False,
)

_RequiredQueueTypeDef = TypedDict(
    "_RequiredQueueTypeDef",
    {
        "Name": str,
    },
)
_OptionalQueueTypeDef = TypedDict(
    "_OptionalQueueTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Description": str,
        "LastUpdated": datetime,
        "PricingPlan": PricingPlanType,
        "ProgressingJobsCount": int,
        "ReservationPlan": ReservationPlanTypeDef,
        "Status": QueueStatusType,
        "SubmittedJobsCount": int,
        "Type": TypeType,
    },
    total=False,
)


class QueueTypeDef(_RequiredQueueTypeDef, _OptionalQueueTypeDef):
    pass


S3DestinationSettingsTypeDef = TypedDict(
    "S3DestinationSettingsTypeDef",
    {
        "AccessControl": S3DestinationAccessControlTypeDef,
        "Encryption": S3EncryptionSettingsTypeDef,
        "StorageClass": S3StorageClassType,
    },
    total=False,
)

XavcSettingsTypeDef = TypedDict(
    "XavcSettingsTypeDef",
    {
        "AdaptiveQuantization": XavcAdaptiveQuantizationType,
        "EntropyEncoding": XavcEntropyEncodingType,
        "FramerateControl": XavcFramerateControlType,
        "FramerateConversionAlgorithm": XavcFramerateConversionAlgorithmType,
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "Profile": XavcProfileType,
        "SlowPal": XavcSlowPalType,
        "Softness": int,
        "SpatialAdaptiveQuantization": XavcSpatialAdaptiveQuantizationType,
        "TemporalAdaptiveQuantization": XavcTemporalAdaptiveQuantizationType,
        "Xavc4kIntraCbgProfileSettings": Xavc4kIntraCbgProfileSettingsTypeDef,
        "Xavc4kIntraVbrProfileSettings": Xavc4kIntraVbrProfileSettingsTypeDef,
        "Xavc4kProfileSettings": Xavc4kProfileSettingsTypeDef,
        "XavcHdIntraCbgProfileSettings": XavcHdIntraCbgProfileSettingsTypeDef,
        "XavcHdProfileSettings": XavcHdProfileSettingsTypeDef,
    },
    total=False,
)

AutomatedAbrSettingsPaginatorTypeDef = TypedDict(
    "AutomatedAbrSettingsPaginatorTypeDef",
    {
        "MaxAbrBitrate": int,
        "MaxRenditions": int,
        "MinAbrBitrate": int,
        "Rules": List[AutomatedAbrRulePaginatorTypeDef],
    },
    total=False,
)

AutomatedAbrSettingsTypeDef = TypedDict(
    "AutomatedAbrSettingsTypeDef",
    {
        "MaxAbrBitrate": int,
        "MaxRenditions": int,
        "MinAbrBitrate": int,
        "Rules": Sequence[AutomatedAbrRuleTypeDef],
    },
    total=False,
)

CaptionDescriptionPaginatorTypeDef = TypedDict(
    "CaptionDescriptionPaginatorTypeDef",
    {
        "CaptionSelectorName": str,
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsPaginatorTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

CaptionDescriptionPresetPaginatorTypeDef = TypedDict(
    "CaptionDescriptionPresetPaginatorTypeDef",
    {
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsPaginatorTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

CaptionDescriptionPresetTypeDef = TypedDict(
    "CaptionDescriptionPresetTypeDef",
    {
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

CaptionDescriptionTypeDef = TypedDict(
    "CaptionDescriptionTypeDef",
    {
        "CaptionSelectorName": str,
        "CustomLanguageCode": str,
        "DestinationSettings": CaptionDestinationSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "LanguageDescription": str,
    },
    total=False,
)

CaptionSourceSettingsTypeDef = TypedDict(
    "CaptionSourceSettingsTypeDef",
    {
        "AncillarySourceSettings": AncillarySourceSettingsTypeDef,
        "DvbSubSourceSettings": DvbSubSourceSettingsTypeDef,
        "EmbeddedSourceSettings": EmbeddedSourceSettingsTypeDef,
        "FileSourceSettings": FileSourceSettingsTypeDef,
        "SourceType": CaptionSourceTypeType,
        "TeletextSourceSettings": TeletextSourceSettingsTypeDef,
        "TrackSourceSettings": TrackSourceSettingsTypeDef,
        "WebvttHlsSourceSettings": WebvttHlsSourceSettingsTypeDef,
    },
    total=False,
)

RemixSettingsPaginatorTypeDef = TypedDict(
    "RemixSettingsPaginatorTypeDef",
    {
        "ChannelMapping": ChannelMappingPaginatorTypeDef,
        "ChannelsIn": int,
        "ChannelsOut": int,
    },
    total=False,
)

RemixSettingsTypeDef = TypedDict(
    "RemixSettingsTypeDef",
    {
        "ChannelMapping": ChannelMappingTypeDef,
        "ChannelsIn": int,
        "ChannelsOut": int,
    },
    total=False,
)

ContainerSettingsPaginatorTypeDef = TypedDict(
    "ContainerSettingsPaginatorTypeDef",
    {
        "CmfcSettings": CmfcSettingsTypeDef,
        "Container": ContainerTypeType,
        "F4vSettings": F4vSettingsTypeDef,
        "M2tsSettings": M2tsSettingsPaginatorTypeDef,
        "M3u8Settings": M3u8SettingsPaginatorTypeDef,
        "MovSettings": MovSettingsTypeDef,
        "Mp4Settings": Mp4SettingsTypeDef,
        "MpdSettings": MpdSettingsTypeDef,
        "MxfSettings": MxfSettingsTypeDef,
    },
    total=False,
)

ContainerSettingsTypeDef = TypedDict(
    "ContainerSettingsTypeDef",
    {
        "CmfcSettings": CmfcSettingsTypeDef,
        "Container": ContainerTypeType,
        "F4vSettings": F4vSettingsTypeDef,
        "M2tsSettings": M2tsSettingsTypeDef,
        "M3u8Settings": M3u8SettingsTypeDef,
        "MovSettings": MovSettingsTypeDef,
        "Mp4Settings": Mp4SettingsTypeDef,
        "MpdSettings": MpdSettingsTypeDef,
        "MxfSettings": MxfSettingsTypeDef,
    },
    total=False,
)

VideoPreprocessorPaginatorTypeDef = TypedDict(
    "VideoPreprocessorPaginatorTypeDef",
    {
        "ColorCorrector": ColorCorrectorTypeDef,
        "Deinterlacer": DeinterlacerTypeDef,
        "DolbyVision": DolbyVisionTypeDef,
        "Hdr10Plus": Hdr10PlusTypeDef,
        "ImageInserter": ImageInserterPaginatorTypeDef,
        "NoiseReducer": NoiseReducerTypeDef,
        "PartnerWatermarking": PartnerWatermarkingTypeDef,
        "TimecodeBurnin": TimecodeBurninTypeDef,
    },
    total=False,
)

VideoPreprocessorTypeDef = TypedDict(
    "VideoPreprocessorTypeDef",
    {
        "ColorCorrector": ColorCorrectorTypeDef,
        "Deinterlacer": DeinterlacerTypeDef,
        "DolbyVision": DolbyVisionTypeDef,
        "Hdr10Plus": Hdr10PlusTypeDef,
        "ImageInserter": ImageInserterTypeDef,
        "NoiseReducer": NoiseReducerTypeDef,
        "PartnerWatermarking": PartnerWatermarkingTypeDef,
        "TimecodeBurnin": TimecodeBurninTypeDef,
    },
    total=False,
)

OutputGroupDetailTypeDef = TypedDict(
    "OutputGroupDetailTypeDef",
    {
        "OutputDetails": List[OutputDetailTypeDef],
    },
    total=False,
)

CreateQueueResponseTypeDef = TypedDict(
    "CreateQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueueResponseTypeDef = TypedDict(
    "GetQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueuesResponseTypeDef = TypedDict(
    "ListQueuesResponseTypeDef",
    {
        "NextToken": str,
        "Queues": List[QueueTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateQueueResponseTypeDef = TypedDict(
    "UpdateQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DestinationSettingsTypeDef = TypedDict(
    "DestinationSettingsTypeDef",
    {
        "S3Settings": S3DestinationSettingsTypeDef,
    },
    total=False,
)

VideoCodecSettingsTypeDef = TypedDict(
    "VideoCodecSettingsTypeDef",
    {
        "Av1Settings": Av1SettingsTypeDef,
        "AvcIntraSettings": AvcIntraSettingsTypeDef,
        "Codec": VideoCodecType,
        "FrameCaptureSettings": FrameCaptureSettingsTypeDef,
        "H264Settings": H264SettingsTypeDef,
        "H265Settings": H265SettingsTypeDef,
        "Mpeg2Settings": Mpeg2SettingsTypeDef,
        "ProresSettings": ProresSettingsTypeDef,
        "Vc3Settings": Vc3SettingsTypeDef,
        "Vp8Settings": Vp8SettingsTypeDef,
        "Vp9Settings": Vp9SettingsTypeDef,
        "XavcSettings": XavcSettingsTypeDef,
    },
    total=False,
)

AutomatedEncodingSettingsPaginatorTypeDef = TypedDict(
    "AutomatedEncodingSettingsPaginatorTypeDef",
    {
        "AbrSettings": AutomatedAbrSettingsPaginatorTypeDef,
    },
    total=False,
)

AutomatedEncodingSettingsTypeDef = TypedDict(
    "AutomatedEncodingSettingsTypeDef",
    {
        "AbrSettings": AutomatedAbrSettingsTypeDef,
    },
    total=False,
)

CaptionSelectorTypeDef = TypedDict(
    "CaptionSelectorTypeDef",
    {
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "SourceSettings": CaptionSourceSettingsTypeDef,
    },
    total=False,
)

AudioDescriptionPaginatorTypeDef = TypedDict(
    "AudioDescriptionPaginatorTypeDef",
    {
        "AudioChannelTaggingSettings": AudioChannelTaggingSettingsTypeDef,
        "AudioNormalizationSettings": AudioNormalizationSettingsTypeDef,
        "AudioSourceName": str,
        "AudioType": int,
        "AudioTypeControl": AudioTypeControlType,
        "CodecSettings": AudioCodecSettingsTypeDef,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageCodeControl": AudioLanguageCodeControlType,
        "RemixSettings": RemixSettingsPaginatorTypeDef,
        "StreamName": str,
    },
    total=False,
)

AudioSelectorPaginatorTypeDef = TypedDict(
    "AudioSelectorPaginatorTypeDef",
    {
        "AudioDurationCorrection": AudioDurationCorrectionType,
        "CustomLanguageCode": str,
        "DefaultSelection": AudioDefaultSelectionType,
        "ExternalAudioFileInput": str,
        "HlsRenditionGroupSettings": HlsRenditionGroupSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "Offset": int,
        "Pids": List[int],
        "ProgramSelection": int,
        "RemixSettings": RemixSettingsPaginatorTypeDef,
        "SelectorType": AudioSelectorTypeType,
        "Tracks": List[int],
    },
    total=False,
)

AudioDescriptionTypeDef = TypedDict(
    "AudioDescriptionTypeDef",
    {
        "AudioChannelTaggingSettings": AudioChannelTaggingSettingsTypeDef,
        "AudioNormalizationSettings": AudioNormalizationSettingsTypeDef,
        "AudioSourceName": str,
        "AudioType": int,
        "AudioTypeControl": AudioTypeControlType,
        "CodecSettings": AudioCodecSettingsTypeDef,
        "CustomLanguageCode": str,
        "LanguageCode": LanguageCodeType,
        "LanguageCodeControl": AudioLanguageCodeControlType,
        "RemixSettings": RemixSettingsTypeDef,
        "StreamName": str,
    },
    total=False,
)

AudioSelectorTypeDef = TypedDict(
    "AudioSelectorTypeDef",
    {
        "AudioDurationCorrection": AudioDurationCorrectionType,
        "CustomLanguageCode": str,
        "DefaultSelection": AudioDefaultSelectionType,
        "ExternalAudioFileInput": str,
        "HlsRenditionGroupSettings": HlsRenditionGroupSettingsTypeDef,
        "LanguageCode": LanguageCodeType,
        "Offset": int,
        "Pids": Sequence[int],
        "ProgramSelection": int,
        "RemixSettings": RemixSettingsTypeDef,
        "SelectorType": AudioSelectorTypeType,
        "Tracks": Sequence[int],
    },
    total=False,
)

CmafGroupSettingsPaginatorTypeDef = TypedDict(
    "CmafGroupSettingsPaginatorTypeDef",
    {
        "AdditionalManifests": List[CmafAdditionalManifestPaginatorTypeDef],
        "BaseUrl": str,
        "ClientCache": CmafClientCacheType,
        "CodecSpecification": CmafCodecSpecificationType,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": CmafEncryptionSettingsPaginatorTypeDef,
        "FragmentLength": int,
        "ImageBasedTrickPlay": CmafImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": CmafImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": CmafManifestCompressionType,
        "ManifestDurationFormat": CmafManifestDurationFormatType,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": CmafMpdManifestBandwidthTypeType,
        "MpdProfile": CmafMpdProfileType,
        "PtsOffsetHandlingForBFrames": CmafPtsOffsetHandlingForBFramesType,
        "SegmentControl": CmafSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": CmafSegmentLengthControlType,
        "StreamInfResolution": CmafStreamInfResolutionType,
        "TargetDurationCompatibilityMode": CmafTargetDurationCompatibilityModeType,
        "VideoCompositionOffsets": CmafVideoCompositionOffsetsType,
        "WriteDashManifest": CmafWriteDASHManifestType,
        "WriteHlsManifest": CmafWriteHLSManifestType,
        "WriteSegmentTimelineInRepresentation": CmafWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

CmafGroupSettingsTypeDef = TypedDict(
    "CmafGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[CmafAdditionalManifestTypeDef],
        "BaseUrl": str,
        "ClientCache": CmafClientCacheType,
        "CodecSpecification": CmafCodecSpecificationType,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": CmafEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "ImageBasedTrickPlay": CmafImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": CmafImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": CmafManifestCompressionType,
        "ManifestDurationFormat": CmafManifestDurationFormatType,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": CmafMpdManifestBandwidthTypeType,
        "MpdProfile": CmafMpdProfileType,
        "PtsOffsetHandlingForBFrames": CmafPtsOffsetHandlingForBFramesType,
        "SegmentControl": CmafSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": CmafSegmentLengthControlType,
        "StreamInfResolution": CmafStreamInfResolutionType,
        "TargetDurationCompatibilityMode": CmafTargetDurationCompatibilityModeType,
        "VideoCompositionOffsets": CmafVideoCompositionOffsetsType,
        "WriteDashManifest": CmafWriteDASHManifestType,
        "WriteHlsManifest": CmafWriteHLSManifestType,
        "WriteSegmentTimelineInRepresentation": CmafWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

DashIsoGroupSettingsPaginatorTypeDef = TypedDict(
    "DashIsoGroupSettingsPaginatorTypeDef",
    {
        "AdditionalManifests": List[DashAdditionalManifestPaginatorTypeDef],
        "AudioChannelConfigSchemeIdUri": DashIsoGroupAudioChannelConfigSchemeIdUriType,
        "BaseUrl": str,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": DashIsoEncryptionSettingsPaginatorTypeDef,
        "FragmentLength": int,
        "HbbtvCompliance": DashIsoHbbtvComplianceType,
        "ImageBasedTrickPlay": DashIsoImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": DashIsoImageBasedTrickPlaySettingsTypeDef,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": DashIsoMpdManifestBandwidthTypeType,
        "MpdProfile": DashIsoMpdProfileType,
        "PtsOffsetHandlingForBFrames": DashIsoPtsOffsetHandlingForBFramesType,
        "SegmentControl": DashIsoSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": DashIsoSegmentLengthControlType,
        "VideoCompositionOffsets": DashIsoVideoCompositionOffsetsType,
        "WriteSegmentTimelineInRepresentation": DashIsoWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

DashIsoGroupSettingsTypeDef = TypedDict(
    "DashIsoGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[DashAdditionalManifestTypeDef],
        "AudioChannelConfigSchemeIdUri": DashIsoGroupAudioChannelConfigSchemeIdUriType,
        "BaseUrl": str,
        "DashManifestStyle": DashManifestStyleType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": DashIsoEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "HbbtvCompliance": DashIsoHbbtvComplianceType,
        "ImageBasedTrickPlay": DashIsoImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": DashIsoImageBasedTrickPlaySettingsTypeDef,
        "MinBufferTime": int,
        "MinFinalSegmentLength": float,
        "MpdManifestBandwidthType": DashIsoMpdManifestBandwidthTypeType,
        "MpdProfile": DashIsoMpdProfileType,
        "PtsOffsetHandlingForBFrames": DashIsoPtsOffsetHandlingForBFramesType,
        "SegmentControl": DashIsoSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": DashIsoSegmentLengthControlType,
        "VideoCompositionOffsets": DashIsoVideoCompositionOffsetsType,
        "WriteSegmentTimelineInRepresentation": DashIsoWriteSegmentTimelineInRepresentationType,
    },
    total=False,
)

FileGroupSettingsTypeDef = TypedDict(
    "FileGroupSettingsTypeDef",
    {
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
    },
    total=False,
)

HlsGroupSettingsPaginatorTypeDef = TypedDict(
    "HlsGroupSettingsPaginatorTypeDef",
    {
        "AdMarkers": List[HlsAdMarkersType],
        "AdditionalManifests": List[HlsAdditionalManifestPaginatorTypeDef],
        "AudioOnlyHeader": HlsAudioOnlyHeaderType,
        "BaseUrl": str,
        "CaptionLanguageMappings": List[HlsCaptionLanguageMappingTypeDef],
        "CaptionLanguageSetting": HlsCaptionLanguageSettingType,
        "CaptionSegmentLengthControl": HlsCaptionSegmentLengthControlType,
        "ClientCache": HlsClientCacheType,
        "CodecSpecification": HlsCodecSpecificationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "DirectoryStructure": HlsDirectoryStructureType,
        "Encryption": HlsEncryptionSettingsPaginatorTypeDef,
        "ImageBasedTrickPlay": HlsImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": HlsImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": HlsManifestCompressionType,
        "ManifestDurationFormat": HlsManifestDurationFormatType,
        "MinFinalSegmentLength": float,
        "MinSegmentLength": int,
        "OutputSelection": HlsOutputSelectionType,
        "ProgramDateTime": HlsProgramDateTimeType,
        "ProgramDateTimePeriod": int,
        "ProgressiveWriteHlsManifest": HlsProgressiveWriteHlsManifestType,
        "SegmentControl": HlsSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": HlsSegmentLengthControlType,
        "SegmentsPerSubdirectory": int,
        "StreamInfResolution": HlsStreamInfResolutionType,
        "TargetDurationCompatibilityMode": HlsTargetDurationCompatibilityModeType,
        "TimedMetadataId3Frame": HlsTimedMetadataId3FrameType,
        "TimedMetadataId3Period": int,
        "TimestampDeltaMilliseconds": int,
    },
    total=False,
)

HlsGroupSettingsTypeDef = TypedDict(
    "HlsGroupSettingsTypeDef",
    {
        "AdMarkers": Sequence[HlsAdMarkersType],
        "AdditionalManifests": Sequence[HlsAdditionalManifestTypeDef],
        "AudioOnlyHeader": HlsAudioOnlyHeaderType,
        "BaseUrl": str,
        "CaptionLanguageMappings": Sequence[HlsCaptionLanguageMappingTypeDef],
        "CaptionLanguageSetting": HlsCaptionLanguageSettingType,
        "CaptionSegmentLengthControl": HlsCaptionSegmentLengthControlType,
        "ClientCache": HlsClientCacheType,
        "CodecSpecification": HlsCodecSpecificationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "DirectoryStructure": HlsDirectoryStructureType,
        "Encryption": HlsEncryptionSettingsTypeDef,
        "ImageBasedTrickPlay": HlsImageBasedTrickPlayType,
        "ImageBasedTrickPlaySettings": HlsImageBasedTrickPlaySettingsTypeDef,
        "ManifestCompression": HlsManifestCompressionType,
        "ManifestDurationFormat": HlsManifestDurationFormatType,
        "MinFinalSegmentLength": float,
        "MinSegmentLength": int,
        "OutputSelection": HlsOutputSelectionType,
        "ProgramDateTime": HlsProgramDateTimeType,
        "ProgramDateTimePeriod": int,
        "ProgressiveWriteHlsManifest": HlsProgressiveWriteHlsManifestType,
        "SegmentControl": HlsSegmentControlType,
        "SegmentLength": int,
        "SegmentLengthControl": HlsSegmentLengthControlType,
        "SegmentsPerSubdirectory": int,
        "StreamInfResolution": HlsStreamInfResolutionType,
        "TargetDurationCompatibilityMode": HlsTargetDurationCompatibilityModeType,
        "TimedMetadataId3Frame": HlsTimedMetadataId3FrameType,
        "TimedMetadataId3Period": int,
        "TimestampDeltaMilliseconds": int,
    },
    total=False,
)

MsSmoothGroupSettingsPaginatorTypeDef = TypedDict(
    "MsSmoothGroupSettingsPaginatorTypeDef",
    {
        "AdditionalManifests": List[MsSmoothAdditionalManifestPaginatorTypeDef],
        "AudioDeduplication": MsSmoothAudioDeduplicationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": MsSmoothEncryptionSettingsPaginatorTypeDef,
        "FragmentLength": int,
        "FragmentLengthControl": MsSmoothFragmentLengthControlType,
        "ManifestEncoding": MsSmoothManifestEncodingType,
    },
    total=False,
)

MsSmoothGroupSettingsTypeDef = TypedDict(
    "MsSmoothGroupSettingsTypeDef",
    {
        "AdditionalManifests": Sequence[MsSmoothAdditionalManifestTypeDef],
        "AudioDeduplication": MsSmoothAudioDeduplicationType,
        "Destination": str,
        "DestinationSettings": DestinationSettingsTypeDef,
        "Encryption": MsSmoothEncryptionSettingsTypeDef,
        "FragmentLength": int,
        "FragmentLengthControl": MsSmoothFragmentLengthControlType,
        "ManifestEncoding": MsSmoothManifestEncodingType,
    },
    total=False,
)

VideoDescriptionPaginatorTypeDef = TypedDict(
    "VideoDescriptionPaginatorTypeDef",
    {
        "AfdSignaling": AfdSignalingType,
        "AntiAlias": AntiAliasType,
        "CodecSettings": VideoCodecSettingsTypeDef,
        "ColorMetadata": ColorMetadataType,
        "Crop": RectangleTypeDef,
        "DropFrameTimecode": DropFrameTimecodeType,
        "FixedAfd": int,
        "Height": int,
        "Position": RectangleTypeDef,
        "RespondToAfd": RespondToAfdType,
        "ScalingBehavior": ScalingBehaviorType,
        "Sharpness": int,
        "TimecodeInsertion": VideoTimecodeInsertionType,
        "VideoPreprocessors": VideoPreprocessorPaginatorTypeDef,
        "Width": int,
    },
    total=False,
)

VideoDescriptionTypeDef = TypedDict(
    "VideoDescriptionTypeDef",
    {
        "AfdSignaling": AfdSignalingType,
        "AntiAlias": AntiAliasType,
        "CodecSettings": VideoCodecSettingsTypeDef,
        "ColorMetadata": ColorMetadataType,
        "Crop": RectangleTypeDef,
        "DropFrameTimecode": DropFrameTimecodeType,
        "FixedAfd": int,
        "Height": int,
        "Position": RectangleTypeDef,
        "RespondToAfd": RespondToAfdType,
        "ScalingBehavior": ScalingBehaviorType,
        "Sharpness": int,
        "TimecodeInsertion": VideoTimecodeInsertionType,
        "VideoPreprocessors": VideoPreprocessorTypeDef,
        "Width": int,
    },
    total=False,
)

InputPaginatorTypeDef = TypedDict(
    "InputPaginatorTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Dict[str, AudioSelectorGroupPaginatorTypeDef],
        "AudioSelectors": Dict[str, AudioSelectorPaginatorTypeDef],
        "CaptionSelectors": Dict[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DecryptionSettings": InputDecryptionSettingsTypeDef,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FileInput": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterPaginatorTypeDef,
        "InputClippings": List[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "SupplementalImps": List[str],
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoGenerator": InputVideoGeneratorTypeDef,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

InputTemplatePaginatorTypeDef = TypedDict(
    "InputTemplatePaginatorTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Dict[str, AudioSelectorGroupPaginatorTypeDef],
        "AudioSelectors": Dict[str, AudioSelectorPaginatorTypeDef],
        "CaptionSelectors": Dict[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterPaginatorTypeDef,
        "InputClippings": List[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

InputTemplateTypeDef = TypedDict(
    "InputTemplateTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Mapping[str, AudioSelectorGroupTypeDef],
        "AudioSelectors": Mapping[str, AudioSelectorTypeDef],
        "CaptionSelectors": Mapping[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterTypeDef,
        "InputClippings": Sequence[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "AdvancedInputFilter": AdvancedInputFilterType,
        "AdvancedInputFilterSettings": AdvancedInputFilterSettingsTypeDef,
        "AudioSelectorGroups": Mapping[str, AudioSelectorGroupTypeDef],
        "AudioSelectors": Mapping[str, AudioSelectorTypeDef],
        "CaptionSelectors": Mapping[str, CaptionSelectorTypeDef],
        "Crop": RectangleTypeDef,
        "DeblockFilter": InputDeblockFilterType,
        "DecryptionSettings": InputDecryptionSettingsTypeDef,
        "DenoiseFilter": InputDenoiseFilterType,
        "DolbyVisionMetadataXml": str,
        "FileInput": str,
        "FilterEnable": InputFilterEnableType,
        "FilterStrength": int,
        "ImageInserter": ImageInserterTypeDef,
        "InputClippings": Sequence[InputClippingTypeDef],
        "InputScanType": InputScanTypeType,
        "Position": RectangleTypeDef,
        "ProgramNumber": int,
        "PsiControl": InputPsiControlType,
        "SupplementalImps": Sequence[str],
        "TimecodeSource": InputTimecodeSourceType,
        "TimecodeStart": str,
        "VideoGenerator": InputVideoGeneratorTypeDef,
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

OutputGroupSettingsPaginatorTypeDef = TypedDict(
    "OutputGroupSettingsPaginatorTypeDef",
    {
        "CmafGroupSettings": CmafGroupSettingsPaginatorTypeDef,
        "DashIsoGroupSettings": DashIsoGroupSettingsPaginatorTypeDef,
        "FileGroupSettings": FileGroupSettingsTypeDef,
        "HlsGroupSettings": HlsGroupSettingsPaginatorTypeDef,
        "MsSmoothGroupSettings": MsSmoothGroupSettingsPaginatorTypeDef,
        "Type": OutputGroupTypeType,
    },
    total=False,
)

OutputGroupSettingsTypeDef = TypedDict(
    "OutputGroupSettingsTypeDef",
    {
        "CmafGroupSettings": CmafGroupSettingsTypeDef,
        "DashIsoGroupSettings": DashIsoGroupSettingsTypeDef,
        "FileGroupSettings": FileGroupSettingsTypeDef,
        "HlsGroupSettings": HlsGroupSettingsTypeDef,
        "MsSmoothGroupSettings": MsSmoothGroupSettingsTypeDef,
        "Type": OutputGroupTypeType,
    },
    total=False,
)

OutputPaginatorTypeDef = TypedDict(
    "OutputPaginatorTypeDef",
    {
        "AudioDescriptions": List[AudioDescriptionPaginatorTypeDef],
        "CaptionDescriptions": List[CaptionDescriptionPaginatorTypeDef],
        "ContainerSettings": ContainerSettingsPaginatorTypeDef,
        "Extension": str,
        "NameModifier": str,
        "OutputSettings": OutputSettingsTypeDef,
        "Preset": str,
        "VideoDescription": VideoDescriptionPaginatorTypeDef,
    },
    total=False,
)

PresetSettingsPaginatorTypeDef = TypedDict(
    "PresetSettingsPaginatorTypeDef",
    {
        "AudioDescriptions": List[AudioDescriptionPaginatorTypeDef],
        "CaptionDescriptions": List[CaptionDescriptionPresetPaginatorTypeDef],
        "ContainerSettings": ContainerSettingsPaginatorTypeDef,
        "VideoDescription": VideoDescriptionPaginatorTypeDef,
    },
    total=False,
)

OutputTypeDef = TypedDict(
    "OutputTypeDef",
    {
        "AudioDescriptions": Sequence[AudioDescriptionTypeDef],
        "CaptionDescriptions": Sequence[CaptionDescriptionTypeDef],
        "ContainerSettings": ContainerSettingsTypeDef,
        "Extension": str,
        "NameModifier": str,
        "OutputSettings": OutputSettingsTypeDef,
        "Preset": str,
        "VideoDescription": VideoDescriptionTypeDef,
    },
    total=False,
)

PresetSettingsTypeDef = TypedDict(
    "PresetSettingsTypeDef",
    {
        "AudioDescriptions": Sequence[AudioDescriptionTypeDef],
        "CaptionDescriptions": Sequence[CaptionDescriptionPresetTypeDef],
        "ContainerSettings": ContainerSettingsTypeDef,
        "VideoDescription": VideoDescriptionTypeDef,
    },
    total=False,
)

OutputGroupPaginatorTypeDef = TypedDict(
    "OutputGroupPaginatorTypeDef",
    {
        "AutomatedEncodingSettings": AutomatedEncodingSettingsPaginatorTypeDef,
        "CustomName": str,
        "Name": str,
        "OutputGroupSettings": OutputGroupSettingsPaginatorTypeDef,
        "Outputs": List[OutputPaginatorTypeDef],
    },
    total=False,
)

_RequiredPresetPaginatorTypeDef = TypedDict(
    "_RequiredPresetPaginatorTypeDef",
    {
        "Name": str,
        "Settings": PresetSettingsPaginatorTypeDef,
    },
)
_OptionalPresetPaginatorTypeDef = TypedDict(
    "_OptionalPresetPaginatorTypeDef",
    {
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "LastUpdated": datetime,
        "Type": TypeType,
    },
    total=False,
)


class PresetPaginatorTypeDef(_RequiredPresetPaginatorTypeDef, _OptionalPresetPaginatorTypeDef):
    pass


OutputGroupTypeDef = TypedDict(
    "OutputGroupTypeDef",
    {
        "AutomatedEncodingSettings": AutomatedEncodingSettingsTypeDef,
        "CustomName": str,
        "Name": str,
        "OutputGroupSettings": OutputGroupSettingsTypeDef,
        "Outputs": Sequence[OutputTypeDef],
    },
    total=False,
)

_RequiredCreatePresetRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePresetRequestRequestTypeDef",
    {
        "Name": str,
        "Settings": PresetSettingsTypeDef,
    },
)
_OptionalCreatePresetRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePresetRequestRequestTypeDef",
    {
        "Category": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePresetRequestRequestTypeDef(
    _RequiredCreatePresetRequestRequestTypeDef, _OptionalCreatePresetRequestRequestTypeDef
):
    pass


_RequiredPresetTypeDef = TypedDict(
    "_RequiredPresetTypeDef",
    {
        "Name": str,
        "Settings": PresetSettingsTypeDef,
    },
)
_OptionalPresetTypeDef = TypedDict(
    "_OptionalPresetTypeDef",
    {
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "LastUpdated": datetime,
        "Type": TypeType,
    },
    total=False,
)


class PresetTypeDef(_RequiredPresetTypeDef, _OptionalPresetTypeDef):
    pass


_RequiredUpdatePresetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePresetRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdatePresetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePresetRequestRequestTypeDef",
    {
        "Category": str,
        "Description": str,
        "Settings": PresetSettingsTypeDef,
    },
    total=False,
)


class UpdatePresetRequestRequestTypeDef(
    _RequiredUpdatePresetRequestRequestTypeDef, _OptionalUpdatePresetRequestRequestTypeDef
):
    pass


JobSettingsPaginatorTypeDef = TypedDict(
    "JobSettingsPaginatorTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": List[InputPaginatorTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": List[OutputGroupPaginatorTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionPaginatorTypeDef,
    },
    total=False,
)

JobTemplateSettingsPaginatorTypeDef = TypedDict(
    "JobTemplateSettingsPaginatorTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": List[InputTemplatePaginatorTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": List[OutputGroupPaginatorTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionPaginatorTypeDef,
    },
    total=False,
)

ListPresetsResponsePaginatorTypeDef = TypedDict(
    "ListPresetsResponsePaginatorTypeDef",
    {
        "NextToken": str,
        "Presets": List[PresetPaginatorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobSettingsTypeDef = TypedDict(
    "JobSettingsTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": Sequence[InputTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": Sequence[OutputGroupTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionTypeDef,
    },
    total=False,
)

JobTemplateSettingsTypeDef = TypedDict(
    "JobTemplateSettingsTypeDef",
    {
        "AdAvailOffset": int,
        "AvailBlanking": AvailBlankingTypeDef,
        "Esam": EsamSettingsTypeDef,
        "ExtendedDataServices": ExtendedDataServicesTypeDef,
        "Inputs": Sequence[InputTemplateTypeDef],
        "KantarWatermark": KantarWatermarkSettingsTypeDef,
        "MotionImageInserter": MotionImageInserterTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
        "NielsenNonLinearWatermark": NielsenNonLinearWatermarkSettingsTypeDef,
        "OutputGroups": Sequence[OutputGroupTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "TimedMetadataInsertion": TimedMetadataInsertionTypeDef,
    },
    total=False,
)

CreatePresetResponseTypeDef = TypedDict(
    "CreatePresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPresetResponseTypeDef = TypedDict(
    "GetPresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPresetsResponseTypeDef = TypedDict(
    "ListPresetsResponseTypeDef",
    {
        "NextToken": str,
        "Presets": List[PresetTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePresetResponseTypeDef = TypedDict(
    "UpdatePresetResponseTypeDef",
    {
        "Preset": PresetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJobPaginatorTypeDef = TypedDict(
    "_RequiredJobPaginatorTypeDef",
    {
        "Role": str,
        "Settings": JobSettingsPaginatorTypeDef,
    },
)
_OptionalJobPaginatorTypeDef = TypedDict(
    "_OptionalJobPaginatorTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "AccelerationStatus": AccelerationStatusType,
        "Arn": str,
        "BillingTagsSource": BillingTagsSourceType,
        "ClientRequestToken": str,
        "CreatedAt": datetime,
        "CurrentPhase": JobPhaseType,
        "ErrorCode": int,
        "ErrorMessage": str,
        "HopDestinations": List[HopDestinationTypeDef],
        "Id": str,
        "JobPercentComplete": int,
        "JobTemplate": str,
        "Messages": JobMessagesTypeDef,
        "OutputGroupDetails": List[OutputGroupDetailTypeDef],
        "Priority": int,
        "Queue": str,
        "QueueTransitions": List[QueueTransitionTypeDef],
        "RetryCount": int,
        "SimulateReservedQueue": SimulateReservedQueueType,
        "Status": JobStatusType,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Timing": TimingTypeDef,
        "UserMetadata": Dict[str, str],
        "Warnings": List[WarningGroupTypeDef],
    },
    total=False,
)


class JobPaginatorTypeDef(_RequiredJobPaginatorTypeDef, _OptionalJobPaginatorTypeDef):
    pass


_RequiredJobTemplatePaginatorTypeDef = TypedDict(
    "_RequiredJobTemplatePaginatorTypeDef",
    {
        "Name": str,
        "Settings": JobTemplateSettingsPaginatorTypeDef,
    },
)
_OptionalJobTemplatePaginatorTypeDef = TypedDict(
    "_OptionalJobTemplatePaginatorTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "HopDestinations": List[HopDestinationTypeDef],
        "LastUpdated": datetime,
        "Priority": int,
        "Queue": str,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Type": TypeType,
    },
    total=False,
)


class JobTemplatePaginatorTypeDef(
    _RequiredJobTemplatePaginatorTypeDef, _OptionalJobTemplatePaginatorTypeDef
):
    pass


_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "Role": str,
        "Settings": JobSettingsTypeDef,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "BillingTagsSource": BillingTagsSourceType,
        "ClientRequestToken": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "JobTemplate": str,
        "Priority": int,
        "Queue": str,
        "SimulateReservedQueue": SimulateReservedQueueType,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Tags": Mapping[str, str],
        "UserMetadata": Mapping[str, str],
    },
    total=False,
)


class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass


_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "Role": str,
        "Settings": JobSettingsTypeDef,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "AccelerationStatus": AccelerationStatusType,
        "Arn": str,
        "BillingTagsSource": BillingTagsSourceType,
        "ClientRequestToken": str,
        "CreatedAt": datetime,
        "CurrentPhase": JobPhaseType,
        "ErrorCode": int,
        "ErrorMessage": str,
        "HopDestinations": List[HopDestinationTypeDef],
        "Id": str,
        "JobPercentComplete": int,
        "JobTemplate": str,
        "Messages": JobMessagesTypeDef,
        "OutputGroupDetails": List[OutputGroupDetailTypeDef],
        "Priority": int,
        "Queue": str,
        "QueueTransitions": List[QueueTransitionTypeDef],
        "RetryCount": int,
        "SimulateReservedQueue": SimulateReservedQueueType,
        "Status": JobStatusType,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Timing": TimingTypeDef,
        "UserMetadata": Dict[str, str],
        "Warnings": List[WarningGroupTypeDef],
    },
    total=False,
)


class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass


_RequiredCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
        "Settings": JobTemplateSettingsTypeDef,
    },
)
_OptionalCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobTemplateRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Category": str,
        "Description": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "Priority": int,
        "Queue": str,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateJobTemplateRequestRequestTypeDef(
    _RequiredCreateJobTemplateRequestRequestTypeDef, _OptionalCreateJobTemplateRequestRequestTypeDef
):
    pass


_RequiredJobTemplateTypeDef = TypedDict(
    "_RequiredJobTemplateTypeDef",
    {
        "Name": str,
        "Settings": JobTemplateSettingsTypeDef,
    },
)
_OptionalJobTemplateTypeDef = TypedDict(
    "_OptionalJobTemplateTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Arn": str,
        "Category": str,
        "CreatedAt": datetime,
        "Description": str,
        "HopDestinations": List[HopDestinationTypeDef],
        "LastUpdated": datetime,
        "Priority": int,
        "Queue": str,
        "StatusUpdateInterval": StatusUpdateIntervalType,
        "Type": TypeType,
    },
    total=False,
)


class JobTemplateTypeDef(_RequiredJobTemplateTypeDef, _OptionalJobTemplateTypeDef):
    pass


_RequiredUpdateJobTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobTemplateRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateJobTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobTemplateRequestRequestTypeDef",
    {
        "AccelerationSettings": AccelerationSettingsTypeDef,
        "Category": str,
        "Description": str,
        "HopDestinations": Sequence[HopDestinationTypeDef],
        "Priority": int,
        "Queue": str,
        "Settings": JobTemplateSettingsTypeDef,
        "StatusUpdateInterval": StatusUpdateIntervalType,
    },
    total=False,
)


class UpdateJobTemplateRequestRequestTypeDef(
    _RequiredUpdateJobTemplateRequestRequestTypeDef, _OptionalUpdateJobTemplateRequestRequestTypeDef
):
    pass


ListJobsResponsePaginatorTypeDef = TypedDict(
    "ListJobsResponsePaginatorTypeDef",
    {
        "Jobs": List[JobPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobTemplatesResponsePaginatorTypeDef = TypedDict(
    "ListJobTemplatesResponsePaginatorTypeDef",
    {
        "JobTemplates": List[JobTemplatePaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobTemplateResponseTypeDef = TypedDict(
    "CreateJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobTemplateResponseTypeDef = TypedDict(
    "GetJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobTemplatesResponseTypeDef = TypedDict(
    "ListJobTemplatesResponseTypeDef",
    {
        "JobTemplates": List[JobTemplateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobTemplateResponseTypeDef = TypedDict(
    "UpdateJobTemplateResponseTypeDef",
    {
        "JobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
