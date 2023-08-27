import decimal
import io
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
import numpy.typing
from typing import*
from rasterio._base import Profile


from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin


Decimal = decimal.Decimal
PythonScalar = str | int | float | bool

ArrayLike = numpy.typing.ArrayLike
MatrixLike = np.ndarray | pd.DataFrame | spmatrix
FileLike = io.IOBase
PathLike = str
DictLike= Dict|Profile


Int = int | np.int8 | np.int16 | np.int32 | np.int64
Float = float | np.float16 | np.float32 | np.float64

PandasScalar = pd.Period | pd.Timestamp | pd.Timedelta | pd.Interval
Scalar = PythonScalar | PandasScalar

Estimator = BaseEstimator
Classifier = ClassifierMixin
Regressor = RegressorMixin

Color = tuple[float, float, float] | str