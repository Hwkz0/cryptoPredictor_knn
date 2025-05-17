import concurrent.futures
from typing import List, Callable, Any, Dict, Tuple

class ThreadingProcessor:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers

    def process_parallel(self, func: Callable, param_list: List[Dict[str, Any]]) -> List[Tuple[Any, Any]]:
        results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(func, **params): next(iter(params.values())) for params in param_list}
            
            for future in concurrent.futures.as_completed(futures):
                key = futures[future]
                try:
                    result = future.result()
                    results.append((key, result))
                    print(f"Completed for {key}")
                except Exception as e:
                    print(f"Exception for {key}: {e}")
                    results.append((key, None))
        return sorted(results, key=lambda x: x[0])

    @staticmethod
    def create_param_list(param_name: str, param_values: List[Any], fixed_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        fixed_params = fixed_params or {}
        return [{param_name: v, **fixed_params} for v in param_values]
