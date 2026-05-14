"""
Pipeline configuration for the Pitchfork SQLite dataset.
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold

from src.transformers import (
    PitchforkCleanerTransformer, ContentFeatureTransformer, DropColumnsTransformer
)

def build_pitchfork_pipeline(columns_to_drop=None):
    """Builds and returns the scikit-learn preprocessing pipeline."""
    if columns_to_drop is None:
        # Eliminamos la reseña en texto crudo y URLs que no sirven para el modelo matemático
        columns_to_drop = ['content', 'url', 'reviewid', 'artist', 'label']

    # Ruta para variables numéricas (incluyendo nuestro nuevo conteo de palabras)
    num_pipe = Pipeline([
        ('zero_variance', VarianceThreshold(threshold=0.0)),
        ('scaler', StandardScaler())
    ])

    # Ruta para variables categóricas
    cat_pipe = Pipeline([
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipe, make_column_selector(dtype_include='number')),
            ('cat', cat_pipe, make_column_selector(dtype_exclude='number'))
        ],
        remainder='drop'
    )

    full_pipeline = Pipeline([
        ('cleaner', PitchforkCleanerTransformer()),
        ('content_features', ContentFeatureTransformer()),
        ('drop_cols', DropColumnsTransformer(columns_to_drop=columns_to_drop)),
        ('preprocessing', preprocessor)
    ])

    # Obligamos a que mantenga la salida como DataFrame
    full_pipeline.set_output(transform="pandas")
    
    return full_pipeline