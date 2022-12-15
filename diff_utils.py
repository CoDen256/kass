from typing import List, Any
from collections import defaultdict
from model import SystemSnapshot, SnapshotDiff, FileSnapshot, DirSnapshot, Snapshot, Type


def compare_snapshots(old: SystemSnapshot, new: SystemSnapshot) -> List[SnapshotDiff]:
    old_diff = set(old.snapshots) - set(new.snapshots)
    new_diff = set(new.snapshots) - set(old.snapshots)

    grouped_diff: defaultdict[str, tuple[Snapshot, Snapshot]] = defaultdict(lambda: (None, None))

    for snapshot in old_diff:
        grouped_diff[get_unique_key(snapshot)] = (snapshot, None)

    for snapshot in new_diff:
        (old, _) = grouped_diff[get_unique_key(snapshot)]
        grouped_diff[get_unique_key(snapshot)] = (old, snapshot)

    result = []
    for o, n in grouped_diff.values():
        diff = compare_snapshot(o, n)
        if diff is None: continue
        result.append(diff)
    return result


def get_unique_key(snapshot):
    # creating a unique key from a path and type of the snapshot
    # using / just to be sure, that there are no overlapping with actual files
    return snapshot.full_path + "/" + get_type(snapshot)


def compare_snapshot(old: Snapshot, new: Snapshot) -> SnapshotDiff:
    if old is None:
        return SnapshotDiff('add', new.full_path, get_type(new), 'object', None, None)
    if new is None:
        return SnapshotDiff('delete', old.full_path, get_type(old), 'object', None, None)
    if isinstance(old, FileSnapshot) and isinstance(new, FileSnapshot):
        if new.size != old.size:
            return SnapshotDiff('modify', new.full_path, get_type(new), 'size', old.size, new.size)

    return None


def get_type(snapshot: Snapshot) -> Type:
    if isinstance(snapshot, FileSnapshot):
        return "f"
    if isinstance(snapshot, DirSnapshot):
        return "d"
    raise Exception(f"Undefined type (not directory or file) : {snapshot}")
