# AdjacencyMatrixRepresentation
import pandas as pd

from .RepresentationStrategy import RepresentationStrategy
from utils.matrix_helpers import transform_matrix_to_edgelist

class AdjacencyMatrixRepresentation(RepresentationStrategy):

    def transform(self, df) -> pd.DataFrame:
        return transform_matrix_to_edgelist(df)