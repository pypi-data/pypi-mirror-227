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
    `ClassifierWrapper`类是一个包装器，允许分类器模型在 3 维输入矩阵（例如图像数据）上进行拟合、预测和评分。

    """
    
    def __init__(self,model) -> None:
        '''将分类器进行包装
        
        Parameters
        ----------
        model
            “model”参数是分类器类的实例。它用于存储和操作将用于分类任务的分类器模型。
    
        '''
        self.__model:Classifier=model
        pass
    
    def fit(self,X:MatrixLike,y:MatrixLike,**fit_params):
        '''该函数接收输入数据和标签，重新调整它们的形状，并将模型拟合到数据。
        
        Parameters
        ----------
        X : MatrixLike
            输入数据矩阵，其中每行代表一个样本，每列代表一个特征。它应该是BSQ格式排列的图像矩阵。
        y : MatrixLike
            参数“y”表示数据集中的目标变量或因变量。它是一个类似矩阵的对象，包含数据集中每个样本的目标变量的值。
        
        Returns
        -------
            使用给定的 X 和 y 数据拟合模型后类本身 (self) 的实例。
        
        '''
        SHAPE=X.shape
        #self.n_features_in_=SHAPE[0]
        
        X=np.transpose(X)
        X=np.reshape(X,[-1,SHAPE[0]])

        y=np.transpose(y)
        y=np.reshape(y ,[-1])
        
        self.__model.fit(X,y,**fit_params)
        
        return self
    
    
    
    def predict(self,X:MatrixLike):
        '''“predict”函数接受 3 维输入矩阵，对其进行整形和转置，使用模型进行预测，然后返回预测的输出矩阵。
        
        Parameters
        ----------
        X : MatrixLike
            参数 X，为BSQ排列的图像矩阵
        
        Returns
        -------
            预测值，Y。
        
        '''
        SHAPE=X.shape
        assert len(SHAPE)==3
        
        X= np.transpose(X) #变换维度
        X=np.reshape(X,[-1,SHAPE[0]]) #变换形状
    
        Y=self.__model.predict(X) #预测
        
        Y=np.reshape(Y,[SHAPE[2],SHAPE[1]])
        Y=np.transpose(Y)
        
        return Y
    
    def score(self, X: MatrixLike, y: MatrixLike | ArrayLike, sample_weight: ArrayLike | None = None) -> Float:
        '''“score”函数计算预测标签与真实标签相比的准确度得分。
        
        Parameters
        ----------
        X : MatrixLike
            输入数据矩阵。它应该是一个类似矩阵的对象，例如 NumPy 数组或 Pandas DataFrame。
        y : MatrixLike | ArrayLike
            参数“y”表示给定输入数据“X”的真实标签或目标值。它应当是类似矩阵的对象。
        sample_weight : ArrayLike | None
            “sample_weight”参数是一个可选的类似数组的对象，用于为各个样本分配权重。它允许您在评分过程中更加重视某些样本。如果未提供，则假定所有样本具有相同的权重。
        
        Returns
        -------
            准确度得分。
        
        '''
        y_pred=self.predict(X)
        y_pred=np.reshape(y_pred,[-1])
        y=np.reshape(y,[-1])
        
        return accuracy_score(y,y_pred,sample_weight=sample_weight)
        
    
    @property
    def n_features_in_(self)-> int:
        """返回模型中的特征数量，对于遥感影像，特征数量即影像层数"""
        return self.__model.n_features_in_
    
    def get_params(self)->dict:
        '''函数“get_params”返回一个包含模型参数的字典以及模型类的名称。
        '''
        d= self.__model.get_params()
        d["model"]=self.__model.__class__.__name__
        return d