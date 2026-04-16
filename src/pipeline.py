import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from src.transformers import cargar_y_limpiar_pitchfork

def build_pitchfork_pipeline():
    """
    Construye un Pipeline de Scikit-Learn que integra la limpieza
    y optimizacion de los datos de Pitchfork.
    """

    
    pitchfork_pipe = Pipeline([
        ('cleaner', cargar_y_limpiar_pitchfork())
    ])

    return pitchfork_pipe