from typing import List

from model import SystemSnapshot, SnapshotDiff, FileSnapshot, DirSnapshot


def compare_snapshots(old: SystemSnapshot, new: SystemSnapshot) -> List[SnapshotDiff]:
    result = []

    for new_object in new.snapshots:
        if new_object in old.snapshots: continue
        if isinstance(new_object, FileSnapshot):
            result.append(SnapshotDiff('add', new_object.full_path, 'f', 'object', None, None))
        else:
            result.append(SnapshotDiff('add', new_object.full_path, 'd', 'object', None, None))

    for old_object in old.snapshots:
        if old_object in new.snapshots: continue
        if isinstance(old_object, FileSnapshot):
            result.append(SnapshotDiff('delete', old_object.full_path, 'f', 'object', None, None))
        else:
            result.append(SnapshotDiff('delete', old_object.full_path, 'd', 'object', None, None))

    return result
