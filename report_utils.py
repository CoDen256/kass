from itertools import groupby
from typing import List
from io_utils import write_rows
from model import SystemSnapshot, InitializationReport, VerificationReport, SnapshotDiff, FileSnapshot, DirSnapshot, \
    Report


def count_dirs_files(snapshot: SystemSnapshot) -> tuple[int, int]:
    snapshots = sorted(map(lambda s: str(type(s)), snapshot.snapshots))
    grouped_count_by_type = dict((key, len(list(group))) for key, group in groupby(snapshots))
    return grouped_count_by_type[str(DirSnapshot)], grouped_count_by_type[str(FileSnapshot)]


def create_init_report(monitored_path: str,
                       verification_path: str,
                       report_file: str,
                       time_millis: int,
                       snapshot: SystemSnapshot) -> InitializationReport:
    dirs, files = count_dirs_files(snapshot)
    return InitializationReport(
        monitored_path,
        verification_path,
        report_file,
        dirs,
        files,
        time_millis
    )


def create_verification_report(monitored_path: str,
                               verification_path: str,
                               report_file: str,
                               time_millis: int,
                               snapshot: SystemSnapshot,
                               diffs: List[SnapshotDiff]) -> VerificationReport:
    dirs, files = count_dirs_files(snapshot)
    return VerificationReport(
        monitored_path,
        verification_path,
        report_file,
        dirs,
        files,
        time_millis,
        len(diffs),
        diffs
    )


def format_report(report: Report) -> List[str]:
    return [
        f"Monitored directory: {report.monitored_dir}",
        f"Verification file: {report.verification_file}",
        f"Report file: {report.report_file}",
        f"Directories parsed: {report.directories_parsed}",
        f"Files parsed: {report.files_parsed}",
        f"Time to complete: {report.execution_time} ms",
    ]


def format_init_report(report: InitializationReport) -> List[str]:
    return format_report(report)


def write_init_report(report: InitializationReport, report_file: str):
    write_rows(report_file, format_init_report(report))


def format_diff(diff: SnapshotDiff) -> str:
    action = {"add": "ADDED", "modify": "MODIFIED", "delete": "DELETED"}
    type = {"f": "F", "d": "D"}
    additional = "" if diff.action != "modify" else \
        f": {diff.property} WAS: {diff.old_value} | NOW: {diff.new_value}"
    return f"({type[diff.type]}) {diff.path} {action[diff.action]}{additional}"


def format_verify_report(report: VerificationReport) -> List[str]:
    base = format_report(report)
    warnings = [f"Warnings: {report.warnings}"]
    diffs = [format_diff(diff) for diff in report.diffs]
    return base + warnings + ["\n"] + diffs


def write_verification_report(report: VerificationReport, report_file: str):
    write_rows(report_file, format_verify_report(report))
