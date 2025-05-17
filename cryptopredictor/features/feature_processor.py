import pandas as pd
from sklearn.preprocessing import StandardScaler

class FeatureProcessor:
    # dataset column scaling
    
    def __init__(self):        
        self.scaler = StandardScaler()
    
    def scale_features(self, X_train, X_test):
        #scale dataset columns using sklearn
        #params: X_train(DataFrame): training data
        #params: X_test(DataFrame): test data
        #returns: tuple: scaled training and test data
        
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train), 
            columns=X_train.columns
        )
        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test), 
            columns=X_test.columns
        )
        
        return X_train_scaled, X_test_scaled
