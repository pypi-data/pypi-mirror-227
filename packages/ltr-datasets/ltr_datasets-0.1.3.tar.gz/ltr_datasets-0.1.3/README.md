# LTR Datasets

## Installation

```
pip install ltr-datasets
```

## Example

```Python
from ltr_datasets.datasets import MSLR10K
from ltr_datasets.transformations import (
    Log1pNormalize,
    StratifiedTruncate,
)

# Download the Microsoft Learning to Rank Datasets and perform the following transformations:
# 1. Normalize document features.
# 2. Sample 10 documents per query while keeping a similar distribution of relevance labels.
# 3. Queries with less than 10 documents are padded.
loader = MSLR10K(
    fold=1,
    transform=[
        Log1pNormalize(),
        StratifiedTruncate(max_length=10, random_state=42),
    ],
)

# Load PyTorch dataset, which is cached by default after the first load.
# To overwrite the cached dataset, e.g. after changing transformations, use .load(force_reload=True).
dataset = loader.load(split="train")

# Each entry is a search query with id, document features, relevance ratings, and number of documents.
query_id, x, y, n = dataset[0]
```
