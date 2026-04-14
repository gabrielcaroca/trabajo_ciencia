import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from src.transformers import PitchforkCleaner # Tu transformador personalizado

def build_pitchfork_pipeline():
    """
    Construye un Pipeline de Scikit-Learn que integra la limpieza
    y optimizacion de los datos de Pitchfork.
    """
    
    # En este caso, como tu limpieza es integral (afecta a todo el dataframe),
    # el pipeline es directo. Si tuvieras modelos de ML, se añadirian aqui.
    
    pitchfork_pipe = Pipeline([
        ('cleaner', PitchforkCleaner())
    ])

    return pitchfork_pipe