import logging
from typing import Callable, Dict, List, Union

import numpy as np
from exodusutils.internal import mean_per_class_error, sanitize_pred_and_actual
from pydantic import BaseModel, validator
from pydantic.types import NonNegativeFloat
from sklearn.metrics import (accuracy_score, log_loss, mean_squared_error,
                             roc_auc_score)
from sklearn.preprocessing import LabelEncoder

METRIC_DECIMAL = 5


class RegressionScores(BaseModel):
    """
    The regression scores set.

    Metrics include:
        - mean squared error (`mse`)
        - root mean square error (`rmse`)
        - root mean square logarithmic error (`rmsle`)
        - mean absolute error (`mae`)
        - r squared (`r2`)
        - deviance (`deviance`)
        - mean absolute percentage error (`mape`)
        - weighted mean absolute percentage error (`wmape`)
    """

    mse: float
    rmse: float
    rmsle: float
    mae: float
    r2: float
    deviance: float
    mape: float
    wmape: float

    @validator("mse", "rmse", "rmsle", "mae", "deviance", "mape", "wmape")
    def check_nonnegative_or_nan(cls, v):
        if not np.isnan(v) and v < 0:
            raise ValueError(
                f"Invalid score: required nan or non-negative float, got {v}"
            )
        return v

    @classmethod
    def get_scores(cls, pred: np.ndarray, actual: np.ndarray):
        """
        Calculate the regrssion scores according to a set of predicted values (`pred`) and actual values (`actual`).

        Parameters
        ----------
        pred : np.ndarray
            Prediction results based on test set feature columns
        actual : np.ndarray
            The test set target values from the original dataframe

        Returns
        -------
        `RegressionScores`
        """
        pred, actual = sanitize_pred_and_actual(pred, actual)

        def calc_rmsle(y_true: np.ndarray, y_pred: np.ndarray) -> float:
            try:
                log_diffs: np.ndarray = np.square(
                    np.log(y_true + 1) - np.log(y_pred + 1)
                )
                msle = np.sum(log_diffs) / len(log_diffs)
                res = np.sqrt(msle)
            except Exception as e:
                logging.error("Unable to calculate rmsle: " + str(e))
                res = float("nan")
            return res

        def calc_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
            variance = np.var(y_true)
            if (
                variance == 0
            ):  # The variance would be 0 if (1) There is only one sample or (2) There is no variation in the samples' actuals
                return float("nan")

            diffs = np.abs(np.subtract(y_true, y_pred))
            diffs_not_nan = diffs[~np.isnan(diffs)]

            square_diffs = np.square(diffs_not_nan)
            mse = np.sum(square_diffs) / len(square_diffs)

            return 1 - mse / variance

        def calc_metric_score(f: Callable[[np.ndarray, np.ndarray], float]):
            if actual.shape != pred.shape:
                raise RuntimeError(
                    f"actual shape ({actual.shape}) != predicted shape ({pred.shape})"
                )
            shape = actual.shape
            if len(shape) == 1:  # single target
                res = f(actual, pred)
            elif len(shape) == 2:  # multiple targets
                ls = list()
                for i in range(shape[0]):
                    ls.append(f(actual[i], pred[i]))
                res = np.sum(ls) / len(ls)
            else:  # can't happen
                raise RuntimeError(f"invalid shape: {shape}")
            return res

        mse = np.round(mean_squared_error(actual, pred), METRIC_DECIMAL)
        rmse = np.round(np.sqrt(mse), METRIC_DECIMAL)
        absolute_difference = np.abs(np.subtract(actual, pred))
        mae = np.round(np.mean(absolute_difference), METRIC_DECIMAL)
        # If there is any 0 or negative value in target values, don't calculate
        # mape
        mape = (
            float("nan")
            if np.any(actual <= 0)
            else np.round(100 * np.mean(absolute_difference / actual), METRIC_DECIMAL)
        )
        # If all the target values are 0 or any one of the target values is
        # negative, don't calculate wmape
        wmape = (
            float("nan")
            if np.all(actual == 0) or np.any(actual < 0)
            else np.round(
                100 * np.sum(absolute_difference) / np.sum(actual), METRIC_DECIMAL
            )
        )
        r2 = np.round(calc_metric_score(calc_r2), METRIC_DECIMAL)
        deviance = mse
        rmsle = np.round(calc_metric_score(calc_rmsle), METRIC_DECIMAL)
        return cls(
            mse=mse,
            rmse=rmse,
            rmsle=rmsle,
            mae=mae,
            mape=mape,
            wmape=wmape,
            r2=r2,
            deviance=deviance,
        )


class ClassificationScores(BaseModel):
    """
    If there are more than 2 classes, it is a MultinomialScores. Otherwise it is a BinomialScores.

    For BinomialScores, the metrics include:
        - logloss (`logloss`)
        - mean per class error (`mean_per_class_error`)
        - misclassification (`misclassification`)
        - area under curve (`auc`)
        - lift top group (`lift_top_group`)

    For MultinomialScores, the metrics include:
        - logloss (`logloss`)
        - mean per class error (`mean_per_class_error`)
        - misclassification (`misclassification`)

    """

    logloss: NonNegativeFloat
    mean_per_class_error: NonNegativeFloat
    misclassification: NonNegativeFloat

    @staticmethod
    def get_scores(
        pred: np.ndarray, pred_proba: np.ndarray, actual: np.ndarray, labels: np.ndarray
    ):
        """
        Calculate the classification scores according to a set of predicted values (`pred`) and actual values (`actual`).
        If `labels.size > 2`, a `MultinomialScores` will be returned. Otherwise it will return `BinomialScores`.

        Parameters
        ----------
        pred : np.ndarray
            Prediction results based on test set feature columns
        pred_proba : np.ndarray
            Nested list of probability scores.

            Each sub-list represents the probability of each class being the
            proper prediction for a particular record. Used for the log loss metric
            e.g., `[[ 0.1, 0.8, 0.1] [ 0.0, 0.79 , 0.21] .... ]`,
            meaning that, for record X[0] in the test set, the proper prediction
            being class_0 is 10%, class_1 is 80%, and class_2 is 10%.
        actual : np.ndarray
            The test set target values from the original dataframe
        labels : np.ndarray
            The labels that appear in target column.

        Returns
        -------
        An instance of either `MultinomialScores` or `BinomialScores`.
        """

        pred, actual = sanitize_pred_and_actual(pred, actual)

        if labels.size < 2:
            raise ValueError(f"Invalid labels, has to be more than 1, got {labels}")

        def lift_top_group(y_true: np.ndarray, y_score: np.ndarray) -> float:
            top_group = sorted(zip(y_true, y_score), key=lambda x: -x[1])
            one_percent_len = int(np.ceil(len(top_group) / 100.0))
            return np.mean([x[0] for x in top_group[:one_percent_len]]) / np.mean(
                y_true
            )

        encoder = LabelEncoder()
        labels = encoder.fit_transform(labels)
        actual = encoder.transform(actual)
        pred = encoder.transform(pred)
        log_loss_ = log_loss(actual, pred_proba, labels=labels)
        # pred_scores = [pred_proba[i[0]][x] for i, x in np.ndenumerate(pred)]
        misclassification = 1 - accuracy_score(actual, pred)
        mpce = mean_per_class_error(actual=actual, pred=pred)
        if len(labels) > 2:  # Multiple classification problem
            return MultinomialScores(
                logloss=log_loss_,
                mean_per_class_error=mpce,
                misclassification=misclassification,
            )
        else:  # Binary classification problem
            y_score = pred_proba[:, 1]
            auc_ = roc_auc_score(actual, y_score)
            lift = lift_top_group(actual, y_score)
            return BinomialScores(
                logloss=log_loss_,
                mean_per_class_error=mpce,
                misclassification=misclassification,
                auc=auc_,
                lift_top_group=lift,
            )


class BinomialScores(ClassificationScores):
    """
    The binomial scores set.

    Metrics include:
        - logloss (`logloss`)
        - misclassification (`misclassification`)
        - mean per class error (`mean_per_class_error`)
        - area under curve (`auc`)
        - lift top group (`lift_top_group`)
    """

    auc: NonNegativeFloat
    lift_top_group: NonNegativeFloat

    @validator("auc", "lift_top_group")
    def check_nonnan_and_nonnegative(cls, v):
        if np.isnan(v) or v < 0:
            raise ValueError(f"{v} should be non-NaN and greater than or equal to 0")
        return v


class MultinomialScores(ClassificationScores):
    """
    The multinomial scores set.

    Metrics include:
        - logloss (`logloss`)
        - misclassification (`misclassification`)
        - mean per class error (`mean_per_class_error`)
    """


Scores = Union[RegressionScores, BinomialScores, MultinomialScores]


class CVScores(BaseModel):
    """
    The CV scores struct.

    Usage
    -----
    ```python
    split_scores: List[Scores] = []
    for _ in nfolds:
        # dates, actual = extract_from_data(df)
        # pred = model.predict(dates)
        split_scores.append(RegressionScores.get_scores(pred, actual))
    # To get the CV scores that can be sent from FastAPI, do this
    CVScores(split_scores=split_scores).to_report()
    ```
    """

    split_scores: List[Scores]

    @validator("split_scores")
    def check_folds(cls, v):
        if not v:
            raise ValueError("No score")
        types = {type(f).__name__ for f in v}
        if len(types) > 1:
            raise ValueError(
                f"All split scores must have consistent type. Found {types}"
            )
        return v

    def to_report(self) -> Dict[str, List[float]]:
        """
        Turns this CV scores object into a `dict` from `str` (the metric names) to a list of `floats` (the actual scores).

        """
        return {
            field: [score.dict()[field] for score in self.split_scores]
            for field in self.split_scores[0].__fields__
        }
