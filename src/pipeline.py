import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from src.transformers import cargar_y_limpiar_pitchfork

from sklearn.preprocessing import FunctionTransformer

def build_pitchfork_pipeline():

    return Pipeline([
        ('cleaner', FunctionTransformer(lambda X: cargar_y_limpiar_pitchfork(db_path)))
    ])

    return pitchfork_pipe