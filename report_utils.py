from itertools import groupby
from typing import List

from model import SystemSnapshot, InitializationReport, VerificationReport, SnapshotDiff, FileSnapshot, DirSnapshot


def create_init_report(monitored_path: str, verification_path: str, time_millis: int,
                       snapshot: SystemSnapshot) -> InitializationReport:
    snapshots = sorted(map(lambda s: str(type(s)), snapshot.snapshots))
    grouped_count_by_type = dict((key, len(list(group))) for key, group in groupby(snapshots))
    return InitializationReport(
        monitored_path,
        verification_path,
        grouped_count_by_type[str(DirSnapshot)],
        grouped_count_by_type[str(FileSnapshot)],
        time_millis
    )


def create_verification_report(monitored_path: str, verification_path: str, time_millis: int, snapshot: SystemSnapshot,
                               diffs: List[SnapshotDiff]) -> VerificationReport:
    pass


def write_init_report(report: InitializationReport, report_file: str):
    pass


def write_verification_report(report: VerificationReport, report_file: str):
    pass
