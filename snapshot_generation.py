from model import SystemSnapshot, FileSnapshot, DirSnapshot, HashFunction
from os_utils import walktree, sha256, md5

# CREATE #
def create_file_snapshot(file_path: str, stat_result, function: HashFunction) -> FileSnapshot:
    pass


def create_dir_snapshot(dir_path: str, stat_result) -> DirSnapshot:
    pass


def create_system_snapshot(monitored_path: str, function: HashFunction) -> SystemSnapshot:
    snapshots = []
    walktree(monitored_path,
             lambda f, stat: snapshots.append(create_file_snapshot(f, stat, function)),
             lambda d, stat: snapshots.append(create_dir_snapshot(d, stat)),
             )
    return SystemSnapshot(snapshots, function)