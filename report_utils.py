from itertools import groupby
from typing import List

from model import SystemSnapshot, InitializationReport, VerificationReport, SnapshotDiff, FileSnapshot, DirSnapshot


def count_dirs_files(snapshot: SystemSnapshot) -> tuple[int, int]:
    snapshots = sorted(map(lambda s: str(type(s)), snapshot.snapshots))
    grouped_count_by_type = dict((key, len(list(group))) for key, group in groupby(snapshots))
    return grouped_count_by_type[str(DirSnapshot)], grouped_count_by_type[str(FileSnapshot)]


def create_init_report(monitored_path: str, verification_path: str, time_millis: int,
                       snapshot: SystemSnapshot) -> InitializationReport:
    dirs, files = count_dirs_files(snapshot)
    return InitializationReport(
        monitored_path,
        verification_path,
        dirs,
        files,
        time_millis
    )


def create_verification_report(monitored_path: str, verification_path: str, time_millis: int,
                               snapshot: SystemSnapshot,
                               diffs: List[SnapshotDiff]) -> VerificationReport:
    dirs, files = count_dirs_files(snapshot)
    return VerificationReport(
        monitored_path,
        verification_path,
        dirs,
        files,
        time_millis,
        len(diffs),
        diffs
    )


def write_init_report(report: InitializationReport, report_file: str):
    pass


def write_verification_report(report: VerificationReport, report_file: str):
    pass
