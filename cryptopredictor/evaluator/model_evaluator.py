import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score

from ..model.knn_regressor import SKLearnKNN
from ..threader.threading_processor import ThreadingProcessor

class ModelEvaluator:
    def __init__(self, X_train, y_train):
        self.X_train = X_train  
        self.y_train = y_train  
        self.optimal_k = None   
        self.rmse_values = []   
        self.r2_values = []     
        self.threader = None    
        self.use_threading = False

    def enable_threading(self, max_workers=None):
        # enable parallel evaluation with optional max threads
        self.use_threading = True
        self.threader = ThreadingProcessor(max_workers=max_workers)
        return self

    def _evaluate_k(self, k):
        # cross-validate single k, return (rmse, r2)
        try:
            model = SKLearnKNN(k=k)
            rmse = -np.mean(cross_val_score(model, self.X_train, self.y_train,
                                            scoring='neg_root_mean_squared_error', cv=5))
            r2 = np.mean(cross_val_score(model, self.X_train, self.y_train,
                                        scoring='r2', cv=5))
            print(f"k={k}: RMSE={rmse:.2f}, R²={r2:.4f}")
            return rmse, r2
        except Exception as e:
            print(f"Error k={k}: {e}")
            return float('inf'), -float('inf')

    def find_optimal_k(self, k_range):
        # tune k over range, store RMSE & R2, return best k
        print("Finding optimal k...")
        self.rmse_values, self.r2_values = [], []

        if self.use_threading and self.threader:
            try:
                param_list = self.threader.create_param_list('k', k_range)
                results = self.threader.process_parallel(self._evaluate_k, param_list)
                for _, (rmse, r2) in results:
                    self.rmse_values.append(rmse)
                    self.r2_values.append(r2)
            except Exception as e:
                print(f"Threading failed: {e}, falling back to sequential.")
                self.use_threading = False
                return self.find_optimal_k(k_range)

        if not self.use_threading:
            for k in k_range:
                rmse, r2 = self._evaluate_k(k)
                self.rmse_values.append(rmse)
                self.r2_values.append(r2)

        best_idx = np.argmin(self.rmse_values)
        self.optimal_k = k_range[best_idx]
        print(f"Optimal k: {self.optimal_k} (RMSE={self.rmse_values[best_idx]:.4f}, R²={self.r2_values[best_idx]:.4f})")
        return self.optimal_k

    def evaluate_model(self, model, X_test, y_test):
        # evaluate final model, return metrics dict
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        print(f"Eval (k={self.optimal_k}): RMSE={rmse:.2f}, R²={r2:.4f}")
        return {'predictions': preds, 'rmse': rmse, 'r2': r2}
