import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import os

class Visualizer:
    
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        #Output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_plot(self, filename, dpi=300):

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=dpi)
        print(f"Plot saved to {filepath}")
    
    def create_basic_plot(self, figsize=(10, 6), show=True):
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax
    
    def plot_rmse_vs_k(self, k_values, rmse_values, target_column='Close'):

        plt.figure(figsize=(10, 6))
        plt.plot(k_values, rmse_values, marker='o')
        plt.title(f'RMSE vs k for {target_column} Prediction')
        plt.xlabel('k value')
        plt.ylabel('RMSE')
        plt.grid(True)
        
        # Find and mark best k (lowest RMSE)
        best_k_idx = np.argmin(rmse_values)
        best_k = k_values[best_k_idx]
        best_rmse = rmse_values[best_k_idx]
        
        plt.plot(best_k, best_rmse, 'ro', markersize=12, fillstyle='none')
        plt.annotate(f'Best k={best_k}\nRMSE={best_rmse:.2f}', 
                     xy=(best_k, best_rmse),
                     xytext=(best_k+1, best_rmse), 
                     arrowprops=dict(arrowstyle='->'))
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'rmse_vs_k_{target_column}.png'))
        plt.close()
    
    def plot_actual_vs_predicted(self, y_actual, y_pred, k, target_column='Close'):
        plt.figure(figsize=(12, 6))
        plt.scatter(y_actual, y_pred, alpha=0.5)
        
        # Add perfect prediction line
        min_val = min(y_actual.min(), y_pred.min())
        max_val = max(y_actual.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect Prediction')
        
        plt.title(f'Actual vs Predicted {target_column} (k={k})')
        plt.xlabel(f'Actual {target_column}')
        plt.ylabel(f'Predicted {target_column}')
        plt.grid(True)
        plt.legend()
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'actual_vs_predicted_{target_column}.png'))
        plt.close()
    
    def plot_forecast(self, historical_data, forecasts, forecast_dates, target_columns=None):
        plt.figure(figsize=(15, 8))
        
        # If forecasts is a list (single model), convert to dict format
        if isinstance(forecasts, list):
            forecasts = {'Close': forecasts}
            if target_columns is None:
                target_columns = ['Close']
        
        if target_columns is None:
            target_columns = list(forecasts.keys())
            
        # Plot historical data for each target
        for target in target_columns:
            if target in historical_data.columns:
                plt.plot(historical_data['Date'].tail(90), 
                         historical_data[target].tail(90), 
                         label=f'Historical {target}')
        
        # Plot forecasts for each target
        for target in target_columns:
            if target in forecasts:
                plt.plot(forecast_dates, 
                         forecasts[target], 
                         linestyle='--', 
                         marker='o',
                         label=f'Forecasted {target}')
        
        plt.title('Price Forecast')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'price_forecast.png'))
        plt.close()
    
    def plot_forecast_with_details(self, historical_data, forecasts, forecast_dates, 
                                 days_to_show=30, target_columns=None,
                                 fig=None, ax=None, save_fig=True):

        # Create figure if not provided
        if fig is None or ax is None:
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        # If forecasts is a list (single model), convert to dict format
        if isinstance(forecasts, list):
            forecasts = {'Close': forecasts}
            if target_columns is None:
                target_columns = ['Close']
        
        if target_columns is None:
            target_columns = list(forecasts.keys())
        
        # Convert dates to datetime for consistency
        if 'Date' in historical_data.columns:
            historical_dates = pd.to_datetime(historical_data['Date'].values[-days_to_show:])
        else:
            # Create date range if dates not available
            end_date = forecast_dates[0]
            start_date = end_date - pd.Timedelta(days=days_to_show)
            historical_dates = pd.date_range(start=start_date, end=end_date, periods=days_to_show)
        
        # Ensure forecast dates are datetime
        if not isinstance(forecast_dates[0], (pd.Timestamp, datetime.datetime)):
            forecast_dates = pd.to_datetime(forecast_dates)
        
        # Define colors for different targets
        historical_colors = {
            'Close': '#1f77b4',  # Blue
            'Open': '#2ca02c',   # Green
            'High': '#ff7f0e',   # Orange
            'Low': '#d62728'     # Red
        }
        
        forecast_colors = {
            'Close': '#ff5733',  # Bright Orange
            'Open': '#33ff57',   # Bright Green
            'High': '#3357ff',   # Bright Blue
            'Low': '#ff33f5'     # Bright Pink
        }
        
        # Track min and max values for y-axis limits
        all_values = []
        
        # Plot historical data for each target
        for target in target_columns:
            if target in historical_data.columns:
                historical_prices = historical_data[target].values[-days_to_show:]
                all_values.extend(historical_prices)
                
                ax.plot(historical_dates, historical_prices, 
                       label=f'Historical {target}', 
                       color=historical_colors.get(target, '#1f77b4'), 
                       linewidth=2.5, 
                       alpha=0.8)
        
        # Plot forecasts for each target
        for target in target_columns:
            if target in forecasts:
                forecast_values = forecasts[target]
                all_values.extend(forecast_values)
                
                # Plot main forecast line
                ax.plot(forecast_dates, forecast_values, 
                       label=f'Forecast {target}', 
                       color=forecast_colors.get(target, '#ff5733'), 
                       linewidth=2.5, 
                       linestyle='-')
                
                # Add markers
                ax.plot(forecast_dates[0], forecast_values[0], 'o', 
                       color=forecast_colors.get(target, '#ff5733'), markersize=8, 
                       markeredgewidth=2, markeredgecolor='white')
                ax.plot(forecast_dates[-1], forecast_values[-1], 'o', 
                       color=forecast_colors.get(target, '#ff5733'), markersize=8, 
                       markeredgewidth=2, markeredgecolor='white')
        
        # Calculate buffer for y-axis limits
        if all_values:
            min_price = min(all_values)
            max_price = max(all_values)
            buffer = (max_price - min_price) * 0.1  # 10% buffer
            
            # Set y-axis limits with buffer
            ax.set_ylim(min_price - buffer, max_price + buffer)
        
        # Shade forecast region
        ax.axvspan(forecast_dates[0], forecast_dates[-1], alpha=0.15, color='gray')
        ax.axvline(x=forecast_dates[0], color='gray', linestyle='--', alpha=0.5)
        
        # Add labels
        ax.set_title('Price Forecast', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Format y-axis with dollar signs
        from matplotlib.ticker import FuncFormatter
        def currency_formatter(x, pos):
            return f'${x:,.2f}'
        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        
        # Add legend
        ax.legend(loc='upper left', fontsize=11, frameon=True, framealpha=0.9)
        
        # Format x-axis dates
        fig.autofmt_xdate()
        
        # Tight layout
        plt.tight_layout()
        
        # Save the figure if requested
        if save_fig:
            self.save_plot('price_forecast_detailed.png')
        
        return fig, ax
