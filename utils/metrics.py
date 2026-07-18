"""Evaluation metrics for the Brent price prediction model."""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_metrics(y_true, y_pred):
    """Return RMSE, MAE, MAPE (percent), and R² for two numeric series.

    Zero values are excluded from MAPE because percentage error is undefined for
    those observations. A clear error is raised when the supplied series cannot
    produce a meaningful set of metrics.
    """
    actual = np.asarray(y_true, dtype=float).reshape(-1)
    predicted = np.asarray(y_pred, dtype=float).reshape(-1)

    if actual.size == 0 or actual.size != predicted.size:
        raise ValueError("y_true and y_pred must have the same non-zero length.")
    if not (np.isfinite(actual).all() and np.isfinite(predicted).all()):
        raise ValueError("y_true and y_pred must contain only finite values.")
    if actual.size < 2:
        raise ValueError("At least two observations are required to calculate R².")

    non_zero_actual = actual != 0
    if not non_zero_actual.any():
        raise ValueError("MAPE cannot be calculated when all actual values are zero.")

    return {
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "mae": float(mean_absolute_error(actual, predicted)),
        "mape": float(
            np.mean(
                np.abs(
                    (actual[non_zero_actual] - predicted[non_zero_actual])
                    / actual[non_zero_actual]
                )
            )
            * 100
        ),
        "r2": float(r2_score(actual, predicted)),
    }
