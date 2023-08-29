from typing import List, Optional

import pandas as pd

from ltr_datasets.datasets.base import DatasetLoader
from ltr_datasets.transformations import Transformation
from ltr_datasets.util.file import unarchive, verify_file
from ltr_datasets.util.svmlight import read_svmlight_file


class Yahoo(DatasetLoader):
    name = "Yahoo"
    file = "ltrc_yahoo"
    zip_file = "ltrc_yahoo.tgz"
    checksum = "d82bcaa8eae8f89db88c87a9fce819ec6fa86dba3fa8b09e531364cc23f916a7"
    n_features: int = 699

    def __init__(
        self,
        fold: int,
        transform: Optional[List[Transformation]] = None,
    ):
        super().__init__(self.name, fold, transform)

    def _parse(self, split: str) -> pd.DataFrame:
        zip_path = self.download_directory / self.zip_file

        if not zip_path.exists():
            raise FileNotFoundError(
                f"""
            Cannot find the Yahoo LTR 2.0 dataset at: {zip_path}
            
            Yahoo LTR 2.0 cannot be automatically downloaded.
            Please apply for access to the C14B dataset online at:
            https://webscope.sandbox.yahoo.com/catalog.php?datatype=c
            
            Unzip the downloaded file and place the inner archive {self.zip_file} at:
            {zip_path}
            """
            )

        verify_file(zip_path, self.checksum)
        dataset_path = unarchive(zip_path, self.dataset_directory / self.file)

        split = "valid" if split == "val" else split
        path = dataset_path / f"set{self.fold}.{split}.txt"

        return read_svmlight_file(path)

    @property
    def folds(self) -> List[int]:
        return [1, 2, 3, 4, 5]

    @property
    def splits(self) -> List[str]:
        return ["train", "test", "val"]
