import os
import threading
import pandas as pd
import tkinter as tk

class StateManager:
    """Manages shared state and data between GUI components."""
    
    def __init__(self):
        """Initialize the state manager with default values."""
        # Input parameters
        self.data_file_path = tk.StringVar()
        self.output_dir = tk.StringVar(value="output")
        self.use_threading = tk.BooleanVar(value=True)
        self.forecast_days = tk.IntVar(value=7)
        self.k_min = tk.IntVar(value=1)
        self.k_max = tk.IntVar(value=20)
        
        # Forecast attribute selection variables
        self.forecast_attributes = {
            'Close': tk.BooleanVar(value=True),
            'Open': tk.BooleanVar(value=False),
            'High': tk.BooleanVar(value=False),
            'Low': tk.BooleanVar(value=False)
        }
        
        # Selected target columns for forecast
        self.selected_target_columns = ['Close']
        
        # Data containers
        self.data = None
        self.processed_data = None
        self.data_loader = None
        
        # Model containers
        self.model = None
        self.feature_processor = None
        self.optimal_k = None
        self.eval_results = None
        self.model_evaluator = None
        self.k_range = None
        self.trained_models = {}  # Dictionary to store multiple models for different targets
        
        # Test data
        self.X_train = None
        self.X_test = None 
        self.y_train = None
        self.y_test = None
        
        # Forecast data
        self.future_forecast = None   # For backward compatibility
        self.future_forecasts = {}    # Dictionary for multiple forecasts
        self.forecast_df = None
        
        # Threading control
        self.threads = []
    
    def reset(self):
        """Reset all state variables to their default values."""
        self.data = None
        self.processed_data = None
        self.data_loader = None
        self.model = None
        self.feature_processor = None
        self.optimal_k = None
        self.eval_results = None
        self.model_evaluator = None
        self.k_range = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.future_forecast = None
        self.forecast_df = None
        
        # Stop any running threads
        for thread in self.threads:
            if thread.is_alive():
                # Cannot actually stop threads in Python,
                # but we can clear the list
                pass
        self.threads = []
    
    def start_thread(self, target, args=()):
        """Start a new daemon thread and keep track of it."""
        thread = threading.Thread(target=target, args=args, daemon=True)
        self.threads.append(thread)
        thread.start()
        return thread
    
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        output_dir = self.output_dir.get()
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir
