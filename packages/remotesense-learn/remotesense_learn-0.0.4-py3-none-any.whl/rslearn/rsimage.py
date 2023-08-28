import rasterio
from PIL.JpegImagePlugin import JpegImageFile
from affine import Affine
from rasterio import plot

from rslearn.utils import *
from ._typing import *


class ImageFrame:
    """
    图像类

    Note
    ----
    这里的图像采用BSQ排列
    """

    def __init__(self, data: MatrixLike, dispose: ['BSQ', "BIL", "BIP"], bands_name: Sequence = ...) -> None:
        '''该函数使用数据、数据排列方法和 band 名称初始化一个对象。
        
        Parameters
        ----------
        data : MatrixLike
            “data”参数是一个类似矩阵的对象，表示图像的数据。它可以是 NumPy 数组或任何其他可以转换为 NumPy 数组的对象。
        dispose : ['BSQ', "BIL", "BIP"]
            `dispose` 参数用于指定输入矩阵中数据的排列。它可以采用以下值之一：“BSQ”（波段顺序）、“BIL”（波段按行交错）或“BIP”（波段按像素交错）
        bands_name : Sequence
            数据中每个波段的名称序列。
        
        '''

        if dispose == "BSQ":
            self.__data = np.array(data)
        elif dispose == "BIL":
            self.__data = bil_to_bsq(np.array(data))
        elif dispose == "BIP":
            self.__data = bip_to_bsq(np.array(data))
        else:
            raise Exception()

        self.__shape = self.__data.shape

        self.__profile = {}

    @classmethod
    def read(cls, fp):
        '''该函数使用 rasterio 读取光栅文件，使用数据创建图像对象，并设置图像的配置文件。
        
        Parameters
        ----------
        cls
            参数“cls”是对“read”方法所属类的引用。它用于使用“data”和“dispose”参数创建类“cls”的实例。
        fp
            参数“fp”代表“文件路径”。它是您要读取的光栅文件的路径。
        
        Returns
        -------
            类“cls”的实例，它是使用“data”和“dispose”参数创建的。然后为“img”实例分配“src”对象的配置文件并返回。
        
        '''
        with rasterio.open(fp) as src:
            data = src.read()
            img = cls(data, dispose="BSQ")
            img.set_profile(src.profile)
            return img

    @classmethod
    def read_tif(cls, fp):
        """

        Parameters
        ----------
        fp

        Returns
        -------

        """

        raise NotImplementedError()

        pass

    @classmethod
    def read_jpg(cls, fp):
        img = JpegImageFile(fp=fp)
        data = np.array(img)
        return cls(data, dispose="BIP")

    @property
    def profile(self):
        return self.__profile

    def set_profile(self, profile: DictLike):
        # TODO 这里应该加一些安全措施
        self.__profile = profile

    @property
    def shape(self):
        return self.__data.shape

    @property
    def n_bands(self) -> int:
        return self.shape[0]

    @property
    def bands(self) -> int:
        return self.to_bsq_mat()

    @property
    def transform(self) -> Affine:
        return self.profile.get("transform", Affine.identity())

    def to_bil_mat(self):
        return bsq_to_bil(self.__data)

    def to_bip_mat(self):
        return bip_to_bsq(self.__data)

    def to_bsq_mat(self):
        return self.__data

    def display(self, bidx: list[int] = ...):
        '''`display` 函数用于显示图像的指定波段。
        
        Parameters
        ----------
        bidx : list[int]
            `bidx` 参数是一个整数列表，指定要显示的波段。如果未提供“bidx”，则默认为“Ellipsis”。如果“bidx”是“Ellipsis”，则该函数检查波段数（“n_bands”）并设置“
        
        '''
        if bidx is Ellipsis:
            if self.n_bands < 3:
                bidx = list[range(self.n_bands)]
            else:
                bidx = [0, 1, 2]

        plot.show(self.bands[bidx, :, :], transform=self.transform)
