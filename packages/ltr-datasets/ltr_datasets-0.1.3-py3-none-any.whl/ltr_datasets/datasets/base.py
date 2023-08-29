import logging
from abc import abstractmethod
from os import getenv
from pathlib import Path
from typing import List, Optional, Union, Tuple

import pandas as pd
import torch
from torch import Tensor
from torch.utils.data import Dataset

from ltr_datasets.transformations import Transformation
from ltr_datasets.util.file import write_to_disk, read_from_disk


class RatingDataset(Dataset):
    def __init__(self, df: pd.DataFrame):
        feature_columns = [c for c in df.columns if c.startswith("feature_")]

        query_df = df.groupby(["query_id"]).agg(n=("y", "count")).reset_index()
        feature_df = self._agg_by_query(df, feature_columns, "x")
        target_df = self._agg_by_query(df, "y", "y")

        query_df = query_df.merge(feature_df, on=["query_id"])
        query_df = query_df.merge(target_df, on=["query_id"])

        n_queries = len(query_df)
        n_results = query_df["n"].max()
        n_features = len(feature_columns)

        self.query_ids = torch.zeros((n_queries,), dtype=torch.long)
        self.x = torch.zeros((n_queries, n_results, n_features), dtype=torch.float)
        self.y = torch.zeros((n_queries, n_results), dtype=torch.long)
        self.n = torch.zeros((n_queries,), dtype=torch.long)

        for i, row in query_df.iterrows():
            self.query_ids[i] = row["query_id"]
            self.x[i, : row["n"]] = torch.from_numpy(row["x"])
            self.y[i, : row["n"]] = torch.from_numpy(row["y"])
            self.n[i] = row["n"]

    def __len__(self) -> int:
        return len(self.query_ids)

    def __getitem__(self, idx: int) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
        return self.query_ids[idx], self.x[idx], self.y[idx], self.n[idx]

    @staticmethod
    def _agg_by_query(
        df: pd.DataFrame, columns: Union[str, List[str]], name: str
    ) -> pd.DataFrame:
        return (
            df.groupby(["query_id"])
            .apply(lambda x: x[columns].values)
            .rename(name)
            .reset_index()
        )


class DatasetLoader:
    def __init__(
        self,
        name: str,
        fold: int,
        transform: Optional[List[Transformation]] = None,
    ):
        self.name = name
        self.fold = fold
        self.base_dir = self.base_directory
        self.transform = transform if transform is not None else []

        assert fold in self.folds, f"Fold must be one of {self.folds}"

    @property
    def base_directory(self):
        path = Path(getenv("LTR_DATASETS_DIRECTORY", "~/ltr_datasets"))
        path = path.expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def download_directory(self):
        path = self.base_directory / "download"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def dataset_directory(self):
        path = self.base_directory / "dataset"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def cache_directory(self):
        path = self.base_directory / "cache"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def load(self, split: str, force_reload: bool = False) -> RatingDataset:
        assert split in self.splits, f"Split must be one of {self.splits}"
        path = self.cache_directory / f"{self.name}-fold_{self.fold}-{split}.pkl"

        if not path.exists() or force_reload:
            logging.info(f"Parsing {self.name}-fold_{self.fold}-{split} dataset")
            df = self._parse(split)

            for t in self.transform:
                df = t(df)

            dataset = RatingDataset(df)
            write_to_disk(dataset, path)

        return read_from_disk(path)

    @property
    @abstractmethod
    def folds(self) -> List[int]:
        pass

    @property
    @abstractmethod
    def splits(self) -> List[str]:
        pass

    @abstractmethod
    def _parse(self, split: str) -> pd.DataFrame:
        pass
