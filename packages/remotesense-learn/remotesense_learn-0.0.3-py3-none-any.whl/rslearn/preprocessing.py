from sklearn.base import TransformerMixin
from typing import *
import numpy as np
import math

class StandardScaler2D(TransformerMixin):
    
    def __init__(self, *, copy: bool = True, with_mean: bool = True, with_std: bool = True) -> None:
        #super().__init__(copy=copy, with_mean=with_mean, with_std=with_std)
        pass
    
    def fit(self,X:np.ndarray):
        self.n_features_in_=len(X)
        self.mean_=[ np.mean(b) for b in X ]
        self.var_=[np.var(b) for b in X]
        self.scale_=[math.sqrt(v) for v in self.var_ ]
        return self
        
    def transform(self,X:np.ndarray):
        assert X.shape[0]==self.n_features_in_
        X1=[(layer-mean)/scale for layer,mean,scale in zip(X,self.mean_,self.scale_)]
        return np.array(X1)
            