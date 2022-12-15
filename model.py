from dataclasses import dataclass
from typing import Literal, List, Any
from datetime import datetime

HashFunction = Literal['md5', 'sha1']
FileDirProperty = Literal['size', 'access rights', 'object', 'message digest', 'user', 'group', 'modification date']
Action = Literal['add', 'delete', 'modify']
Type = Literal['f', 'd']

@dataclass()
class Snapshot:
    full_path: str
    user: str
    group: str
    access_mode: str
    last_modified: datetime


@dataclass(unsafe_hash=True)
class FileSnapshot(Snapshot):
    message_digest: str
    size: int


@dataclass(unsafe_hash=True)
class DirSnapshot(Snapshot):
    pass


@dataclass()
class SystemSnapshot:
    snapshots: List[Snapshot]
    hash_function: HashFunction


@dataclass()
class Report:
    pass


@dataclass()
class InitializationReport:
    pass


@dataclass()
class VerificationReport:
    pass


@dataclass()
class SnapshotDiff:
    action: Action
    path: str
    type: Type
    property: FileDirProperty
    old_value: Any
    new_value: Any
