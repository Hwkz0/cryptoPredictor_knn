import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from cryptopredictor.ui.base_page import BasePage
from cryptopredictor.visualization.visualizer import Visualizer
import os

class ResultsPage(BasePage):

    def build(self):
        # Title and description
        self.create_title(
            "Step 3: Model Results",
            "Review the performance metrics and visualization of your trained model."
        )
        
        # Main container with columns
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column for metrics
        left_column = ctk.CTkFrame(main_container, fg_color="transparent", width=400)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_column.pack_propagate(False)  # Prevent column from shrinking
        
        # Right column for visualizations
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Add prominent forecast button at the top
        forecast_button_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        forecast_button_frame.pack(fill=tk.X, pady=(0, 20))
        
        forecast_action_button = ctk.CTkButton(
            forecast_button_frame,
            text="PROCEED TO PRICE FORECASTING",
            command=lambda: self.navigate_to("forecast_setup"),
            width=380,
            height=60,
            fg_color="#00A3FF",  # Match app theme
            hover_color="#0077CC",  # Darker blue on hover
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        forecast_action_button.pack()
        
        # Results frame
        results_frame = ctk.CTkFrame(left_column, corner_radius=15)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add model performance metrics
        metrics_title = ctk.CTkLabel(
            results_frame,
            text="Model Performance Metrics",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        metrics_title.pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        # Store metric elements for updating
        self.metrics_elements = {}
        
        # Metrics container
        metrics_container = ctk.CTkFrame(results_frame, fg_color="#1A1A1A", corner_radius=10)
        metrics_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Optimal K with icon
        k_frame = ctk.CTkFrame(metrics_container, fg_color="transparent")
        k_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        k_icon = ctk.CTkLabel(
            k_frame,
            text="🔑",  # Key icon
            font=ctk.CTkFont(size=18)
        )
        k_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        k_label = ctk.CTkLabel(
            k_frame,
            text="Optimal K Value:",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        k_label.pack(side=tk.LEFT)
        
        self.metrics_elements['k_value'] = ctk.CTkLabel(
            k_frame,
            text="N/A",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color="#00A3FF"
        )
        self.metrics_elements['k_value'].pack(side=tk.LEFT, padx=(10, 0))
        
        # RMSE with explanation
        rmse_frame = ctk.CTkFrame(metrics_container, fg_color="transparent")
        rmse_frame.pack(fill=tk.X, padx=15, pady=10)
        
        rmse_icon = ctk.CTkLabel(
            rmse_frame,
            text="📉",  # Chart icon
            font=ctk.CTkFont(size=18)
        )
        rmse_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        rmse_label = ctk.CTkLabel(
            rmse_frame,
            text="RMSE:",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        rmse_label.pack(side=tk.LEFT)
        
        self.metrics_elements['rmse_value'] = ctk.CTkLabel(
            rmse_frame,
            text="N/A",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color="#00A3FF"
        )
        self.metrics_elements['rmse_value'].pack(side=tk.LEFT, padx=(10, 0))
        
        rmse_explanation = ctk.CTkLabel(
            metrics_container,
            text="RMSE measures the average magnitude of prediction errors. Lower values indicate better accuracy.",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="gray",
            wraplength=350
        )
        rmse_explanation.pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        # R² with explanation
        r2_frame = ctk.CTkFrame(metrics_container, fg_color="transparent")
        r2_frame.pack(fill=tk.X, padx=15, pady=10)
        
        r2_icon = ctk.CTkLabel(
            r2_frame,
            text="📊",  # Bar chart icon
            font=ctk.CTkFont(size=18)
        )
        r2_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        r2_label = ctk.CTkLabel(
            r2_frame,
            text="R² Score:",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        r2_label.pack(side=tk.LEFT)
        
        self.metrics_elements['r2_value'] = ctk.CTkLabel(
            r2_frame,
            text="N/A",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color="#00A3FF"
        )
        self.metrics_elements['r2_value'].pack(side=tk.LEFT, padx=(10, 0))
        
        r2_explanation = ctk.CTkLabel(
            metrics_container,
            text="R² indicates how well the model explains the variance in the data. Values close to 1 are better.",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="gray",
            wraplength=350
        )
        r2_explanation.pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        # After the prominent forecast button, add a trained models summary section
        trained_models_frame = ctk.CTkFrame(left_column, corner_radius=15)
        trained_models_frame.pack(fill=tk.X, pady=10)
        
        trained_models_title = ctk.CTkLabel(
            trained_models_frame,
            text="Trained Models Summary",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        trained_models_title.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        self.trained_models_text = ctk.CTkLabel(
            trained_models_frame,
            text="No models have been trained yet.",
            font=ctk.CTkFont(family="Helvetica", size=12),
            justify=tk.LEFT,
            wraplength=350
        )
        self.trained_models_text.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Create plotting section in right column
        plots_title = ctk.CTkLabel(
            right_column,
            text="Performance Visualizations",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="#00A3FF"
        )
        plots_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Add vizualization explanation
        viz_explanation = ctk.CTkLabel(
            right_column,
            text="These visualizations show your model's performance. The top chart displays RMSE scores for different K values, with the optimal K highlighted. The bottom chart compares actual vs predicted values.",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="gray",
            wraplength=600,
            justify=tk.LEFT
        )
        viz_explanation.pack(anchor=tk.W, pady=(0, 10))
        
        # RMSE vs. K plot - make it smaller
        self.rmse_plot_frame = ctk.CTkFrame(right_column, corner_radius=15)
        self.rmse_plot_frame.pack(fill=tk.X, pady=(0, 10), ipady=10)
        
        rmse_plot_title = ctk.CTkLabel(
            self.rmse_plot_frame,
            text="RMSE vs. K Values",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        rmse_plot_title.pack(pady=(15, 0))
        
        # Actual vs. Predicted plot - make it larger
        self.pred_plot_frame = ctk.CTkFrame(right_column, corner_radius=15)
        self.pred_plot_frame.pack(fill=tk.BOTH, expand=True, ipady=10)
        
        pred_plot_title = ctk.CTkLabel(
            self.pred_plot_frame,
            text="Actual vs. Predicted Values",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        pred_plot_title.pack(pady=(15, 0))
        
        # Initialize visualizer
        self.visualizer = Visualizer(output_dir=os.path.join(os.getcwd(), "Output files"))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        back_button = ctk.CTkButton(
            nav_frame,
            text="← Back: Model Parameters",
            command=lambda: self.navigate_to("model_parameters"),
            width=200,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        back_button.pack(side=tk.LEFT)
        
        next_button = ctk.CTkButton(
            nav_frame,
            text="Next: Generate Forecast →",
            command=lambda: self.navigate_to("forecast_setup"),
            width=200,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        next_button.pack(side=tk.RIGHT)
    
    def update_content(self):
        if not self.state_manager.eval_results:
            return
        
        # Update metrics for the primary model (usually Close price)
        self.metrics_elements['k_value'].configure(text=f"{self.state_manager.optimal_k}")
        
        if 'rmse' in self.state_manager.eval_results:
            self.metrics_elements['rmse_value'].configure(
                text=f"{self.state_manager.eval_results['rmse']:.4f}"
            )
        
        if 'r2' in self.state_manager.eval_results:
            self.metrics_elements['r2_value'].configure(
                text=f"{self.state_manager.eval_results['r2']:.4f}"
            )
        
        # Update trained models summary
        if hasattr(self.state_manager, 'trained_models') and self.state_manager.trained_models:
            summary_text = "The following price attributes have been modeled:\n\n"
            
            for target, model_info in self.state_manager.trained_models.items():
                optimal_k = model_info.get('optimal_k', 'N/A')
                eval_results = model_info.get('eval_results', {})
                
                rmse = eval_results.get('rmse', 'N/A')
                if isinstance(rmse, (int, float)):
                    rmse = f"{rmse:.4f}"
                
                r2 = eval_results.get('r2', 'N/A')
                if isinstance(r2, (int, float)):
                    r2 = f"{r2:.4f}"
                    
                summary_text += f"• {target} Price: k={optimal_k}, RMSE={rmse}, R²={r2}\n"
            
            self.trained_models_text.configure(text=summary_text)
        
        # Update plots using the visualizer
        self._create_rmse_vs_k_plot()
        self._create_actual_vs_predicted_plot()
    
    def _create_rmse_vs_k_plot(self):
        if not hasattr(self.state_manager, 'model_evaluator') or not self.state_manager.model_evaluator:
            return
        
        # Clear any existing widgets
        for widget in self.rmse_plot_frame.winfo_children():
            if widget.winfo_class() != "CTkLabel":  # Keep the title
                widget.destroy()
        
        try:
            # Create frame for the plot
            canvas_frame = ctk.CTkFrame(self.rmse_plot_frame, fg_color="transparent")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Create figure with app theme
            plt.close('all')
            fig = plt.figure(figsize=(8, 3.5), dpi=100, facecolor='#2B2B2B')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2B2B2B')
            
            # Plot RMSE vs K
            ax.plot(self.state_manager.k_range, self.state_manager.model_evaluator.rmse_values, 
                   marker='o', color='#00A3FF', linewidth=2, markersize=8)
            
            # Find and mark the best K
            best_k_idx = self.state_manager.model_evaluator.rmse_values.index(min(self.state_manager.model_evaluator.rmse_values))
            best_k = self.state_manager.k_range[best_k_idx]
            best_rmse = self.state_manager.model_evaluator.rmse_values[best_k_idx]
            
            # Mark the best K
            ax.plot(best_k, best_rmse, 'ro', markersize=12, fillstyle='none')
            ax.annotate(f'Best k={best_k}\nRMSE={best_rmse:.4f}', 
                       xy=(best_k, best_rmse),
                       xytext=(best_k+1, best_rmse), 
                       arrowprops=dict(arrowstyle='->'),
                       color='white')
            
            # Customize the plot
            ax.set_xlabel('K Value', color='white', fontsize=12)
            ax.set_ylabel('RMSE', color='white', fontsize=12)
            ax.tick_params(colors='white')
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Set spines color
            for spine in ax.spines.values():
                spine.set_color('#555555')
            
            plt.tight_layout()
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.rmse_plot_frame,
                text=f"Could not create plot.\nError: {str(e)}",
                text_color="red"
            )
            error_label.pack(padx=20, pady=30)
    
    def _create_actual_vs_predicted_plot(self):
        if not self.state_manager.eval_results or 'predictions' not in self.state_manager.eval_results:
            return
        
        # Clear any existing widgets
        for widget in self.pred_plot_frame.winfo_children():
            if widget.winfo_class() != "CTkLabel":  # Keep the title
                widget.destroy()
        
        try:
            # Create frame for the plot
            canvas_frame = ctk.CTkFrame(self.pred_plot_frame, fg_color="transparent")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Use visualizer to create the plot
            plt.close('all')
            fig = plt.figure(figsize=(8, 5), dpi=100, facecolor='#2B2B2B')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2B2B2B')
            
            # Scatter plot of actual vs predicted
            ax.scatter(self.state_manager.y_test, self.state_manager.eval_results['predictions'], 
                      alpha=0.7, color='#00A3FF', s=50)
            
            # Add perfect prediction line
            min_val = min(self.state_manager.y_test.min(), min(self.state_manager.eval_results['predictions']))
            max_val = max(self.state_manager.y_test.max(), max(self.state_manager.eval_results['predictions']))
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
            
            # Customize the plot
            ax.set_xlabel('Actual Values', color='white', fontsize=12)
            ax.set_ylabel('Predicted Values', color='white', fontsize=12)
            ax.set_title(f'Actual vs Predicted (k={self.state_manager.optimal_k})', color='white', fontsize=14)
            ax.tick_params(colors='white')
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.legend(facecolor='#2B2B2B', edgecolor='#555555', labelcolor='white')
            
            # Set spines color
            for spine in ax.spines.values():
                spine.set_color('#555555')
            
            plt.tight_layout()
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.pred_plot_frame,
                text=f"Could not create plot.\nError: {str(e)}",
                text_color="red"
            )
            error_label.pack(padx=20, pady=30)
