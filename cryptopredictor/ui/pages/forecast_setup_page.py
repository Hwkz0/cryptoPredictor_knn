import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from cryptopredictor.ui.base_page import BasePage
from cryptopredictor.forecaster.price_forecaster import PriceForecaster

class ForecastSetupPage(BasePage):
    
    def build(self):
        # Title and description
        self.create_title(
            "Step 4: Forecast Setup",
            "Configure and generate price forecasts using your trained model."
        )
        
        # Main container with columns for better layout
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column for forecast parameters
        left_column = ctk.CTkFrame(main_container, fg_color="transparent")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column for model info
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Forecast parameters frame - Left column
        forecast_frame = ctk.CTkFrame(left_column, corner_radius=10)
        forecast_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crypto forecast icon
        forecast_icon = ctk.CTkLabel(
            forecast_frame,
            text="🔮",  # Crystal ball icon
            font=ctk.CTkFont(size=40)
        )
        forecast_icon.pack(pady=(20, 0))
        
        forecast_title = ctk.CTkLabel(
            forecast_frame,
            text="Forecast Settings",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        forecast_title.pack(pady=(5, 20))
        
        # Forecast days
        days_label = ctk.CTkLabel(
            forecast_frame,
            text="Number of Days to Forecast:",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        days_label.pack(anchor=tk.W, padx=30, pady=(10, 5))
        
        days_explanation = ctk.CTkLabel(
            forecast_frame,
            text="How many days into the future do you want to predict prices?",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="gray"
        )
        days_explanation.pack(anchor=tk.W, padx=30, pady=(0, 15))
        
        # Days slider with larger height
        days_slider = ctk.CTkSlider(
            forecast_frame,
            from_=1,
            to=24,
            number_of_steps=23,
            variable=self.state_manager.forecast_days,
            height=20
        )
        days_slider.pack(fill=tk.X, padx=40, pady=(0, 10))
        
        # Display selected days value
        days_value_frame = ctk.CTkFrame(forecast_frame, fg_color="#1A2C42", corner_radius=10)
        days_value_frame.pack(fill=tk.X, padx=40, pady=(5, 20))
        
        days_value_container = ctk.CTkFrame(days_value_frame, fg_color="transparent")
        days_value_container.pack(pady=10)
        
        days_value_label = ctk.CTkLabel(
            days_value_container,
            textvariable=self.state_manager.forecast_days,
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#00A3FF"
        )
        days_value_label.pack(side=tk.LEFT)
        
        days_text = ctk.CTkLabel(
            days_value_container,
            text=" days",
            font=ctk.CTkFont(family="Helvetica", size=18)
        )
        days_text.pack(side=tk.LEFT)
        
        # Price attributes selection
        attributes_label = ctk.CTkLabel(
            forecast_frame,
            text="Price Attributes to Forecast:",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        attributes_label.pack(anchor=tk.W, padx=30, pady=(20, 5))
        
        attributes_explanation = ctk.CTkLabel(
            forecast_frame,
            text="Select which price attributes you want to forecast:",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="gray"
        )
        attributes_explanation.pack(anchor=tk.W, padx=30, pady=(0, 15))
        
        # Create checkboxes for price attributes in a container
        attributes_container = ctk.CTkFrame(forecast_frame, fg_color="#1A2C42", corner_radius=10)
        attributes_container.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Initialize dictionary for checkbox variables if not already in state manager
        if not hasattr(self.state_manager, 'forecast_attributes'):
            self.state_manager.forecast_attributes = {
                'Close': tk.BooleanVar(value=True),
                'Open': tk.BooleanVar(value=False),
                'High': tk.BooleanVar(value=False),
                'Low': tk.BooleanVar(value=False)
            }
        
        # Create attribute checkboxes
        self.attribute_checkboxes = {}
        available_attributes = ['Close', 'Open', 'High', 'Low']
        
        # Create a grid layout for attributes (2x2)
        attribute_grid = ctk.CTkFrame(attributes_container, fg_color="transparent")
        attribute_grid.pack(padx=20, pady=15)
        
        for i, attr in enumerate(available_attributes):
            var = self.state_manager.forecast_attributes.get(attr, tk.BooleanVar(value=attr=='Close'))
            self.state_manager.forecast_attributes[attr] = var  # Ensure it's in state manager
            
            checkbox = ctk.CTkCheckBox(
                attribute_grid,
                text=attr,
                variable=var,
                font=ctk.CTkFont(family="Helvetica", size=14),
                width=120,
                height=30,
                checkbox_width=22,
                checkbox_height=22
            )
            checkbox.grid(row=i//2, column=i%2, padx=15, pady=10, sticky=tk.W)
            self.attribute_checkboxes[attr] = checkbox
        
        # Model details frame - Right column
        model_info_frame = ctk.CTkFrame(right_column, corner_radius=10)
        model_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Model icon
        model_icon = ctk.CTkLabel(
            model_info_frame,
            text="📊",  # Chart icon
            font=ctk.CTkFont(size=40)
        )
        model_icon.pack(pady=(20, 0))
        
        model_info_title = ctk.CTkLabel(
            model_info_frame,
            text="Model Information",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        model_info_title.pack(pady=(5, 20))
        
        # Model details in a styled container
        model_details_container = ctk.CTkFrame(model_info_frame, fg_color="#1A2C42", corner_radius=10)
        model_details_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.model_details = ctk.CTkLabel(
            model_details_container,
            text="Model details not available",
            font=ctk.CTkFont(family="Helvetica", size=14),
            justify=tk.LEFT,
            wraplength=400
        )
        self.model_details.pack(anchor=tk.W, padx=20, pady=20)
        
        # Forecast button in a container
        generate_button_frame = ctk.CTkFrame(model_info_frame, fg_color="transparent")
        generate_button_frame.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        generate_button = ctk.CTkButton(
            generate_button_frame,
            text="Generate Forecast",
            command=self._generate_forecast,
            width=250,
            height=50,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        generate_button.pack(pady=10)
        
        # Loading indicator (hidden initially)
        self.loading_frame = ctk.CTkFrame(generate_button_frame, fg_color="transparent")
        self.loading_frame.pack(fill=tk.X, pady=(0, 10))
        self.loading_frame.pack_forget()  # Hide initially
        
        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text="Generating forecast...",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="#00A3FF"
        )
        self.loading_label.pack(pady=(0, 5))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.loading_frame,
            width=250,
            height=15,
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=(0, 5))
        self.progress_bar.set(0)
        
        # Bottom navigation with buttons to all steps
        nav_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Back button
        back_button = ctk.CTkButton(
            nav_frame,
            text="← Back: Results",
            command=lambda: self.navigate_to("results"),
            width=150,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        back_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Return to Step 1 button
        restart_button = ctk.CTkButton(
            nav_frame,
            text="Return to Step 1",
            command=lambda: self.navigate_to("data_selection"),
            width=150,
            font=ctk.CTkFont(family="Helvetica", size=14),
            fg_color="#555555",
            hover_color="#444444"
        )
        restart_button.pack(side=tk.LEFT)
    
    def update_content(self):
        """Update page content with current model information."""
        if not self.state_manager.model or not self.state_manager.eval_results:
            self.model_details.configure(
                text="Model not trained yet. Please go back and train the model first."
            )
            return
        
        model_details_text = (
            f"Algorithm: K-Nearest Neighbors (KNN)\n"
            f"Optimal K Value: {self.state_manager.optimal_k}\n"
        )
        
        if 'rmse' in self.state_manager.eval_results:
            model_details_text += f"RMSE: {self.state_manager.eval_results['rmse']:.4f}\n"
        
        if 'mae' in self.state_manager.eval_results:
            model_details_text += f"MAE: {self.state_manager.eval_results['mae']:.4f}\n"
        
        if 'r2' in self.state_manager.eval_results:
            model_details_text += f"R²: {self.state_manager.eval_results['r2']:.4f}"
        
        self.model_details.configure(text=model_details_text)
    
    def _generate_forecast(self):
        """Generate price forecast using the trained model."""
        if not self.state_manager.model:
            messagebox.showerror("Error", "Please train a model first.")
            return
        
        # Check if at least one attribute is selected
        selected_attributes = [attr for attr, var in self.state_manager.forecast_attributes.items() 
                              if var.get()]
        
        if not selected_attributes:
            messagebox.showerror("Error", "Please select at least one price attribute to forecast.")
            return
        
        # Store selected attributes in state manager
        self.state_manager.selected_target_columns = selected_attributes
        
        try:
            # Disable buttons during forecasting
            self._disable_buttons()
            
            # Show loading indicator
            self.loading_frame.pack(fill=tk.X, pady=(0, 10))
            self.progress_bar.start()
            
            self.set_status(f"Generating forecast for {', '.join(selected_attributes)}...")
            
            # Start forecasting in a separate thread
            self.state_manager.start_thread(target=self._perform_forecasting)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate forecast: {str(e)}")
            self.set_status("Error generating forecast.")
            self._enable_buttons()
            
            # Hide loading indicator
            self.loading_frame.pack_forget()
            self.progress_bar.stop()
    
    def _perform_forecasting(self):
        """Perform the forecasting in a separate thread."""
        try:
            import pandas as pd
            import os
            
            # Get forecast parameters
            forecast_days = self.state_manager.forecast_days.get()
            selected_attributes = self.state_manager.selected_target_columns
            
            # Get the last data points for forecasting
            last_date = pd.to_datetime(self.state_manager.data['Date'].values[-1])
            last_days_data = self.state_manager.data_loader.get_last_days_data()
            
            # Initialize forecaster and forecast dictionary
            forecaster = PriceForecaster()
            forecasts = {}
            
            # Generate forecasts for each selected attribute
            for target in selected_attributes:
                try:
                    # Check if we have a model for this target or use the default model
                    if hasattr(self.state_manager, 'trained_models') and target in self.state_manager.trained_models:
                        model_info = self.state_manager.trained_models[target]
                        model = model_info['model']
                        scaler = model_info['scaler']
                        feature_columns = model_info.get('feature_columns')
                    else:
                        model = self.state_manager.model
                        scaler = self.state_manager.feature_processor.scaler
                        feature_columns = None
                    
                    # Generate forecast for this target
                    forecasts[target] = forecaster.forecast(
                        model, 
                        scaler, 
                        last_days_data, 
                        forecast_days,
                        target_column=target,
                        feature_columns=feature_columns
                    )
                except Exception as e:
                    self._post_to_main_thread(lambda t=target, err=str(e): messagebox.showwarning(
                        "Forecast Warning", 
                        f"Error forecasting {t}: {err}\nSkipping this attribute."
                    ))
            
            # Create forecast DataFrame and save to CSV
            forecast_df = forecaster.create_forecast_dataframe(forecasts, last_date, selected_attributes)
            
            # Ensure output directory exists
            output_dir = self.state_manager.ensure_output_dir()
            forecast_output_path = os.path.join(output_dir, 'price_forecast.csv')
            forecaster.save_forecast(forecast_df, forecast_output_path)
            
            # Store for visualization
            self.state_manager.future_forecasts = forecasts
            self.state_manager.forecast_df = forecast_df
            
            # Navigate to forecast results page
            self._post_to_main_thread(lambda: self.navigate_to("forecast_results"))
            
        except Exception as e:
            error_message = str(e)  # Capture the error message immediately
            self._post_to_main_thread(lambda msg=error_message: messagebox.showerror("Forecasting Error", msg))
        finally:
            # Hide loading indicator
            self._post_to_main_thread(lambda: self.loading_frame.pack_forget())
            self._post_to_main_thread(lambda: self.progress_bar.stop())
            
            # Re-enable buttons
            self._post_to_main_thread(self._enable_buttons)
            self._post_to_main_thread(lambda: self.set_status("Forecast generation completed."))
    
    def _post_to_main_thread(self, func):
        """Post a function to be executed in the main thread."""
        self.frame.after(0, func)
    
    def _disable_buttons(self):
        """Disable all buttons in the UI."""
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state=tk.DISABLED)
            # Check nested frames for buttons
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        child.configure(state=tk.DISABLED)
                    # One more level
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkButton):
                                grandchild.configure(state=tk.DISABLED)
    
    def _enable_buttons(self):
        """Enable all buttons in the UI."""
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state=tk.NORMAL)
            # Check nested frames for buttons
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        child.configure(state=tk.NORMAL)
                    # One more level
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkButton):
                                grandchild.configure(state=tk.NORMAL)
