from typing import List
from model import *


def load_snapshot(verification_file: str) -> SystemSnapshot:
    pass


def create_file_snapshot(file_path: str, function: HashFunction) -> FileSnapshot:
    pass


def create_dir_snapshot(dir_path: str) -> DirSnapshot:
    pass


def create_system_snapshot(monitored_path: str, function: HashFunction) -> SystemSnapshot:
    pass


def compare_snapshots(s1: SystemSnapshot, s2: SystemSnapshot) -> List[SnapshotDiff]:
    pass


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


def write_system_snapshot(snapshot: SystemSnapshot, verification_file: str):
    pass


def verify_initialize_mode(monitored_dir: str, report_file: str, verification_file: str, hash_function: HashFunction):
    pass


def verify_verification_mode(monitored_dir: str, report_file: str, verification_file: str):
    pass


def millis() -> int:
    pass


def run_initialize_mode(monitored_dir: str, report_file: str, verification_file: str, hash_function: HashFunction):
    started = millis()
    verify_initialize_mode(monitored_dir, report_file, verification_file, hash_function)

    snapshot = create_system_snapshot(monitored_dir, hash_function)
    write_system_snapshot(snapshot, verification_file)

    ended = millis()
    report = create_init_report(monitored_dir, verification_file, ended-started, snapshot)
    write_init_report(report, report_file)


def run_verification_mode(monitored_dir: str, report_file: str, verification_file: str):
    started = millis()
    verify_verification_mode(monitored_dir, report_file, verification_file)

    previous = load_snapshot(verification_file)
    current = create_system_snapshot(monitored_dir, previous.hash_function)

    diffs = compare_snapshots(previous, current)

    ended = millis()
    report = create_verification_report(monitored_dir, verification_file, ended - started, current, diffs)
    write_verification_report(report, report_file)
