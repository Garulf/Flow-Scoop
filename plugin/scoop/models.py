from typing import Dict, List, TypedDict, Union, NotRequired


class BucketExport(TypedDict):
    Name: str
    Source: str
    Updated: Dict
    Manifests: int


class AppExport(TypedDict):
    Info: str
    Source: str
    Name: str
    Version: str
    Updated: str


class ScoopExport(TypedDict):
    buckets: List[BucketExport]
    apps: List[AppExport]


class AppManifest(TypedDict):
    """Partial scoop app manifest"""
    version: str
    description: str
    homepage: str
    license: Union[str, Dict[str, str]]
    url: NotRequired[str]
