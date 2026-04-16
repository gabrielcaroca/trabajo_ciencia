from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

def build_pitchfork_pipeline():

    return Pipeline([
        ('cleaner', FunctionTransformer(lambda df: df))
    ])