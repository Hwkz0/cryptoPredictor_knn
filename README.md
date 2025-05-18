# KNN Crypto Predictor

ML app that predicts crypto prices using KNN (K-Nearest Neighbors) regression algorithm.

# Images

![Application Interface](images/image.png)
*Application interface*

## Functionality

Python based tool that used historical data to forecast price movements. This uses the KNN regression algorithm. Can generate predictions for multiple values (Close, Open, High, Low).

## Features

- **Data processing**: Automatically cleans and sorts data
- **Multi-prediction**: Predict Close, Open, High, and Low prices
- **Hyperparameter optimization**: Finds the optimal K value for KNN models
- **Multiple forecasting**: Predict prices for user-defined future periods (up to 24 days!)
- **Parallel processing**: Multithreading support for faster model evaluation
- **Visualization**: Plots performance and price predictions
- **Interface**: GUI and command-line interfaces available

## Installation

### Option 1

    Download Crypto_Predictor EXE.exe file and run on your machine, select crypto file, train model, forecast prices.

### Option 2
1. Clone the repository:
   ```
   git clone https://github.com/Hwkz0/cryptoPredictor_knn
   cd cryptoPredictor_knn
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Mode

To run the application in console mode:

```
python main.py --console
```

## Project Structure

```
knncryptob/
│
├── main.py                           # Entry point
├── Output files/                     # Visualizations
├── Crypto_currency.csv               # Dataset
│
└── cryptopredictor/                  # Main package
    ├── data/                         # Data preprocessing
    ├── features/                     # Feature processing
    ├── model/                        # KNN model implementation
    ├── evaluator/                    # Model evaluation  
    ├── forecaster/                   # Future price prediction
    ├── visualization/                # Plot visualization
    └── ui/                           # GUI files
```

## Plots and data
*Price forecast*
![Price forecast](output/price_forecast.png)

*Correlation Matrix*
![Correlation Matrix](output/correlation_matrix.png)

*Actual v predicted Low*
![Actual v predicted Low](output/actual_vs_predicted_Low.png)

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computations
- scikit-learn: Machine learning algorithms
- matplotlib/seaborn: Data visualization
- tkinter: GUI framework

## Output

"Output files" directory:

- RMSE vs. K plots for model optimization
- Actual vs. Predicted price visualizations
- Price forecast charts
- CSV file with detailed price forecasts

## License

This project is licensed under the MIT License - see the LICENSE file for details.
