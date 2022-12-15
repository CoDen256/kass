from diff_utils import compare_snapshots
from report_utils import write_verification_report, write_init_report, create_verification_report, create_init_report
from snapshot_utils import load_snapshot, create_system_snapshot, write_system_snapshot
from model import HashFunction


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
    report = create_init_report(monitored_dir, verification_file, ended - started, snapshot)
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