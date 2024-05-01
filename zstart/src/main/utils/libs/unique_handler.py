from typing import List, Set, Optional

import re
from pathlib import Path
from datetime import date

from . import paths
from common.logger import logger

def free_latest_file(dir_path: str, base_name: str, extension: str, max_files: int = 0) -> Path:
    """Manages a "latest" file, ensuring it's always updated with new content while preserving previous versions."""
    lastest_file = Path(dir_path, "latest" + extension)

    if lastest_file.is_file():
        timestamp = date.fromtimestamp(lastest_file.stat().st_mtime)
        new_file = UniqueFileManager(
            dir_path, base_name, extension, max_files, append_date=False, set_date=timestamp
        ).obtain()

        lastest_file.rename(new_file)
    return lastest_file

class UniqueFileManager:
    """Manages file creation, naming, and cleanup within a specified directory."""
    def __init__(self, dir_path: str, base_name: str, extension: str, max_files: Optional[int] = None, appendDate: bool = True, set_date: Optional[date] = None):
        """Initializes the UniqueFileManager instance"""

        self.dir_path = Path(dir_path)
        self.base_name = base_name
        self.ext = extension
        self.max_files = max_files
        if set_date:
            self.base_name += f"_{set_date}_"
        else:
            self.base_name += f"_{date.today()}_" if appendDate else '_'
        paths.mkDirs(dir_path)

    def obtain(self) -> Path:
        """Generates a unique filename, creates the file, and manages file count."""
        matching_files = self.get_matching()
        files = self._remove_older(matching_files)
        indexes = self._get_indexes(files)
        unique_name = self._create_unique_filename(indexes)
        return self.dir_path / unique_name

    def get_matching(self) -> List[Path]:
        """Returns a list of existing files matching a pattern based on the base name and extension."""
        pattern = re.compile(rf"^({re.escape(self.base_name)})\d*{re.escape(self.ext)}$") # ([0-9_\-]*)

        return sorted(
            [file_path
            for file_path in self.dir_path.iterdir()
            if file_path.is_file() and pattern.match(file_path.name)],
            key=lambda i: i.stem
        )

    def _get_indexes(self, files: List[Path]) -> Set[int]:
        """Extracts indexes from filenames matching a pattern."""
        pattern = re.compile(r"_(\d+)$")
        indexes = {
            int(match[0])
            for file_path in files
            if (match := pattern.findall(file_path.name))
        }
        return indexes

    def _remove_older(self, files: List[Path]) -> List[Path]:
        """Removes old files from the directory, keeping at most max_files."""

        if self.max_files is None:
            return
        if len(files) > self.max_files:
            for file_path in files[: len(files) - self.max_files]:
                file_path.unlink()
                files.remove(file_path)
                logger.info(f"Removed old file: {file_path}")
        return files

    def _create_unique_filename(self, indexes: Set[int]) -> str:
        """Generates a unique filename in the specified path by appending a 2-digit number to the base name."""
        n = 1
        if indexes:
            n += max(indexes)
        while True:
            new_filename = f"{self.base_name}{n:02}{self.ext}"
            if not (self.dir_path / new_filename).is_file():
                return new_filename
            n += 1