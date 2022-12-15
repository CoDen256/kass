from model import SystemSnapshot, FileSnapshot, DirSnapshot, HashFunction


def load_snapshot(verification_file: str) -> SystemSnapshot:
    pass


def create_file_snapshot(file_path: str, function: HashFunction) -> FileSnapshot:
    pass


def create_dir_snapshot(dir_path: str) -> DirSnapshot:
    pass


def create_system_snapshot(monitored_path: str, function: HashFunction) -> SystemSnapshot:
    pass


def write_system_snapshot(snapshot: SystemSnapshot, verification_file: str):
    pass
