"""
Custom Scikit-Learn transformers for the Pitchfork music reviews dataset.
Handles text cleaning, missing values for categorical data, and feature engineering.
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class PitchforkCleanerTransformer(BaseEstimator, TransformerMixin):
    """Cleans genres and labels, filling missing values with domain defaults."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        # Limpieza de géneros musicales y sellos discográficos
        if 'genre' in X_copy.columns:
            X_copy['genre'] = X_copy['genre'].fillna('unassigned').str.strip().str.lower()
        if 'label' in X_copy.columns:
            X_copy['label'] = X_copy['label'].fillna('independent').str.strip().str.lower()
        return X_copy

    def set_output(self, transform=None):
        """Protocol requirement for scikit-learn >= 1.2 to support pandas output."""
        return self


class ContentFeatureTransformer(BaseEstimator, TransformerMixin):
    """Extracts text-based features like word count from the review content."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        if 'content' in X_copy.columns:
            X_copy['content'] = X_copy['content'].fillna('').str.strip()
            # Feature Engineering: Calculamos qué tan larga es la reseña
            X_copy['review_word_count'] = X_copy['content'].str.split().str.len()
        return X_copy

    def set_output(self, transform=None):
        """Protocol requirement for scikit-learn >= 1.2 to support pandas output."""
        return self


class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    """Drops specified columns to prevent data leakage or remove raw text."""
    def __init__(self, columns_to_drop=None):
        self.columns_to_drop = columns_to_drop if columns_to_drop else []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        cols = [c for c in self.columns_to_drop if c in X_copy.columns]
        return X_copy.drop(columns=cols)

    def set_output(self, transform=None):
        """Protocol requirement for scikit-learn >= 1.2 to support pandas output."""
        return self