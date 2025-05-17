import datetime
import pandas as pd
import numpy as np

class PriceForecaster:    
    #forecast future prices
    
    def __init__(self):
        # Initialize forecaster without requiring model and feature_processor
        pass
    
    def forecast(self, model, scaler, last_days_data, steps, target_column='Close', feature_columns=None):
        forecast = []
        
        #if feature columns aren't explicitly provided, use default ones
        if feature_columns is None:
            feature_columns = [
                f'{target_column}_t-1', f'{target_column}_t-2', f'{target_column}_t-3', 
                'Volume_t-1', 'MA_5', 'MA_10', 'Price_Change'
            ]
        
        #start from last row
        last_row = last_days_data.tail(1)
        
        #extract last values
        current_value = last_row[target_column].values[0]  # The most recent value
        prev_value_1 = last_days_data[target_column].values[-2] if len(last_days_data) > 1 else current_value
        prev_value_2 = last_days_data[target_column].values[-3] if len(last_days_data) > 2 else prev_value_1
        
        # extract last volume
        last_volume = last_row['Volume'].values[0]
        
        #calc moving averages
        ma5 = last_days_data[target_column].tail(5).mean()
        ma10 = last_days_data[target_column].tail(10).mean()
        
        #calc price change
        price_change = current_value - prev_value_1
        
        #forecast "steps" days
        for _ in range(steps):
            # Create a dictionary to hold feature values
            input_data = {}
            
            # Fill in feature values based on what's needed by the model
            for feature in feature_columns:
                if feature == f'{target_column}_t-1':
                    input_data[feature] = current_value
                elif feature == f'{target_column}_t-2':
                    input_data[feature] = prev_value_1
                elif feature == f'{target_column}_t-3':
                    input_data[feature] = prev_value_2
                elif feature == 'Volume_t-1':
                    input_data[feature] = last_volume
                elif feature == 'MA_5':
                    input_data[feature] = ma5
                elif feature == 'MA_10':
                    input_data[feature] = ma10
                elif feature == 'Price_Change':
                    input_data[feature] = price_change
            
            # Create input as a DataFrame with proper column names
            input_df = pd.DataFrame([input_data])
            
            #scale input data
            scaled_input = scaler.transform(input_df)
            
            #predict next value
            pred = model.predict(pd.DataFrame(scaled_input, columns=feature_columns))[0]
            forecast.append(pred)
            
            #update prev values for next iter
            prev_value_2 = prev_value_1
            prev_value_1 = current_value
            current_value = pred
            
            #update moving averages for next iter
            ma5 = (ma5 * 5 - last_days_data[target_column].values[-5] + pred) / 5 if len(last_days_data) >= 5 else pred
            ma10 = (ma10 * 10 - last_days_data[target_column].values[-10] + pred) / 10 if len(last_days_data) >= 10 else pred
            
            #up price diff
            price_change = current_value - prev_value_1
            
        return forecast
    
    def create_forecast_dataframe(self, forecasts, last_date, target_columns=None):
        # If forecasts is a list (single model), convert to dict format
        if isinstance(forecasts, list):
            # Convert NumPy array to list if needed
            if isinstance(forecasts, np.ndarray):
                forecasts = forecasts.tolist()
            forecasts = {'Close': forecasts}
            target_columns = ['Close']
        
        if target_columns is None:
            target_columns = list(forecasts.keys())
        
        # Get the length from the first forecast
        forecast_length = len(next(iter(forecasts.values())))
        
        # Ensure last_date is a datetime object
        if isinstance(last_date, str):
            last_date = pd.to_datetime(last_date)
        
        # Generate future dates starting from the day after last_date
        forecast_dates = []
        current_date = last_date
        for i in range(forecast_length):
            # Move to next calendar day (now we start from the current date, not the day after)
            if i > 0:  # Only add days after the first prediction
                current_date = current_date + datetime.timedelta(days=1)
            # Uncomment below if you want to skip weekends for stock market forecasts
            # while current_date.weekday() >= 5:  # Skip weekend (5=Saturday, 6=Sunday)
            #     current_date = current_date + datetime.timedelta(days=1)
            forecast_dates.append(current_date)
        
        # Create dataframe with dates
        forecast_df = pd.DataFrame({'Date': forecast_dates})
        
        # Add each forecast as a column
        for target in target_columns:
            if target in forecasts:
                forecast_values = forecasts[target]
                # Convert NumPy array to list if needed
                if isinstance(forecast_values, np.ndarray):
                    forecast_values = forecast_values.tolist()
                forecast_df[f'Forecasted_{target}'] = forecast_values
        
        # Additional columns for full OHLCV structure if needed
        standard_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        for column in standard_columns:
            if column not in target_columns and f'Forecasted_{column}' not in forecast_df.columns:
                # You might add default values or leave these columns out
                pass
        
        return forecast_df
    
    def save_forecast(self, forecast_df, filepath):
        #write calc values to csv
        # params: forecast_df(DataFrame): predicted values
        #params: filepath(str): path to save csv
        
        forecast_df.to_csv(filepath, index=False)
        print(f"\nForecasted values saved to {filepath}")
        
        #preview predicted data
        print("\nPreview of forecasted data:")
        print(forecast_df.head())
