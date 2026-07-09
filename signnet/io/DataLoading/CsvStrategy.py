# CsvStrategy.py
import pandas as pd

from .DataLoadingStrategy import DataLoadingStrategy

class CsvStrategy(DataLoadingStrategy):

    def __init__(self, representation):
        self.representation = representation

    def load(self, file_source) -> pd.DataFrame:

        df = pd.read_csv(file_source, index_col=0)

        return self.representation.transform(df)