"""Classify a remotely sensed image"""

import numpy as np
try:
    import gdal
except:
    from osgeo import gdal_array, osr
import colorsys

# 确定需要处理的遥感影像
src = "GF1.jpg"
# 定义输出的遥感影像名称
tgt = "GF1_radom4.jpg"

# 利用gdal导入遥感影像
srcArr = gdal_array.LoadFile(src)

# 设置类别数量，
bins_num = int(input("请输入分类类别数量："))
#利用numpy中的直方图函数numpy.histogram对遥感影像数据进行直方图统计
# 函数返回每个bin的计数和bin edge，这里只需要bin edge
classes = gdal_array.numpy.histogram(srcArr, bins=bins_num)[1]
# 定义将遥感图像划分为不同类别时的起始值
start = classes[0]

# # 随机生成RGB颜色查找表（LUT）：需要比类别的数量多
lut = np.random.randint(0, 256, size=(bins_num+1, 3), dtype=np.uint8)



# # 利用Hue色调, Saturaction饱和度, Value明暗度自动计算颜色表
# h = .67
# s = 1
# v = 1
# step = h / bins_num
# lut = np.zeros((bins_num+1, 3), dtype=np.uint8)
# # 创建调色板
# for i in range(bins_num):
#     rp, gp, bp = colorsys.hsv_to_rgb(h, s, v)
#     r = int(rp * 255)
#     g = int(gp * 255)
#     b = int(bp * 255)
#     #替换颜色表对应项
#     lut[i] = [r, g, b]
#     h -= step

# 创建一个三维数组，用于存储遥感图像的RGB颜色信息
rgb = gdal_array.numpy.zeros((3, srcArr.shape[0],
                              srcArr.shape[1], ), gdal_array.numpy.float32)
# 利用颜色查找表lut对影像进行颜色渲染
for i in range(len(classes)-1):
    # 使用numpy.logical_and函数创建一个掩膜，该掩膜指示哪些像素属于该类别
    mask = gdal_array.numpy.logical_and(start <= srcArr, srcArr <= classes[i+1])
    for j in range(len(lut[i])):
        # 使用numpy.choose函数根据mask为每个像素分配相应的RGB颜色
        rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i+1]

# 保存图片
output = gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), tgt, format="JPEG")
print('successful')
output = None
