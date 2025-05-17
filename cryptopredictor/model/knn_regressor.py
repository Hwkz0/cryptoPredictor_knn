import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from sklearn.base import BaseEstimator, RegressorMixin

class KNNRegressor:
    # KNN regressor using KDTree for fast neighbor search
    
    def __init__(self, k=3):
        # params: k(int): number of neighbors
        self.k = k
        self.X_train = None
        self.y_train = None
        self.tree = None
    
    def fit(self, X_train, y_train):
        # Store training data and build KDTree
        self.X_train = X_train.values if isinstance(X_train, pd.DataFrame) else np.array(X_train)
        self.y_train = y_train.values if hasattr(y_train, "values") else np.array(y_train)
        
        # Build KDTree for fast nearest neighbor search
        self.tree = KDTree(self.X_train)
        return self
    
    def predict(self, X_test):
        # KDTree for KNN
        X_test = X_test.values if isinstance(X_test, pd.DataFrame) else np.array(X_test)
        distances, indices = self.tree.query(X_test, k=self.k)
        
        #multi-output prediction
        if len(self.y_train.shape) > 1 and self.y_train.shape[1] > 1:
            preds = np.array([self.y_train[idx].mean(axis=0) for idx in indices])
        else:
            preds = np.array([self.y_train[idx].mean() for idx in indices])
        
        return preds


class SKLearnKNN(BaseEstimator, RegressorMixin):
    # sklearn wrapper for the above KNNRegressor
    
    def __init__(self, k=3):
        self.k = k
    
    def fit(self, X, y):
        self.model = KNNRegressor(k=self.k)
        self.model.fit(pd.DataFrame(X), y)
        return self
    
    def predict(self, X):
        return self.model.predict(pd.DataFrame(X))
