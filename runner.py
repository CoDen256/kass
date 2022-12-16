
import os
import sys

from diff_utils import compare_snapshots
from model import HashFunction
from report_utils import write_verification_report, write_init_report, create_verification_report, create_init_report
from os_utils import is_dir, exists, is_parent_of_file
from snapshot_generation import create_system_snapshot
from snapshot_serialization import load_system_snapshot, write_system_snapshot
import time


def error(message):
    sys.exit(message)


def verify(monitored_dir: str, report_file: str, verification_file: str):
    if not exists(monitored_dir):
        error(f"Monitored directory path does not exist: {monitored_dir}")

    if not is_dir(monitored_dir):
        error(f"Monitored directory path is not a directory: {monitored_dir}")

    if is_parent_of_file(monitored_dir, report_file):
        error(f"Report file should be outside of the monitored directory: {report_file} is inside")

    if is_parent_of_file(monitored_dir, verification_file):
        error(f"Verification file should be outside of the monitored directory: {verification_file} is inside {monitored_dir}")


def verify_initialize_mode(monitored_dir: str, report_file: str, verification_file: str, hash_function: HashFunction):
    verify(monitored_dir, report_file, verification_file)


def verify_verification_mode(monitored_dir: str, report_file: str, verification_file: str):
    verify(monitored_dir, report_file, verification_file)
    if not exists(verification_file):
        error(f"Verification file does not exist {verification_file}")


def millis() -> int:
    return round(time.time() * 1000)


def run_initialize_mode(monitored_dir: str, report_file: str, verification_file: str, hash_function: HashFunction):
    print(f"Running init {monitored_dir} {report_file} {verification_file} {hash_function}")
    started = millis()
    verify_initialize_mode(monitored_dir, report_file, verification_file, hash_function)

    snapshot = create_system_snapshot(monitored_dir, hash_function)
    write_system_snapshot(snapshot, verification_file)

    ended = millis()
    report = create_init_report(monitored_dir, verification_file, report_file, ended - started , snapshot)
    write_init_report(report, report_file)


def run_verification_mode(monitored_dir: str, report_file: str, verification_file: str):
    print(f"Running verify {monitored_dir} {report_file} {verification_file}")
    started = millis()
    verify_verification_mode(monitored_dir, report_file, verification_file)

    previous = load_system_snapshot(verification_file)
    current = create_system_snapshot(monitored_dir, previous.hash_function)

    diffs = compare_snapshots(previous, current)

    ended = millis()
    report = create_verification_report(monitored_dir, verification_file, report_file, ended - started, current, diffs)
    write_verification_report(report, report_file)
