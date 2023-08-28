import logging
from typing import List, Optional

import numpy as np
import pandas as pd

from ltr_datasets.transformations.base import (
    FeatureTransformation,
    ColumnTransformation,
)


class ClipNormalize(FeatureTransformation):
    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ):
        self.min_value = min_value
        self.max_value = max_value

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(
            f"Clip document features between: {self.min_value} and {self.max_value}"
        )
        return df.clip(lower=self.min_value, upper=self.max_value)


class MinMaxNormalize(FeatureTransformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"MinMax normalize document features")
        df = (df - df.min()) / (df.max() - df.min())
        df[df.isna()] = 0
        return df


class QueryMinMaxNormalize(ColumnTransformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"MinMax normalize document features per query")
        return df.groupby("query_id").apply(self.scale)

    def scale(self, df: pd.DataFrame):
        query = df["query_id"].values[0]
        df = (df - df.min()) / (df.max() - df.min())
        df[df.isna()] = 0
        df["query_id"] = query
        return df

    def get_columns(self, df) -> List[str]:
        return [c for c in df.columns if c not in ["y"]]


class Log1pNormalize(FeatureTransformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"Log1p normalize document features")
        return np.sign(df) * np.log(np.abs(df) + 1)


class ZScoreNormalize(FeatureTransformation):
    def __init__(self, epsilon: float = 1e-7):
        self.epsilon = epsilon

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"Z-Score normalize document features")
        # Epsilon in case of zero variance features
        return (df - df.mean()) / (df.std() + self.epsilon)
