from model import SystemSnapshot, FileSnapshot, DirSnapshot, HashFunction


# CREATE #
def create_file_snapshot(file_path: str, function: HashFunction) -> FileSnapshot:
    pass


def create_dir_snapshot(dir_path: str) -> DirSnapshot:
    pass


def create_system_snapshot(monitored_path: str, function: HashFunction) -> SystemSnapshot:
    pass
