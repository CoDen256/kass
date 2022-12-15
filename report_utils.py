from typing import List

from model import SystemSnapshot, InitializationReport, VerificationReport, SnapshotDiff


def create_init_report(monitored_path: str, verification_path: str, time_millis: int,
                       snapshot: SystemSnapshot) -> InitializationReport:
    pass


def create_verification_report(monitored_path: str, verification_path: str, time_millis: int, snapshot: SystemSnapshot,
                               diffs: List[SnapshotDiff]) -> VerificationReport:
    pass


def write_init_report(report: InitializationReport, report_file: str):
    pass


def write_verification_report(report: VerificationReport, report_file: str):
    pass
