import hashlib
import json
import logging
import pickle
import shutil
from pathlib import Path
from typing import Any, Dict

import wget


def sha256_checksum(path: Path, chunk_size: int = 4 * 1024 * 1024):
    """
    https://github.com/rjagerman/pytorchltr/blob/master/pytorchltr/utils/file.py
    """
    hash_sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


def download(url: str, out_path: Path) -> Path:
    if not out_path.exists():
        logging.debug(f"Download archived dataset to: {out_path}")
        wget.download(url, str(out_path))

    assert out_path.exists()
    return out_path


def verify_file(path: Path, checksum: str) -> bool:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if checksum != sha256_checksum(path):
        raise ValueError(f"Checksum verification failed. Wrong or damaged file: {path}")

    return True


def unarchive(in_path: Path, out_path: Path) -> Path:
    if not out_path.exists():
        logging.debug(f"Unpack archived dataset to: {out_path}")
        shutil.unpack_archive(in_path, out_path)

    assert out_path.exists()
    return out_path


def write_to_disk(obj: Any, path: Path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def read_from_disk(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)
