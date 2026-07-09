import pandas as pd

from .DataLoadingStrategy import DataLoadingStrategy

class JsonStrategy(DataLoadingStrategy):

    def __init__(self, representation):
        self.representation = representation

    def load(self, file_source) -> pd.DataFrame:

        df = pd.read_json(file_source, index_col=0)

        return self.representation.transform(df)
