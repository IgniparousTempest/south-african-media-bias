from typing import Tuple
import pandas as pd


def _auc(data: pd.DataFrame) -> float:
    area = 0.0

    dates = data.keys()
    for i, k in enumerate(dates):
        if i == 0:
            continue
        # calculate area of trapezium
        days = (k - dates[i - 1]).days  # Height
        a = data[k]
        b = data[dates[i - 1]]
        area += 0.5 * (a + b) * days
    return area


def auc(focus_data: pd.DataFrame, seats_data: pd.DataFrame) -> Tuple[float, float, float]:
    """
    Calculates the ratio of focus AUC to seats AUC, and the corresponding AUCs.
    :param focus_data:
    :param seats_data:
    :return: ratio, auc_focus, auc_seats
    """
    auc_focus = _auc(focus_data)
    auc_seats = _auc(seats_data)
    return auc_focus / auc_seats, auc_focus, auc_seats
