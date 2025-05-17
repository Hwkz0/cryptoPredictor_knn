import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from cryptopredictor.ui.base_page import BasePage
from cryptopredictor.visualization.visualizer import Visualizer

class ForecastResultsPage(BasePage):
    
    def build(self):
        # Title and description
        self.create_title(
            "Step 5: Forecast Results",
            "View and interpret the generated price forecast."
        )
        
        # Header with navigation and buttons
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Back button
        back_to_settings_button = ctk.CTkButton(
            header_frame,
            text="⬅ Back to Forecast Settings",
            command=lambda: self.navigate_to("forecast_setup"),
            width=200,
            height=30,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        back_to_settings_button.pack(side=tk.LEFT)
        
        # Removed "Return to Step 1" button
        
        # Main content
        content_frame = ctk.CTkFrame(self.frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left and right columns
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=320)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0), pady=10)
        right_frame.pack_propagate(False)  # Prevent column from shrinking
        
        # Left column: Chart with crypto-themed header
        self.chart_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Modern header with icon and title in a row
        chart_header_frame = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
        chart_header_frame.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        chart_icon = ctk.CTkLabel(
            chart_header_frame,
            text="📈",  # Chart up icon
            font=ctk.CTkFont(size=30)
        )
        chart_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        chart_title_frame = ctk.CTkFrame(chart_header_frame, fg_color="transparent")
        chart_title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        chart_title = ctk.CTkLabel(
            chart_title_frame,
            text="Price Forecast Visualization",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        chart_title.pack(anchor=tk.W, pady=(0, 0))
        
        chart_subtitle = ctk.CTkLabel(
            chart_title_frame,
            text="Historical data and future price predictions",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="gray"
        )
        chart_subtitle.pack(anchor=tk.W, pady=(0, 5))
        
        # Right column: Forecast info and table in modern crypto style
        # Info card with crypto theme
        info_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Modern header with icon
        info_header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        info_icon = ctk.CTkLabel(
            info_header_frame,
            text="🔍",  # Magnifying glass icon
            font=ctk.CTkFont(size=24)
        )
        info_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        info_title = ctk.CTkLabel(
            info_header_frame,
            text="Forecast Details",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#00A3FF"
        )
        info_title.pack(side=tk.LEFT)
        
        # Details in a styled container
        info_container = ctk.CTkFrame(info_frame, fg_color="#1A2C42", corner_radius=10)
        info_container.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        self.info_text = ctk.CTkLabel(
            info_container,
            text="Forecast data not available",
            font=ctk.CTkFont(family="Helvetica", size=12),
            justify=tk.LEFT,
            wraplength=280
        )
        self.info_text.pack(anchor=tk.W, padx=15, pady=15)
        
        # Table Frame with crypto theme
        table_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern header with icon
        table_header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        table_icon = ctk.CTkLabel(
            table_header_frame,
            text="💰",  # Money bag icon
            font=ctk.CTkFont(size=24)
        )
        table_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        table_title = ctk.CTkLabel(
            table_header_frame,
            text="Predicted Prices",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#00A3FF"
        )
        table_title.pack(side=tk.LEFT)
        
        # Scrollable frame for the table with crypto theme
        self.table_scroll = ctk.CTkScrollableFrame(table_frame, width=300, height=400, fg_color="#1A2C42")
        self.table_scroll.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Save buttons frame with crypto theme
        save_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        save_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Modern header with icon
        save_header_frame = ctk.CTkFrame(save_frame, fg_color="transparent")
        save_header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        save_icon = ctk.CTkLabel(
            save_header_frame,
            text="💾",  # Save icon
            font=ctk.CTkFont(size=24)
        )
        save_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        save_title = ctk.CTkLabel(
            save_header_frame,
            text="Export Options",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#00A3FF"
        )
        save_title.pack(side=tk.LEFT)
        
        # Save buttons container
        save_buttons_container = ctk.CTkFrame(save_frame, fg_color="#1A2C42", corner_radius=10)
        save_buttons_container.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        save_buttons_frame = ctk.CTkFrame(save_buttons_container, fg_color="transparent")
        save_buttons_frame.pack(padx=15, pady=15)
        
        save_csv_button = ctk.CTkButton(
            save_buttons_frame,
            text="Save CSV",
            command=self._show_saved_csv_location,
            font=ctk.CTkFont(family="Helvetica", size=12),
            width=120,
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        save_csv_button.pack(side=tk.LEFT, padx=(0, 10))
        
        save_image_button = ctk.CTkButton(
            save_buttons_frame,
            text="Save Chart",
            command=self._save_forecast_image,
            font=ctk.CTkFont(family="Helvetica", size=12),
            width=120,
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        save_image_button.pack(side=tk.LEFT)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        back_button = ctk.CTkButton(
            nav_frame,
            text="← Back to Setup",
            command=lambda: self.navigate_to("forecast_setup"),
            width=150,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        back_button.pack(side=tk.LEFT)
        
        new_analysis_button = ctk.CTkButton(
            nav_frame,
            text="Start New Analysis",
            command=lambda: self.navigate_to("data_selection"),
            width=200,
            font=ctk.CTkFont(family="Helvetica", size=14),
            fg_color="#00A3FF",
            hover_color="#0077CC"
        )
        new_analysis_button.pack(side=tk.RIGHT)
        
        # Initialize visualizer
        self.visualizer = Visualizer(output_dir=os.path.join(os.getcwd(), "Output files"))
    
    def update_content(self):
        if not hasattr(self.state_manager, 'forecast_df') or self.state_manager.forecast_df is None:
            return
        
        # Update forecast info
        self._update_forecast_info()
        
        # Visualization
        self._create_forecast_visualization()
        
        # Price table
        self._create_price_table()
    
    def _update_forecast_info(self):
        if 'Date' in self.state_manager.forecast_df.columns:
            start_date = pd.to_datetime(self.state_manager.forecast_df['Date'].iloc[0]).strftime('%Y-%m-%d')
            end_date = pd.to_datetime(self.state_manager.forecast_df['Date'].iloc[-1]).strftime('%Y-%m-%d')
        else:
            start_date = "Start"
            end_date = "End"
        
        selected_targets = getattr(self.state_manager, 'selected_target_columns', ['Close'])
        
        info_text = (
            f"Period: {self.state_manager.forecast_days.get()} days\n"
            f"From: {start_date}\n"
            f"To: {end_date}\n"
            f"Attributes: {', '.join(selected_targets)}\n\n"
            f"Forecasted using KNN with k={self.state_manager.optimal_k}\n"
        )
        
        self.info_text.configure(text=info_text)
    
    def _create_forecast_visualization(self):
        """Create forecast visualization using the visualizer."""
        # Clear existing content
        for widget in self.chart_frame.winfo_children():
            if widget.winfo_class() not in ["CTkLabel", "CTkFrame"]:  # Keep the header
                widget.destroy()
        
        try:
            # Clear any existing matplotlib figures
            plt.close('all')
            
            # Get data for visualization
            days_to_show = 30
            selected_targets = getattr(self.state_manager, 'selected_target_columns', ['Close'])
            forecasts = getattr(self.state_manager, 'future_forecasts', {})
            
            # If forecasts is a single list, convert to dict format for consistent handling
            if isinstance(forecasts, list):
                forecasts = {'Close': forecasts}
            
            # Ensure forecast dates are datetime objects
            forecast_dates = pd.to_datetime(self.state_manager.forecast_df['Date'].values)
            
            # Create a figure for embedding in the GUI
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100, facecolor='#2B2B2B')
            ax.set_facecolor('#2B2B2B')
            
            # Create the visualization using the Visualizer class
            fig, ax = self.visualizer.plot_forecast_with_details(
                historical_data=self.state_manager.data,
                forecasts=forecasts,
                forecast_dates=forecast_dates,
                days_to_show=days_to_show,
                target_columns=selected_targets,
                fig=fig,
                ax=ax,
                save_fig=False  # Don't save automatically
            )
            
            # Set spines color
            for spine in ax.spines.values():
                spine.set_color('#555555')
                
            # Customize other plot elements for dark theme
            ax.tick_params(colors='white')
            ax.set_title(ax.get_title(), color='white', fontsize=14)
            ax.set_xlabel(ax.get_xlabel(), color='white', fontsize=12)
            ax.set_ylabel(ax.get_ylabel(), color='white', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Update legend if it exists
            legend = ax.get_legend()
            if legend:
                # Check if the legend has the required attributes before setting them
                # This fixes the "legend object has no attribute set_facecolor" error
                if hasattr(legend, 'set_facecolor'):
                    legend.set_facecolor('#2B2B2B')
                if hasattr(legend, 'set_edgecolor'):
                    legend.set_edgecolor('#555555')
                # Set text color for all legend text elements
                for text in legend.get_texts():
                    text.set_color('white')
            
            plt.tight_layout()
            
            # Embed in the GUI
            canvas_frame = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame,
                text=f"Could not create forecast visualization.\nError: {str(e)}",
                text_color="red"
            )
            error_label.pack(padx=10, pady=30)
    
    def _create_price_table(self):
        """Create the table of predicted prices."""
        # Clear existing content
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Get selected targets and forecasts
        selected_targets = getattr(self.state_manager, 'selected_target_columns', ['Close'])
        
        # Create headers
        header_frame = ctk.CTkFrame(self.table_scroll, fg_color="#2A3C52", corner_radius=5)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Date header on left
        date_header = ctk.CTkLabel(
            header_frame,
            text="Date",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold")
        )
        date_header.pack(side=tk.LEFT, padx=(10, 0), pady=8)
        
        # Create a frame for price headers
        price_headers_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        price_headers_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=8)
        
        # Create header for each selected target
        for i, target in enumerate(selected_targets):
            target_header = ctk.CTkLabel(
                price_headers_frame,
                text=f"{target}",
                font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
                text_color="#00A3FF"
            )
            target_header.grid(row=0, column=i, padx=(15, 0))
        
        # Add data rows with alternating colors for better readability
        for idx, row in self.state_manager.forecast_df.iterrows():
            try:
                # Set alternating row colors for better readability
                row_color = "#1A2C42" if idx % 2 == 0 else "#1E324A"
                
                row_frame = ctk.CTkFrame(self.table_scroll, fg_color=row_color, corner_radius=5)
                row_frame.pack(fill=tk.X, pady=2)
                
                # Date cell
                if 'Date' in self.state_manager.forecast_df.columns:
                    date_val = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
                else:
                    date_val = f"Day {idx+1}"
                
                date_label = ctk.CTkLabel(
                    row_frame,
                    text=date_val,
                    font=ctk.CTkFont(family="Helvetica", size=12)
                )
                date_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
                
                # Create a frame for price values
                price_values_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                price_values_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=5)
                
                # Add price for each target
                for i, target in enumerate(selected_targets):
                    forecast_col = f'Forecasted_{target}'
                    if forecast_col in self.state_manager.forecast_df.columns:
                        price_val = f"${row[forecast_col]:.2f}"
                    else:
                        forecasts = getattr(self.state_manager, 'future_forecasts', {})
                        if target in forecasts and idx < len(forecasts[target]):
                            price_val = f"${forecasts[target][idx]:.2f}"
                        else:
                            price_val = "N/A"
                    
                    price_label = ctk.CTkLabel(
                        price_values_frame,
                        text=price_val,
                        font=ctk.CTkFont(family="Helvetica", size=12)
                    )
                    price_label.grid(row=0, column=i, padx=(15, 0))
                
            except Exception as e:
                # In case of error, show a placeholder row
                error_row_frame = ctk.CTkFrame(self.table_scroll, fg_color="#3A2C42")
                error_row_frame.pack(fill=tk.X, pady=2)
                
                error_label = ctk.CTkLabel(
                    error_row_frame,
                    text="Error loading data",
                    font=ctk.CTkFont(family="Helvetica", size=12),
                    text_color="red"
                )
                error_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
    
    def _show_saved_csv_location(self):
        """Show the location of the saved CSV file."""
        # Get the directory where CSV files are saved
        csv_dir = os.path.join(os.getcwd(), "Output files")
        
        # If the directory exists and is accessible, show its contents
        if os.path.exists(csv_dir) and os.path.isdir(csv_dir):
            # List CSV files in the directory
            csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
            
            if csv_files:
                # Create a message with the list of CSV files
                csv_files_list = "\n".join(csv_files)
                message = f"Saved CSV files:\n{csv_files_list}"
            else:
                message = "No CSV files found in the directory."
        else:
            message = "CSV directory does not exist or is not accessible."
        
        # Show the message in a dialog
        messagebox.showinfo("Saved CSV Location", message)
    
    def _save_forecast_image(self):
        """Save the forecast visualization as an image file."""
        # Ask user for file location and name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")],
            title="Save Forecast Image"
        )
        
        if not file_path:
            return  # User cancelled the save dialog
        
        try:
            # Get data for visualization
            days_to_show = 30
            selected_targets = getattr(self.state_manager, 'selected_target_columns', ['Close'])
            forecasts = getattr(self.state_manager, 'future_forecasts', {})
            
            # Create a high-resolution figure for saving
            fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
            
            # Ensure forecast dates are datetime objects
            forecast_dates = pd.to_datetime(self.state_manager.forecast_df['Date'].values)
            
            # Generate the visualization
            self.visualizer.plot_forecast_with_details(
                historical_data=self.state_manager.data,
                forecasts=forecasts,
                forecast_dates=forecast_dates,
                days_to_show=days_to_show,
                target_columns=selected_targets,
                fig=fig,
                ax=ax,
                save_fig=False
            )
            
            # Save the figure manually
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            # Confirmation message
            messagebox.showinfo("Save Chart Image", f"Chart image saved as:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Save Chart Image", f"Error saving image: {str(e)}")
