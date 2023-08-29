from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class Transformation(ABC):
    @abstractmethod
    def __call__(self, df) -> pd.DataFrame:
        pass

class ColumnTransformation(Transformation, ABC):
    def __call__(self, df):
        columns = self.get_columns(df)
        df.loc[:, columns] = self.transform(df[columns])
        return df

    @abstractmethod
    def transform(self, df) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_columns(self, df) -> List[str]:
        pass


class FeatureTransformation(ColumnTransformation, ABC):
    def get_columns(self, df) -> List[str]:
        return [c for c in df.columns if c.startswith("feature_")]
