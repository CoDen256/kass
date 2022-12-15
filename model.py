from dataclasses import dataclass
from typing import Literal

HashFunction = Literal['md5', 'sha1']


@dataclass()
class Snapshot:
    pass


@dataclass()
class FileSnapshot(Snapshot):
    pass


@dataclass()
class DirSnapshot(Snapshot):
    pass


@dataclass()
class SystemSnapshot:
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
    pass
