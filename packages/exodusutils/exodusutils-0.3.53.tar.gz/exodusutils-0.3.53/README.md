# Exodus common utilities

This is the library defining the schemas for exodus utilities.

## Structure

### `exodusutils`

Contains helpful utility functions.

### `schemas`

In the `schemas` folder you can find the following:
- Schema definitions for the model algorithm's incoming requests
- Schema definitions for the model algorithm's responses
- Definitions for `RegressionScores` and `ClassificationScores`
- Definitions for types such as `Attribute` and `Column`

### `predict`

The `predict` folder contains helper functions for prediction.

### `enums.py`

Contains enums used by Exodus. Current contains the following:
- `TimeUnit`, with helper methods to convert timestamps to different formats
- `DataType`, with helper methods to convert from `Pandas` types

### `feature_engineering.py`

Contains commonly used feature engineering methods. Currently includes:
- One-hot encoding
- Label encoding
- Time component encoding
It is recommended to use at least 1 method in this file during training.

### `frame_manipulation.py`

Contains multiple frame manipulation methods. Used during prediction, should pick the method that corresponds to the one used during training.

### `frames.py`

Contains definitions and helper functions for the following classes:
- `SplitFrames`: A 3-tuple with a training dataframe, a testing dataframe, and a validation dataframe.
- `CVFrames`: A list of `SplitFrames`. Should not be instantiated manually, user should use `CVFrames.iid` helper classmethod.
