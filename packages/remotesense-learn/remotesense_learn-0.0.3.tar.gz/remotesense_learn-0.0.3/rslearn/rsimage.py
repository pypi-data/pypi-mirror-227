from .utils import *
from typing import *
from ._typing import *
from rasterio import plot
from rasterio._base import Profile
from PIL.JpegImagePlugin import JpegImageFile


class ImageFrame:
    """
    图像类
    
    Note
    ----
    这里的图像采用BSQ排列
    """
    
    def __init__(self, data: MatrixLike, dispose: ['BSQ', "BIL", "BIP"],bands_name:Sequence=...) -> None:
        
        if dispose=="BSQ":
            self.__data=np.array(data)
        elif dispose=="BIL":
            self.__data=bil_to_bsq(np.array(data))
        elif dispose=="BIP":
            self.__data=bip_to_bsq(np.array(data))
        else:
            raise Exception()
        
        self.__shape=self.__data.shape
        
        self.__profile = {}
        
    
    @classmethod
    def read_tif(cls,fp):
        
        raise NotImplementedError()
        
        pass
    
    

    @classmethod
    def read_jpg(cls,fp):
        img=JpegImageFile(fp=fp)
        data=np.array(img)
        return cls(data,dispose="BIP")


    @property
    def profile(self):
        return self.__profile

    def set_profile(self, profile:DictLike):
        # TODO 这里应该加一些安全措施
        self.__profile = profile
    
    @property
    def shape(self):
        return self.__data.shape
    
    @property
    def n_bands(self)->int:
        return self.shape[0]
        
    @property
    def bands(self)->int:
        return self.to_bsq_mat()


    def to_bil_mat(self):
        return bsq_to_bil(self.__data)

    def to_bip_mat(self):
        return  bip_to_bsq( self.__data)

    def to_bsq_mat(self):
        return self.__data
    
    def display(self):
        plot.show(self.to_bsq_mat(),**self.profile)