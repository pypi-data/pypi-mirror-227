from cocmd_cli.consts import Consts
import os
from typing import List


def find_cocmd_files(source_label: str, scan_depth: int) -> List[str]:
    locations = []
    depth = 0

    for root, dirs, files in os.walk(source_label):
        if Consts.SOURCE_CONFIG_FILE in files:
            locations.append(root)
        # Counting the depth from the source_label
        relative_root = os.path.relpath(root, source_label)
        depth = relative_root.count(os.sep) if relative_root != "." else 0

        # Stop if the scan depth is reached
        if depth >= scan_depth:
            # Removing dirs will prevent os.walk from traversing deeper
            del dirs[:]

    return locations
