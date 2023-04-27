"""Classify a remotely sensed image"""

# https://github.com/GeospatialPython/Learn/raw/master/thermal.zip
try:
    import gdal
except:
    from osgeo import gdal_array, osr
import colorsys
# Input file name (thermal image)
src = "/Users/stzhou/geodata/GF1/GF1_PMS1_E114.2_N30.5_20141020_L1A0000398027-PAN1.jpg"

# Output file name
tgt = "/Users/stzhou/geodata/classified.jpg"

# Load the image into numpy using gdal
srcArr = gdal_array.LoadFile(src)

# Split the histogram into 20 bins as our classes
bins_num = 20
classes = gdal_array.numpy.histogram(srcArr, bins=bins_num)[1]

# Color look-up table (LUT) - must be len(classes)+1.
# Specified as R, G, B tuples
lut = [[255, 0, 0], [191, 48, 48], [166, 0, 0], [255, 64, 64], [255, 115, 115],
       [255, 116, 0], [191, 113, 48], [255, 178, 115], [0, 153, 153],
       [29, 115, 115], [0, 99, 99], [166, 75, 0], [0, 204, 0], [51, 204, 204],
       [255, 150, 64], [92, 204, 204], [38, 153, 38], [0, 133, 0],
       [57, 230, 57], [103, 230, 103], [184, 138, 0]]
# Starting value for classification
start = 1

# 自动计算颜色表
# Hue, Saturaction, Value
# color space
h = .67
s = 1
v = 1
# We'll step through colors from:
# blue-green-yellow-orange-red.
# Blue=low elevation, Red=high-elevation
step = h / bins_num
# Build the palette
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