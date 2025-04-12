# StdLib
import os
import re
from datetime import date
from pathlib import Path
from typing import Optional, Tuple

# Proyect
from common.logger import logger

from . import paths


def get_latest(dir_path: str, base_name: str, extension: str, max_files: int = 0) -> Path:
    """Free the "latest" file, renaming it to preserve previous versions."""
    lastest_file = Path(dir_path, "latest" + extension)

    if lastest_file.is_file():
        timestamp = date.fromtimestamp(lastest_file.stat().st_mtime)
        new_file = UniqueFileMan(dir_path, base_name, extension, max_files, set_date=timestamp).obtain()
        os.rename(lastest_file, new_file)

    return lastest_file


def obtain(
    dir_path: str,
    base_name: str,
    extension: str,
    max_files: Optional[int] = None,
    append_date: bool = True,
    set_date: Optional[date] = None,
):
    """Returns a unique file name in the specified directory."""
    return UniqueFileMan(dir_path, base_name, extension, max_files, append_date, set_date).obtain()


class UniqueFileMan:
    """Manages file creation, naming, and cleanup within a specified directory."""

    dir_path: Path
    base_name: str
    ext: str
    max_files: Optional[int]
    includes_date: bool

    def __init__(
        self,
        dir_path: str,
        base_name: str,
        extension: str,
        max_files: Optional[int] = None,
        append_date: bool = True,
        set_date: Optional[date] = None,
    ):
        """Initializes the UniqueFileManager instance"""
        self.dir_path = Path(dir_path)
        self.base_name = self._get_base_name(base_name, append_date, set_date)
        self.ext = extension
        self.max_files = max_files
        paths.mkDirs(dir_path)
        if not self.dir_path.is_dir():
            raise ValueError(f"Invalid directory: {dir_path}")

    def _get_base_name(self, base_name: str, append_date: bool, set_date: str) -> str:
        """Returns the base name with an optional date suffix."""
        self.includes_date = True
        if set_date:
            return f"{base_name}_{set_date}_"
        elif append_date:
            return f"{base_name}_{date.today()}_"
        self.includes_date = False
        return f"{base_name}_"

    def obtain(self) -> Path:
        """Generates a unique indexed filename and deletes older files exceeding the limit."""
        matching_files = self.get_matching()
        files = self._delete_older_files(matching_files)
        indexes = self._get_indexes(files)
        unique_name = self._create_unique_filename(indexes)
        return self.dir_path / unique_name

    def get_matching(self) -> list[Path]:
        """Returns a list of existing files matching a pattern of the name and extension."""
        pattern = re.compile(rf"^({re.escape(self.base_name)})\d*{re.escape(self.ext)}$")
        return sorted(
            [
                file_path
                for file_path in self.dir_path.iterdir()
                if file_path.is_file() and pattern.match(file_path.name)
            ],
            key=lambda i: i.stem,
        )

    def _delete_older_files(self, sorted_files: list[Path]) -> list[Path]:
        """Delete and remove older files from the sorted list, removing the exceeding of max_files."""
        if self.max_files is None:
            return sorted_files
        if excess := len(sorted_files) - self.max_files > 0:
            for file_path in sorted_files[:excess]:
                sorted_files.remove(file_path)
                file_path.unlink()
                logger.info(f"Removed old file: {file_path}")
        return sorted_files

    def _get_indexes(self, sorted_files: list[Path]) -> Tuple[int]:
        """Returns a tuple of int indexes extracted from filenames matching a pattern of index and extension."""
        if not sorted_files:
            return tuple()
        pattern = re.compile(rf"_(\d+){re.escape(self.ext)}$")
        return tuple(
            int(match[0])
            for file_path in sorted_files
            if (match := pattern.findall(file_path.name))
        )

    def _create_unique_filename(self, indexes: Tuple[int]) -> str:
        """Generates a unique filename in the specified path by appending a 2-digit number to the base name."""
        n = 1
        if indexes:
            n += max(indexes)
        while True:
            new_filename = f"{self.base_name}{n:02}{self.ext}"
            if not (self.dir_path / new_filename).is_file():
                return new_filename
            n += 1