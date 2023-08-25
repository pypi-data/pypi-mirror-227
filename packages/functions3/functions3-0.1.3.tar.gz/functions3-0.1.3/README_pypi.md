# Data Transformation Library

## Project description
3 functions that are common for transforming data used in machine learning models.

- __Transpose__ signature: transpose2d(input_matrix: list[list[float]]) -> list
- __Time Series Windowing__ signature: window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]
- __Cross-Correlation__ signature: convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray


