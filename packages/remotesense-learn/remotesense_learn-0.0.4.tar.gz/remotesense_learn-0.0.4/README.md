# 遥感影像机器学习工具包



## 安装
可以使用pip进行安装：
~~~
pip install remotesense-learn
~~~
本程序依赖的包有`scikit-learn`、`numpy`、`rasterio`等。

## 使用
### 读取数据

~~~python
from rslearn import  ImageFrame
img=ImageFrame.read("example_data/bhtmref.img")
~~~

#### 保存栅格文件

### 聚类分析

### 监督分类

### 数据处理

#### 数据标准化

#### 图像滤波

### 可视化

#### 波段预览

#### 波段直方图
