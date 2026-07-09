# ExcelStrategy.py
import pandas as pd

from .DataLoadingStrategy import DataLoadingStrategy

class ExcelStrategy(DataLoadingStrategy):

    def __init__(self, representation):
        self.representation = representation

    def load(self, file_source) -> pd.DataFrame:

        df = pd.read_excel(file_source, index_col=0)

        return self.representation.transform(df)
