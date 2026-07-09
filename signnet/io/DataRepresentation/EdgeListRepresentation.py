#EdgeListRepresentation
import pandas as pd

from .RepresentationStrategy import RepresentationStrategy

class EdgeListRepresentation(RepresentationStrategy):

    def transform(self, df) -> pd.DataFrame:
        return df