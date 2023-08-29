from typing import List, Dict, Optional

import pandas as pd

from ltr_datasets.datasets.base import DatasetLoader
from ltr_datasets.transformations import Transformation
from ltr_datasets.util.file import download, verify_file, unarchive
from ltr_datasets.util.svmlight import read_svmlight_file


class Istella(DatasetLoader):
    name: str = "Istella-S"
    url: str = "http://library.istella.it/dataset/istella-s-letor.tar.gz"
    zip_file: str = "istella-s-letor.tar.gz"
    file: str = "ISTELLA"
    checksum: str = "41b21116a3650cc043dbe16f02ee39f4467f9405b37fdbcc9a6a05e230a38981"
    n_features: int = 220
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
        dataset_path = unarchive(zip_path, self.dataset_directory / self.file)
        path = dataset_path / "sample" / self.split2file[split]

        return read_svmlight_file(path)

    @property
    def folds(self) -> List[int]:
        return [1]

    @property
    def splits(self) -> List[str]:
        return ["train", "test", "val"]
