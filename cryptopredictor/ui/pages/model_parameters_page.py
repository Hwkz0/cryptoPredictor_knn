import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from cryptopredictor.ui.base_page import BasePage
from cryptopredictor.data.data_loader import DataLoader
from cryptopredictor.features.feature_processor import FeatureProcessor
from cryptopredictor.evaluator.model_evaluator import ModelEvaluator
from cryptopredictor.model.knn_regressor import KNNRegressor

class ModelParametersPage(BasePage):
    
    def build(self):
        # Title and description
        self.create_title(
            "Step 2: Model Parameters",
            "Configure the KNN model parameters and load your cryptocurrency data."
        )
        
        # Main container for two-column layout
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column for data loading
        left_column = ctk.CTkFrame(main_container, fg_color="transparent")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column for model parameters
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Data info frame - Left column
        data_info_frame = ctk.CTkFrame(left_column, corner_radius=10)
        data_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crypto data icon
        data_icon = ctk.CTkLabel(
            data_info_frame,
            text="📊",  # Chart icon
            font=ctk.CTkFont(size=40)
        )
        data_icon.pack(pady=(20, 10))
        
        data_info_label = ctk.CTkLabel(
            data_info_frame,
            text="Selected Data",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        data_info_label.pack(pady=(0, 10))
        
        data_info_container = ctk.CTkFrame(data_info_frame, fg_color="#1A2C42", corner_radius=5)
        data_info_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.data_info_text = ctk.CTkLabel(
            data_info_container,
            text=f"File: {os.path.basename(self.state_manager.data_file_path.get()) if self.state_manager.data_file_path.get() else 'None'}\nStatus: Not loaded yet",
            font=ctk.CTkFont(family="Helvetica", size=14),
            justify=tk.LEFT,
            wraplength=400
        )
        self.data_info_text.pack(anchor=tk.W, padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Store references to important buttons for easier disabling/enabling
        self.load_button = ctk.CTkButton(
            data_info_frame,
            text="Load Data",
            command=self._load_data,
            width=200,
            height=40,
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        self.load_button.pack(pady=(0, 20))
        
        # Parameters frame - Right column
        params_frame = ctk.CTkFrame(right_column, corner_radius=10)
        params_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # AI/ML icon
        ml_icon = ctk.CTkLabel(
            params_frame,
            text="🧠",  # Brain icon for ML
            font=ctk.CTkFont(size=40)
        )
        ml_icon.pack(pady=(20, 10))
        
        # K parameter label
        k_label = ctk.CTkLabel(
            params_frame,
            text="KNN Model Parameters",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        k_label.pack(pady=(0, 10))
        
        # Parameter explanation in a framed box
        explanation_frame = ctk.CTkFrame(params_frame, fg_color="#1A2C42", corner_radius=5)
        explanation_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        k_explanation = ctk.CTkLabel(
            explanation_frame,
            text="K is the number of nearest neighbors used in the KNN algorithm.\n"
                 "The model will test multiple values of K to find the optimal one.\n"
                 "A smaller K is more sensitive to noise, while a larger K is smoother.",
            font=ctk.CTkFont(family="Helvetica", size=14),
            justify=tk.LEFT,
            wraplength=400
        )
        k_explanation.pack(anchor=tk.W, padx=20, pady=20)
        
        # K range settings
        k_range_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        k_range_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # K range title
        k_range_title = ctk.CTkLabel(
            k_range_frame,
            text="K Range to Test:",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        )
        k_range_title.pack(anchor=tk.W, pady=(0, 10))
        
        # K min and max inputs in a row
        k_input_row = ctk.CTkFrame(k_range_frame, fg_color="transparent")
        k_input_row.pack(fill=tk.X)
        
        from_label = ctk.CTkLabel(
            k_input_row,
            text="From K =",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        from_label.pack(side=tk.LEFT)
        
        k_min_spinner = ctk.CTkEntry(
            k_input_row,
            textvariable=self.state_manager.k_min,
            width=80,
            height=30,
            justify='center',
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        k_min_spinner.pack(side=tk.LEFT, padx=10)
        
        to_label = ctk.CTkLabel(
            k_input_row,
            text="To K =",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        to_label.pack(side=tk.LEFT, padx=(20, 0))
        
        k_max_spinner = ctk.CTkEntry(
            k_input_row,
            textvariable=self.state_manager.k_max,
            width=80,
            height=30,
            justify='center',
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        k_max_spinner.pack(side=tk.LEFT, padx=10)
        
        # Parallel processing option
        threading_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        threading_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        threading_switch = ctk.CTkSwitch(
            threading_frame,
            text="Use Parallel Processing (faster but uses more CPU)",
            variable=self.state_manager.use_threading,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        threading_switch.pack(anchor=tk.W)
        
        # Training button and loading indicator container
        train_container = ctk.CTkFrame(params_frame, fg_color="transparent")
        train_container.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # Train button
        self.train_button = ctk.CTkButton(
            train_container,
            text="Train Model",
            command=self._train_model,
            width=200,
            height=50,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        self.train_button.pack(pady=10)
        
        # Loading indicator (hidden initially)
        self.loading_frame = ctk.CTkFrame(train_container, fg_color="transparent")
        self.loading_frame.pack(fill=tk.X, pady=(0, 10))
        self.loading_frame.pack_forget()  # Hide initially
        
        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text="Training in progress...",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="#00A3FF"
        )
        self.loading_label.pack(pady=(0, 5))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.loading_frame,
            width=400,
            height=15,
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=(0, 5))
        self.progress_bar.set(0)
        
        # Navigation buttons
        self.create_navigation_buttons(
            back_page="data_selection",
            back_text="Back: Data Selection"
        )
    
    def update_content(self):
        """Update page content with current state."""
        if self.state_manager.data_file_path.get():
            self.data_info_text.configure(
                text=f"File: {os.path.basename(self.state_manager.data_file_path.get())}\nStatus: Not loaded yet"
            )
    
    def _load_data(self):
        """Load and preprocess data from selected file."""
        file_path = self.state_manager.data_file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a data file.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        try:
            self.set_status("Loading data...")
            
            # Disable buttons during data loading
            self._disable_buttons()
            
            # Create output directory if it doesn't exist
            self.state_manager.ensure_output_dir()
            
            # Load the data
            self.state_manager.data_loader = DataLoader(file_path)
            self.state_manager.data = self.state_manager.data_loader.load_data()
            
            # Show a basic summary before preprocessing
            rows = len(self.state_manager.data)
            cols = len(self.state_manager.data.columns)
            
            # Process the data
            try:
                self.state_manager.processed_data = self.state_manager.data_loader.preprocess_data()
                processed_rows = len(self.state_manager.processed_data) if self.state_manager.processed_data is not None else 0
                
                # Get data info
                data_info = self.state_manager.data_loader.get_data_info()
                
                # Update data info text
                data_info_text = (
                    f"File: {os.path.basename(file_path)}\n"
                    f"Status: Loaded successfully\n"
                    f"Original data: {rows} rows, {cols} columns\n"
                    f"After preprocessing: {processed_rows} rows\n"
                )
                
                # Add date range if available
                if hasattr(data_info, 'get') and data_info.get('date_range'):
                    data_info_text += f"Date range: {data_info['date_range']}\n"
                
                self.data_info_text.configure(text=data_info_text)
                
                messagebox.showinfo("Data Loaded", "Data loaded and preprocessed successfully!")
                self.set_status("Data loaded and preprocessed successfully.")
                
            except Exception as e:
                messagebox.showwarning(
                    "Preprocessing Warning", 
                    f"Data loaded but error during preprocessing: {str(e)}\n\n"
                    "Some features may not work correctly."
                )
                
                self.data_info_text.configure(
                    text=f"File: {os.path.basename(file_path)}\nStatus: Loaded with preprocessing warnings"
                )
                self.set_status("Data loaded with preprocessing warnings.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.set_status("Error loading data.")
        finally:
            # Re-enable buttons
            self._enable_buttons()
    
    def _train_model(self):
        if not hasattr(self.state_manager, 'data_loader') or self.state_manager.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        
        try:
            # Validate k range
            if self.state_manager.k_min.get() >= self.state_manager.k_max.get():
                messagebox.showerror("Invalid Parameters", "K min must be less than K max.")
                return
            
            # Start training in a separate thread to keep UI responsive
            self.set_status("Training models for multiple price targets... This may take a while.")
            
            # Show loading indicator
            self.loading_frame.pack(fill=tk.X, pady=(0, 10))
            self.progress_bar.start()
            
            # Disable buttons during training
            self._disable_buttons()
            
            # Start training in a separate thread
            self.state_manager.start_thread(target=self._perform_training)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to train model: {str(e)}")
            self.set_status("Error training model.")
            self._enable_buttons()
            
            # Hide loading indicator
            self.loading_frame.pack_forget()
            self.progress_bar.stop()
    
    def _perform_training(self):
        try:
            # Price attributes to train models for
            price_targets = ['Close', 'Open', 'High', 'Low']
            available_targets = []
            
            # Check which target columns are available in the data
            for target in price_targets:
                if target in self.state_manager.data.columns:
                    available_targets.append(target)
            
            if not available_targets:
                raise ValueError("No valid price target columns found in the data.")
            
            # Initialize dictionary to store trained models
            self.state_manager.trained_models = {}
            
            # Set initial reference target (default is 'Close')
            primary_target = 'Close' if 'Close' in available_targets else available_targets[0]
            
            # Train models for each available target
            for target in available_targets:
                self._post_to_main_thread(lambda t=target: self.set_status(f"Training model for {t} price target..."))
                
                # Split data for this target
                X_train, X_test, y_train, y_test, feature_columns = self.state_manager.data_loader.split_data(
                    target_column=target, 
                    test_size=0.2, 
                    random_state=42
                )
                
                # If this is the primary target, store the split data in state manager
                if target == primary_target:
                    self.state_manager.X_train = X_train
                    self.state_manager.X_test = X_test
                    self.state_manager.y_train = y_train
                    self.state_manager.y_test = y_test
                
                # Scale features
                feature_processor = FeatureProcessor()
                X_train_scaled, X_test_scaled = feature_processor.scale_features(X_train, X_test)
                
                # Train model
                k_range = list(range(self.state_manager.k_min.get(), self.state_manager.k_max.get() + 1))
                
                # Only store k_range and model_evaluator for the primary target
                if target == primary_target:
                    self.state_manager.k_range = k_range
                    self.state_manager.feature_processor = feature_processor
                
                # Create model evaluator
                model_evaluator = ModelEvaluator(X_train_scaled, y_train)
                
                if self.state_manager.use_threading.get():
                    model_evaluator.enable_threading()
                
                # Find optimal k
                optimal_k = model_evaluator.find_optimal_k(k_range)
                
                # Train final model
                model = KNNRegressor(k=optimal_k)
                model.fit(X_train_scaled, y_train)
                
                # Evaluate model
                eval_results = model_evaluator.evaluate_model(
                    model, 
                    X_test_scaled, 
                    y_test
                )
                
                # Store model, scaler, and evaluation results
                self.state_manager.trained_models[target] = {
                    'model': model,
                    'scaler': feature_processor.scaler,
                    'optimal_k': optimal_k,
                    'eval_results': eval_results,
                    'feature_columns': feature_columns
                }
                
                # If this is the primary target, also store in the main state variables
                if target == primary_target:
                    self.state_manager.model = model
                    self.state_manager.model_evaluator = model_evaluator
                    self.state_manager.optimal_k = optimal_k
                    self.state_manager.eval_results = eval_results
            
            # Navigate to results page
            self._post_to_main_thread(lambda: self.navigate_to("results"))
            
        except Exception as e:
            self._handle_training_error(str(e))
        finally:
            # Hide loading indicator
            self._post_to_main_thread(lambda: self.loading_frame.pack_forget())
            self._post_to_main_thread(lambda: self.progress_bar.stop())
            
            # Re-enable buttons
            self._post_to_main_thread(self._enable_buttons)
            self._post_to_main_thread(lambda: self.set_status("Model training completed for all available price targets."))
    
    def _post_to_main_thread(self, func):
        self.frame.after(0, func)
    
    def _disable_buttons(self):
        # Directly disable the specific buttons we need to control
        self.load_button.configure(state=tk.DISABLED)
        self.train_button.configure(state=tk.DISABLED)
        
        # Disable navigation buttons to prevent page switching during operations
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state=tk.DISABLED)
    
    def _enable_buttons(self):
        # Re-enable the specific buttons
        self.load_button.configure(state=tk.NORMAL)
        self.train_button.configure(state=tk.NORMAL)
        
        # Re-enable navigation buttons
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state=tk.NORMAL)
    
    def _handle_training_error(self, error_message):
        self._post_to_main_thread(lambda: messagebox.showerror("Training Error", error_message))
