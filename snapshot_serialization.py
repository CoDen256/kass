import datetime

from io_utils import read_csv, write_csv
from model import SystemSnapshot, Snapshot, FileSnapshot, DirSnapshot, HashFunction


# DESERIALIZE #
def parse_snapshot(row) -> Snapshot:
    path, type, user, group, access_mode, modified_date, hash, size = tuple(row)
    modified_date = datetime.datetime.strptime(modified_date, "%m-%d-%YT%H:%M:%S")
    size = int(size)
    if type == "f":
        return FileSnapshot(path, user, group, access_mode, modified_date, hash, size)
    if type == "d":
        return DirSnapshot(path, user, group, access_mode, modified_date)
    raise Exception(f"Unable to parse snapshot: {row}")


def parse_header(row) -> HashFunction:
    return row[6]


def load_system_snapshot(verification_file: str) -> SystemSnapshot:
    hash_function, snapshots = read_csv(verification_file, parse_snapshot, parse_header)
    return SystemSnapshot(snapshots, hash_function)


# SERIALIZE #
def format_snapshot(snapshot: Snapshot) -> tuple[str, str, str, str, str, str, str, str]:
    modified = snapshot.last_modified.strftime("%m-%d-%YT%H:%M:%S")
    hash = snapshot.message_digest if isinstance(snapshot, FileSnapshot) else None
    size = str(snapshot.size) if isinstance(snapshot, FileSnapshot) else None
    return snapshot.full_path, snapshot.get_type(), snapshot.user, snapshot.group, snapshot.access_mode, modified, hash, size


def format_header(snapshot: SystemSnapshot) -> tuple[str, str, str, str, str, str, str, str]:
    return "path", "type", "user", "group", "access_mode", "modified_date", snapshot.hash_function, "size"


def write_system_snapshot(snapshot: SystemSnapshot, verification_file: str):
    content = [format_snapshot(s) for s in snapshot.snapshots]
    header = format_header(snapshot)
    write_csv(verification_file, [header] + content)
