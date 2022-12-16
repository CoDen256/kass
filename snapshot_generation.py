import os

from model import SystemSnapshot, FileSnapshot, DirSnapshot, HashFunction
from os_utils import walktree, md5, sha256, get_user, get_group, get_modified, get_access_mode


# CREATE #
def create_file_snapshot(file_path: str, stat_result: os.stat_result, function: HashFunction) -> FileSnapshot:
    compute_hash = {"sha256": sha256, "md5": md5}[function]
    return FileSnapshot(
        full_path=file_path,
        size=stat_result.st_size,
        message_digest=compute_hash(file_path),
        user=get_user(stat_result),
        group=get_group(stat_result),
        last_modified=get_modified(stat_result),
        access_mode=get_access_mode(stat_result)
    )


def create_dir_snapshot(dir_path: str, stat_result) -> DirSnapshot:
    return DirSnapshot(
        full_path=dir_path,
        user=get_user(stat_result),
        group=get_group(stat_result),
        last_modified=get_modified(stat_result),
        access_mode=get_access_mode(stat_result)
    )


def create_system_snapshot(monitored_path: str, function: HashFunction) -> SystemSnapshot:
    snapshots = []
    walktree(monitored_path,
             lambda f, stat: snapshots.append(create_file_snapshot(f, stat, function)),
             lambda d, stat: snapshots.append(create_dir_snapshot(d, stat)),
             )
    return SystemSnapshot(snapshots, function)
