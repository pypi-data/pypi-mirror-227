from typing import Dict, Optional
from typing import List

import pandas as pd

from ltr_datasets.datasets.base import DatasetLoader
from ltr_datasets.transformations import Transformation
from ltr_datasets.util.file import download, verify_file, unarchive
from ltr_datasets.util.svmlight import read_svmlight_file


class MSLR10K(DatasetLoader):
    name: str = "MSLR-WEB10K"
    url: str = "https://api.onedrive.com/v1.0/shares/s!AtsMfWUz5l8nbOIoJ6Ks0bEMp78/root/content"
    zip_file: str = "MSLR-WEB10K.zip"
    folder: str = "MSLR-WEB10K"
    checksum: str = "2902142ea33f18c59414f654212de5063033b707d5c3939556124b1120d3a0ba"
    n_features: int = 136
    split2file: Dict[str, str] = {
        "train": "train.txt",
        "val": "vali.txt",
        "test": "test.txt",
    }

    def __init__(
        self,
        fold: int,
        transform: Optional[List[Transformation]] = None,
    ):
        super().__init__(self.name, fold, transform)

    def _parse(self, split: str) -> pd.DataFrame:
        zip_path = download(self.url, self.download_directory / self.zip_file)
        verify_file(zip_path, self.checksum)
        dataset_path = unarchive(zip_path, self.dataset_directory / self.folder)
        path = dataset_path / f"Fold{self.fold}" / self.split2file[split]

        return read_svmlight_file(path)

    @property
    def folds(self) -> List[int]:
        return [1, 2, 3, 4, 5]

    @property
    def splits(self) -> List[str]:
        return ["train", "test", "val"]


class MSLR30K(DatasetLoader):
    name: str = "MSLR-WEB30K"
    url: str = "https://api.onedrive.com/v1.0/shares/s!AtsMfWUz5l8nbXGPBlwD1rnFdBY/root/content"
    zip_file: str = "MSLR-WEB30K.zip"
    folder: str = "MSLR-WEB30K"
    checksum: str = "08cb7977e1d5cbdeb57a9a2537a0923dbca6d46a76db9a6afc69e043c85341ae"
    n_features: int = 136
    split2file: Dict[str, str] = {
        "train": "train.txt",
        "val": "vali.txt",
        "test": "test.txt",
    }

    def __init__(
        self,
        fold: int,
        transform: Optional[List[Transformation]] = None,
    ):
        super().__init__(self.name, fold, transform)

    def _parse(self, split: str) -> pd.DataFrame:
        zip_path = download(self.url, self.download_directory / self.zip_file)
        verify_file(zip_path, self.checksum)
        dataset_path = unarchive(zip_path, self.dataset_directory / self.folder)
        path = dataset_path / f"Fold{self.fold}" / self.split2file[split]

        return read_svmlight_file(path)

    @property
    def folds(self) -> List[int]:
        return [1, 2, 3, 4, 5]

    @property
    def splits(self) -> List[str]:
        return ["train", "test", "val"]
