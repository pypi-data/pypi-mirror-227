"""
Type annotations for sagemaker-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""
import sys
from typing import IO, Any, Dict, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BlobTypeDef",
    "InvokeEndpointAsyncInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "InvokeEndpointInputRequestTypeDef",
    "InvokeEndpointAsyncOutputTypeDef",
    "InvokeEndpointOutputTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
InvokeEndpointAsyncInputRequestTypeDef = TypedDict(
    "InvokeEndpointAsyncInputRequestTypeDef",
    {
        "EndpointName": str,
        "InputLocation": str,
        "ContentType": NotRequired[str],
        "Accept": NotRequired[str],
        "CustomAttributes": NotRequired[str],
        "InferenceId": NotRequired[str],
        "RequestTTLSeconds": NotRequired[int],
        "InvocationTimeoutSeconds": NotRequired[int],
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

InvokeEndpointInputRequestTypeDef = TypedDict(
    "InvokeEndpointInputRequestTypeDef",
    {
        "EndpointName": str,
        "Body": BlobTypeDef,
        "ContentType": NotRequired[str],
        "Accept": NotRequired[str],
        "CustomAttributes": NotRequired[str],
        "TargetModel": NotRequired[str],
        "TargetVariant": NotRequired[str],
        "TargetContainerHostname": NotRequired[str],
        "InferenceId": NotRequired[str],
        "EnableExplanations": NotRequired[str],
    },
)

InvokeEndpointAsyncOutputTypeDef = TypedDict(
    "InvokeEndpointAsyncOutputTypeDef",
    {
        "InferenceId": str,
        "OutputLocation": str,
        "FailureLocation": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InvokeEndpointOutputTypeDef = TypedDict(
    "InvokeEndpointOutputTypeDef",
    {
        "Body": StreamingBody,
        "ContentType": str,
        "InvokedProductionVariant": str,
        "CustomAttributes": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
