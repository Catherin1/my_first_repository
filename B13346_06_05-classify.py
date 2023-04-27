"""Classify a remotely sensed image"""

# https://github.com/GeospatialPython/Learn/raw/master/thermal.zip
try:
    import gdal
except:
    from osgeo import gdal_array, osr
import colorsys
# 确定需要处理的遥感影像
src = "GF1.jpg"
# 定义输出的遥感影像名称
tgt = "GF1_3.jpg"

# 利用gdal导入遥感影像
srcArr = gdal_array.LoadFile(src)

# 设置类别数量，
bins_num = 15
#函数返回每个bin的计数和bin edge，此次只需要bin edge
classes = gdal_array.numpy.histogram(srcArr, bins=bins_num)[1]

# 颜色查找表（LUT）：需要比类别的数量多
# Specified as R, G, B tuples
lut = [[255, 0, 0], [191, 48, 48], [166, 0, 0], [255, 64, 64], [255, 115, 115],
       [255, 116, 0], [191, 113, 48], [255, 178, 115], [0, 153, 153],
       [29, 115, 115], [0, 99, 99], [166, 75, 0], [0, 204, 0], [51, 204, 204],
       [255, 150, 64], [92, 204, 204], [38, 153, 38], [0, 133, 0],
       [57, 230, 57], [103, 230, 103], [184, 138, 0]]
# 定义将遥感图像划分为不同类别时的起始值
start = 1

# 自动计算颜色表
# Hue色调, Saturaction饱和度, Value明暗度
# color space
h = .67
s = 1
v = 1
# We'll step through colors from:
# blue-green-yellow-orange-red.
# Blue=low elevation, Red=high-elevation
step = h / bins_num
# 创建调色板
for i in range(bins_num):
    rp, gp, bp = colorsys.hsv_to_rgb(h, s, v)
    r = int(rp * 255)
    g = int(gp * 255)
    b = int(bp * 255)
    #替换颜色表对应项
    lut[i] = [r, g, b]
    h -= step

# Set up the RGB color JPEG output image
rgb = gdal_array.numpy.zeros((3, srcArr.shape[0],
                              srcArr.shape[1], ), gdal_array.numpy.float32)

# Process all classes and assign colors
for i in range(len(classes)):
    mask = gdal_array.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1

# Save the image
output = gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), tgt, format="JPEG")
output = None