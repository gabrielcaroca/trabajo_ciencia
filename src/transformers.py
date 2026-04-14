import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#Elimina data leakage
class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    """Drops specified columns from the DataFrame to prevent Data Leakage."""
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        X_copy = X.copy()
        cols = [col for col in self.columns_to_drop if col in X_copy.columns]
        return X_copy.drop(columns=cols)
    
#Reemplaza 'unknown' por NaN
class UnknownToNaNTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        return X.replace('unknown', np.nan)
    
#Elimina columnas con más de un 80% de nulos    
class DropHighMissingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.cols_to_drop_ = []
        
    def fit(self, X, y=None):
        pct_nulos = X.isnull().mean()
        self.cols_to_drop_ = pct_nulos[pct_nulos > self.threshold].index.tolist()
        return self
        
    def transform(self, X):
        X_copy = X.copy()
        cols = [c for c in self.cols_to_drop_ if c in X_copy.columns]
        return X_copy.drop(columns=cols)
    
#Reemplaza Outliers por IQR
class OutlierCapper(BaseEstimator, TransformerMixin):
    def __init__(self, apply_capping=True):
        self.apply_capping = apply_capping
        self.bounds_ = {}

    def fit(self, X, y=None):
        if not self.apply_capping:
            return self
        for col in X.select_dtypes(include=['number']).columns:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            self.bounds_[col] = (Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
        return self
        
    def transform(self, X):
        X_copy = X.copy()
        if not self.apply_capping:
            return X_copy
        
        for col, (lower, upper) in self.bounds_.items():
            if col in X_copy.columns:
                X_copy[col] = np.clip(X_copy[col], lower, upper)
        return X_copy
    
    def get_feature_names_out(self, input_features=None):
        return input_features
    

#Elimina columnas númericas cuya desviación estándar sea 0
class DropZeroVarianceTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.cols_to_drop_ = []

    def fit(self, X, y=None):
        num_cols = X.select_dtypes(include=['number']).columns
        self.cols_to_drop_ = [col for col in num_cols if X[col].std() == 0]
        return self

    def transform(self, X):
        X_copy = X.copy()
        cols = [c for c in self.cols_to_drop_ if c in X_copy.columns]
        return X_copy.drop(columns=cols)    
    
    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return None
        return np.array([f for f in input_features if f not in self.cols_to_drop_])