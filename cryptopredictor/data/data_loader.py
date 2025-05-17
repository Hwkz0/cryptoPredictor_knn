import pandas as pd
import numpy as np

class DataLoader:
    # Load and process CRYPTO data from CSV
    
    def __init__(self, filepath):
        # params : filepath(str): Path to CSV
        self.filepath = filepath
        self.data = None
        self.numeric_data = None
    
    def load_data(self):
        # reads CSV file
        self.data = pd.read_csv(self.filepath)
        
        # Check if Date column exists and sort data by date (oldest to newest)
        if 'Date' in self.data.columns:
            try:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
                self.data = self.data.sort_values('Date', ascending=True)
                print("Data sorted from oldest to newest date")
            except:
                print("Warning: Could not convert Date column to datetime format for sorting")
                
        return self.data
    
    def print_data_info(self):
        # displays dataset info
        print("Columns:", self.data.columns)
        print("Data shape:", self.data.shape)
        print("Data info:")
        self.data.info()
        print("\nData statistics:")
        print(self.data.describe())
    
    def preprocess_data(self):
        # Handle date column properly before dropping NAs
        if 'Date' in self.data.columns:
            try:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
                # Ensure data is sorted by date (oldest to newest)
                self.data = self.data.sort_values('Date', ascending=True)
            except:
                print("Warning: Could not convert Date column to datetime format")
        
        # delete n.a. columns
        self.numeric_data = self.data.select_dtypes(include=[np.number]).dropna()
        
        print("\nNumeric data shape:", self.numeric_data.shape)
        print("Numeric columns:", self.numeric_data.columns)
        
        # Process all potential price columns (Close, Open, High, Low)
        price_columns = ['Close', 'Open', 'High', 'Low']
        
        for column in price_columns:
            if column in self.numeric_data.columns:
                # Add lagged values for each price column (t-1, t-2, t-3)
                for i in range(1, 4):
                    self.numeric_data[f'{column}_t-{i}'] = self.numeric_data[column].shift(i)
        
        # calc previous day volume
        self.numeric_data['Volume_t-1'] = self.numeric_data['Volume'].shift(1)
        
        # Calculate moving averages for all price columns
        for column in price_columns:
            if column in self.numeric_data.columns:
                self.numeric_data[f'{column}_MA_5'] = self.numeric_data[column].rolling(window=5).mean()
                self.numeric_data[f'{column}_MA_10'] = self.numeric_data[column].rolling(window=10).mean()
                self.numeric_data[f'{column}_Change'] = self.numeric_data[column].diff()
        
        # Use the default MA_5 and MA_10 as aliases for Close's moving averages for backward compatibility
        if 'Close' in self.numeric_data.columns:
            self.numeric_data['MA_5'] = self.numeric_data['Close_MA_5']
            self.numeric_data['MA_10'] = self.numeric_data['Close_MA_10']
            self.numeric_data['Price_Change'] = self.numeric_data['Close_Change']
        
        # delete n.a. rows
        self.numeric_data = self.numeric_data.dropna()
        
        return self.numeric_data
    
    def split_data(self, target_column='Close', test_size=0.2, random_state=42):
        
        from sklearn.model_selection import train_test_split
        
        # Make sure target column exists in the data
        if target_column not in self.numeric_data.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Create target-specific features
        feature_columns = []
        
        # Add lagged values for the target
        for i in range(1, 4):  # t-1, t-2, t-3
            col_name = f'{target_column}_t-{i}'
            if col_name not in self.numeric_data.columns:
                self.numeric_data[col_name] = self.numeric_data[target_column].shift(i)
            feature_columns.append(col_name)
        
        # Add common features
        common_features = ['Volume_t-1', 'MA_5', 'MA_10', 'Price_Change']
        for feature in common_features:
            if feature in self.numeric_data.columns:
                feature_columns.append(feature)
        
        # select relevant columns
        X = self.numeric_data[feature_columns]
        y = self.numeric_data[target_column]
        
        #split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        return X_train, X_test, y_train, y_test, feature_columns
    
    def get_last_days_data(self, days=365):       
        # obtain last n data entries
        #params: days(int): nr of days (default: 365)
        #returns: last n days of data
        
        return self.data.tail(days)
    
    def get_data_info(self):
        info = {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': list(self.data.columns)
        }
        
        # Add date range if 'Date' column exists
        if 'Date' in self.data.columns:
            # Ensure Date column is in datetime format
            if not pd.api.types.is_datetime64_any_dtype(self.data['Date']):
                date_col = pd.to_datetime(self.data['Date'])
            else:
                date_col = self.data['Date']
                
            info['date_range'] = f"{date_col.min().strftime('%Y-%m-%d')} to {date_col.max().strftime('%Y-%m-%d')}"
        else:
            info['date_range'] = "No date column found"
            
        return info
