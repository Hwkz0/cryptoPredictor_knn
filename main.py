import os
import pandas as pd
import numpy as np
import multiprocessing
import argparse

# Import modules from cryptopredictor package
from cryptopredictor.data.data_loader import DataLoader
from cryptopredictor.features.feature_processor import FeatureProcessor
from cryptopredictor.model.knn_regressor import KNNRegressor
from cryptopredictor.evaluator.model_evaluator import ModelEvaluator
from cryptopredictor.forecaster.price_forecaster import PriceForecaster
from cryptopredictor.visualization.visualizer import Visualizer

def main(use_gui=False):
    if use_gui:
        # Import here to avoid circular imports
        from cryptopredictor.ui.app import launch_gui
        launch_gui()
        return
        
    # Create output directory if it doesn't exist
    output_dir = 'Output files'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("=== Cryptocurrency Price Prediction with KNN ===")
    
    # Load and preprocess data
    print("\nLoading and preprocessing data...")
    data_file = "Crypto_currency.csv"
    
    # Check if the file exists
    if not os.path.exists(data_file):
        print(f"Error: File {data_file} not found.")
        return
    
    data_loader = DataLoader(data_file)
    data = data_loader.load_data()
    data_loader.print_data_info()
    
    # Preprocess the data
    processed_data = data_loader.preprocess_data()
    
    # Set up model training options
    print("\nSetting up model training options...")
    
    # Ask user which price columns to predict
    available_price_columns = ['Close', 'Open', 'High', 'Low']
    
    print("\nHow would you like to predict cryptocurrency prices?")
    print("1. Predict all price values (Close, Open, High, Low)")
    print("2. Predict specific price values")
    
    prediction_choice = input("Enter your choice (1 or 2): ")
    
    if prediction_choice == '1':
        selected_targets = available_price_columns
        print(f"Selected all targets for prediction: {', '.join(selected_targets)}")
    else:
        print("\nAvailable price targets to predict:")
        for i, col in enumerate(available_price_columns):
            print(f"{i+1}. {col}")
        
        target_input = input("\nEnter the numbers of targets to predict (e.g., '1,3' for Close and High): ")
        selected_indices = [int(idx.strip())-1 for idx in target_input.split(',') if idx.strip().isdigit()]
        
        if not selected_indices:
            print("No valid targets selected. Defaulting to 'Close'")
            selected_targets = ['Close']
        else:
            selected_targets = [available_price_columns[i] for i in selected_indices if i < len(available_price_columns)]
            print(f"Selected targets for prediction: {', '.join(selected_targets)}")
    
    # Ask user if they want to use threading
    use_threading = input("Use parallel processing for model evaluation? (y/n): ").lower() == 'y'
    
    # Dictionary to store trained models and related info
    trained_models = {}
    
    # Train a model for each selected target
    for target in selected_targets:
        print(f"\n--- Training model for {target} prediction ---")
        
        # Get data for this target
        X_train, X_test, y_train, y_test, feature_columns = data_loader.split_data(target_column=target)
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        
        # Scale features
        print(f"\nScaling features for {target} model...")
        feature_processor = FeatureProcessor()
        X_train_scaled, X_test_scaled = feature_processor.scale_features(X_train, X_test)
        
        # Find optimal k and train model
        print(f"\nFinding optimal k and training the {target} model...")
        k_range = list(range(1, 21))  # Test k from 1 to 20
        
        model_evaluator = ModelEvaluator(X_train_scaled, y_train)
        
        if use_threading:
            # Determine number of workers based on CPU cores, but be conservative
            num_workers = max(4, max(1, multiprocessing.cpu_count() // 2))
            print(f"Using {num_workers} workers for parallel processing")
            model_evaluator.enable_threading(max_workers=num_workers)
        else:
            print("Using sequential processing")
            
        try:
            optimal_k = model_evaluator.find_optimal_k(k_range)
            
            # Train the final model with the optimal k
            print(f"\nTraining final {target} model with optimal k={optimal_k}...")
            model = KNNRegressor(k=optimal_k)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model performance
            print(f"\nEvaluating {target} model performance...")
            eval_results = model_evaluator.evaluate_model(model, X_test_scaled, y_test)
            
            # Store model and related info
            trained_models[target] = {
                'model': model,
                'scaler': feature_processor.scaler,
                'k': optimal_k,
                'feature_columns': feature_columns,
                'rmse_values': model_evaluator.rmse_values,
                'predictions': eval_results['predictions'],
                'y_test': y_test
            }
            
            # Visualize results
            print(f"\nVisualizing {target} results...")
            visualizer = Visualizer(output_dir)
            visualizer.plot_rmse_vs_k(k_range, model_evaluator.rmse_values, target_column=target)
            visualizer.plot_actual_vs_predicted(y_test, eval_results['predictions'], optimal_k, target_column=target)
            
        except Exception as e:
            print(f"Error during model evaluation for {target}: {str(e)}")
            print("Falling back to default k=5")
            model = KNNRegressor(k=5)
            model.fit(X_train_scaled, y_train)
            
            # Store model and related info with default k
            trained_models[target] = {
                'model': model,
                'scaler': feature_processor.scaler,
                'k': 5,
                'feature_columns': feature_columns,
                'rmse_values': model_evaluator.rmse_values if hasattr(model_evaluator, 'rmse_values') else None,
                'predictions': None,
                'y_test': y_test
            }
    
    # Forecast future prices
    print("\nForecasting future prices...")
    forecast_days = int(input("Enter number of days to forecast: "))
    
    # Get the last data points for forecasting
    last_date = pd.to_datetime(data['Date'].values[-1])
    print(f"\nLast date in the dataset: {last_date.strftime('%Y-%m-%d')}")
    last_days_data = data_loader.get_last_days_data()
    
    # Initialize and use the forecaster
    forecaster = PriceForecaster()
    forecasts = {}
    
    # Generate forecasts for each target
    for target, model_info in trained_models.items():
        print(f"\nGenerating {target} forecast...")
        forecasts[target] = forecaster.forecast(
            model_info['model'], 
            model_info['scaler'], 
            last_days_data, 
            forecast_days,
            target_column=target,
            feature_columns=model_info['feature_columns']
        )
    
    # Create forecast DataFrame and save to CSV
    forecast_df = forecaster.create_forecast_dataframe(forecasts, last_date, selected_targets)
    forecast_output_path = os.path.join(output_dir, 'price_forecast.csv')
    forecaster.save_forecast(forecast_df, forecast_output_path)
    
    # Display first and last dates in the forecast
    print(f"\nForecast date range: {forecast_df['Date'].min().strftime('%Y-%m-%d')} to {forecast_df['Date'].max().strftime('%Y-%m-%d')}")
    
    # Visualize forecasts
    print("\nVisualizing forecasts...")
    # Convert string dates to datetime objects if needed
    if not pd.api.types.is_datetime64_any_dtype(data['Date']):
        data['Date'] = pd.to_datetime(data['Date'])
    
    forecast_dates = forecast_df['Date'].values
    visualizer.plot_forecast(data, forecasts, forecast_dates, selected_targets)
    
    print("\n=== Analysis Complete ===")
    print(f"Results and visualizations saved in {output_dir} folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cryptocurrency Price Prediction with KNN')
    parser.add_argument('--gui', action='store_true', help='Launch the graphical user interface')
    args = parser.parse_args()
    
    main(use_gui=args.gui)