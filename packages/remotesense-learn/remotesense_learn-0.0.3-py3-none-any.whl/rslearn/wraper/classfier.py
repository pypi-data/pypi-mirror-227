#from sklearn._typing import ArrayLike, Float, MatrixLike
from sklearn.svm import SVC
from sklearn.base import ClassifierMixin
import numpy   as np
from sklearn.metrics import accuracy_score
from typing import *


import decimal
import io
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
import numpy.typing


from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin

from .._typing import *

class ClassifierWrapper(ClassifierMixin):
    """分类器包装器
    """
    
    def __init__(self,model) -> None:
        self.__model:Classifier=model
        pass
    
    def fit(self,X:MatrixLike,y:MatrixLike,**fit_params):
        SHAPE=X.shape
        #self.n_features_in_=SHAPE[0]
        
        X=np.transpose(X)
        X=np.reshape(X,[-1,SHAPE[0]])

        y=np.transpose(y)
        y=np.reshape(y ,[-1])
        
        self.__model.fit(X,y,**fit_params)
        
        return self
    
    
    
    def predict(self,X:MatrixLike):
        SHAPE=X.shape
        assert len(SHAPE)==3
        
        X= np.transpose(X) #变换维度
        X=np.reshape(X,[-1,SHAPE[0]]) #变换形状
    
        Y=self.__model.predict(X) #预测
        
        Y=np.reshape(Y,[SHAPE[2],SHAPE[1]])
        Y=np.transpose(Y)
        
        return Y
    
    def score(self, X: MatrixLike, y: MatrixLike | ArrayLike, sample_weight: ArrayLike | None = None) -> Float:
        y_pred=self.predict(X)
        y_pred=np.reshape(y_pred,[-1])
        y=np.reshape(y,[-1])
        
        return accuracy_score(y,y_pred,sample_weight=sample_weight)
        
    
    @property
    def n_features_in_(self):
        return self.__model.n_features_in_
    
    def get_params(self)->dict:
        d= self.__model.get_params()
        d["model"]=self.__model.__class__.__name__
        return d