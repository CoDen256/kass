import enum
from dataclasses import dataclass
from typing import Literal, List, Any
from datetime import datetime
import abc


class HashFunction(enum.Enum):
    MD5 = 'md5'
    SHA1 = 'sha1'


FileDirProperty = Literal['size', 'access', 'object', 'hash', 'user', 'group', 'modified']
Action = Literal['add', 'delete', 'modify']
ObjectType = Literal['f', 'd']


@dataclass()
class Snapshot(abc.ABC):
    full_path: str
    user: str
    group: str
    access_mode: str
    last_modified: datetime

    @abc.abstractmethod
    def get_type(self) -> ObjectType:
        pass


@dataclass(unsafe_hash=True)
class FileSnapshot(Snapshot):
    message_digest: str
    size: int

    def get_type(self) -> ObjectType:
        return "f"


@dataclass(unsafe_hash=True)
class DirSnapshot(Snapshot):
    def get_type(self) -> ObjectType:
        return "d"


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
    type: ObjectType
    property: FileDirProperty
    old_value: Any
    new_value: Any
