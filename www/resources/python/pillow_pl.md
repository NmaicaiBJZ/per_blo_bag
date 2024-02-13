# pillow创建对象
`from PIL import Image`导入包
## open()
使用 Image 类的 open() 方法，可以创建一个 Image 对象  
`im = Image.open(fp,mode="r")`

参数说明：  
- fp：即 filepath 的缩写，表示文件路径，字符串格式；
- mode：可选参数，若出现该参数，则必须设置为 "r"，否则会引发 ValueError 异常。

示例：
```python
from PIL import Image
#打开一图片文件
im = Image.open("C:\Users\···\data\00008-2630469047.png")
#要显示图像需要调用 show()方法
im.show()
```
## new()
使用 Image 类提供的 new() 方法可以创建一个新的 Image 对象  
`im=Image.new(mode,size,color)`

参数说明如下：  
- mode：图像模式，字符串参数，比如 RGB（真彩图像）、L（灰度图像）、CMYK（色彩图打印模式）等；
- size：图像大小，元组参数（width, height）代表图像的像素大小；
- color：图片颜色，默认值为 0 表示黑色，参数值支持（R,G,B）三元组数字格式、颜色的十六进制值以及颜色英文单词。

示例：
```python
#使用颜色的十六进制格式
im_1=Image.new(mode='RGB',(260,100),color="#ff0000")
im_1.show()
```
# Pillow Image对象属性
Image 对象有一些常用的基本属性，这些属性能够帮助我们了解图片的基本信息
## size 查看图像尺寸
```python
im = Image.open("C:/Users/···/Desktop/c-net.png")
#打印image对象
print(im)
#查看尺寸
print("宽是%s高是%s"%(im.width,im.height))
#或者通过size查看
print("图像的大小size:",im.size)
```
运行结果
```
<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=455x191 at 0x381C750>
宽是455高是191
图像的大小size: (455, 191)
```
##  format 查看图片的格式
```python
im = Image.open("C:/Users/···/Desktop/c-net.png")
print("图像的格式:",im.format)
```
## readonly 图片是否为只读
```python
im = Image.open("C:/Users/···/Desktop/c-net.png")
# 该属性的返回为 0 或者 1，分别对应着是和否
print("图像是否为只读:",im.readonly)
```
## info 查看图片相关信息
```python
im = Image.open("C:/Users/···/Desktop/c-net.png")
# 包括了每英寸像素点大小和截图软件信息
print("图像信息:",im.info)
```
该属性的返回值为字典格式，运行结果：
```
图像信息: {'dpi': (96, 96), 'Software': 'Snipaste'}
```
## mode 图像模式
```python
im = Image.open("C:/Users/···/Desktop/c-net.png")
print("图像模式信息:",im.mode)
```
运行结果：
```
图像的模式: RGBA
```
图片模式：
|mode|描述|
|:--:|:--:|
|1|1 位像素（取值范围 0-1），0表示黑，1 表示白，单色通道。|
|L|8 位像素（取值范围 0 -255），灰度图，单色通道。|
|P|8 位像素，使用调色板映射到任何其他模式，单色通道。|
|RGB|3 x 8位像素，真彩色，三色通道，每个通道的取值范围 0-255。|
|RGBA|4 x 8位像素，真彩色+透明通道，四色通道。|
|CMYK|4 x 8位像素，四色通道，可以适应于打印图片。|
|YCbCr|3 x 8位像素，彩色视频格式，三色通道。|
|LAB|3 x 8位像素，L * a * b颜色空间，三色通道|
|HSV|3 x 8位像素，色相，饱和度，值颜色空间，三色通道。|
|I|32 位有符号整数像素，单色通道。|
|F|32 位浮点像素，单色通道。|

# Pillow图片格式转换
## save()
save() 方法用于保存图像，当不指定文件格式时，它会以默认的图片格式来存储；如果指定图片格式，则会以指定的格式存储图片。语法格式如下：  
`Image.save(fp, format=None)`  
参数说明如下：
- fp：图片的存储路径，包含图片的名称，字符串格式；
- format：可选参数，可以指定图片的格式。

示例：
```python
from PIL import Image
im = Image.open("C:/Users/···/c-net.png")
im.save('C:/Users/···/c.biancheng.net.bmp')
```

## convert()+save()
并非所有的图片格式都可以用 save() 方法转换完成，比如将 PNG 格式的图片保存为 JPG 格式将会报错: `OSError: cannot write mode RGBA as JPEG`

Image 类提供的 convert() 方法可以实现图像模式的转换。该函数提供了多个参数，比如 mode、matrix、dither 等，其中最关键的参数是 mode，其余参数无须关心。语法格式如下：  
`convert(mode,parms**)`  
- mode：指的是要转换成的图像模式；
- params：其他可选参数。

示例：
```python
from PIL import Image
im = Image.open("C:/Users/···/c-net.png")
#此时返回一个新的image对象，转换图片模式
image=im.convert('RGB')
#调用save()保存
image.save('C:/Users/···/c.biancheng.net.jpg')
```
# Pillow图像缩放操作
在图像处理过程中经常会遇到缩小或放大图像的情况，Image 类提供的 resize() 方法能够实现任意缩小和放大图像。    
resize() 函数的语法格式如下：  
`resize(size, resample=image.BICUBIC, box=None, reducing_gap=None)`  
参数说明：  
- size：元组参数 (width,height)，图片缩放后的尺寸；
- resample：可选参数，指图像重采样滤波器，与 thumbnail() 的 resample 参数类似，默认为 Image.BICUBIC；
- box：对指定图片区域进行缩放，box 的参数值是长度为 4 的像素坐标元组，即 (左,上,右,下)。注意，被指定的区域必须在原图的范围内，如果超出范围就会报错。当不传该参数时，默认对整个原图进行缩放；
- reducing_gap：可选参数，浮点参数值，用于优化图片的缩放效果，常用参数值有 3.0 和 5.0。

示例：  
```python
im = Image.open("C:/Users/···/c-net.png")
try:
    #放大图片
    image=im.resize((550,260))
    #将新图像保存至桌面
    image.save("C:/Users/···/放大图像.png")
    print("查看新图像的尺寸",image.size)
except IOError:
    print("放大图像失败")
```

对图片的局部放大：
```python
im = Image.open("C:/Users/···/c-net.png")
try:
    #选择放大的局部位置，并选择图片重采样方式
    # box四元组指的是像素坐标 (左,上,右,下) 
    #(0,0,120,180)，表示以原图的左上角为原点，选择宽和高分别是(120,180)的图像区域
    image=im.resize((550,260),resample=Image.LANCZOS,box=(0,0,120,180))
    image.show()
    #保存
    image.save("C:/Users/···/放大图像.png")
    print("查看新图像的尺寸",image.size)
except IOError:
    print("放大失败")
```

## 创建缩略图
Image 对象提供了一个 thumbnail() 方法用来生图像的缩略图，该函数的语法格式如下：  
`thumbnail(size,resample)`  
- size：元组参数，指的是缩小后的图像大小；
- resample：可选参数，指图像重采样滤波器，有四种过滤方式，分别是 Image.BICUBIC（双立方插值法）、PIL.Image.NEAREST（最近邻插值法）、PIL.Image.BILINEAR（双线性插值法）、PIL.Image.LANCZOS（下采样过滤插值法），默认为 Image.BICUBIC。  

示例：
```python
im = Image.open("C:/Users/···/c-net.png")
im.thumbnail((150,50))
print("缩略图尺寸",im.size)
#将缩略图保存至桌面
im.save("C:/Users/···/th.png")
```
缩略图的尺寸可能与您指定的尺寸不一致，这是因为 Pillow 会对原图像的长、宽进行等比例缩小，当指定的尺寸不符合图像的尺寸规格时，缩略图就会创建失败， 比如指定的尺寸超出了原图像的尺寸规格。
## 批量修改图片尺寸
```python
# 批量修改图片尺寸
import os
from PIL import Image
#读取图片目录
fileName = os.listdir('C:/Users/···/image01/')
print(fileName)
#设定尺寸
width = 350
height = 350
# 如果目录不存在，则创建目录
if not os.path.exists('C:/Users/···/NewImage/'):
    os.mkdir('C:/Users/···/NewImage/')
# 循环读取每一张图片
for img in fileName:
    old_pic = Image.open('C:/Users/···/image01/' + img)
    new_image = old_pic.resize((width, height),Image.BILINEAR)
    print (new_image)
    new_image.save('C:/Users/···/NewImage/'+img)
```

# Pillow图像分离与合并
图像（指数字图像）由许多像素点组成，像素是组成图像的基本单位，而每一个像素点又可以使用不同的颜色，最终呈现出了绚丽多彩的图像。它们的本质就是图片呈现颜色时需要遵循的规则，比如 RGB、RGBA、CYMK 等，而图像的分离与合并，指的就是图像颜色的分离和合并。
## split()
split() 的使用方法比较简单，用来分离颜色通道。  
示例：  
```python
im=Image.open("C:/Users/···/1.jpg")
#修改图像大小，以适应图像处理
image=im.resize((450,400))
image.save("C:/Users/···/2.jpg")
#分离颜色通道，产生三个 Image对象
r,g,b = image.split()
r.show()
g.show()
b.show()
```
## merge()
Image 类提供的 merge() 方法可以实现图像的合并操作。注意，图像合并，可以是单个图像合并，也可以合并两个以上的图像。  
格式：  
`Image.merge(mode, bands)`

参数说明如下：  
- mode：指定输出图片的模式  
- bands：参数类型为元组或者列表序列，其元素值是组成图像的颜色通道，比如 RGB 分别代表三种颜色通道，可以表示为 (r,g,b)。  

注意，该函数会返回一个新的 Image 对象。

单个图像的合并指的是将颜色通道进行重新组合，从而得到不一样的图片效果，代码如下所示：
```python
im=Image.open("C:/Users/···/1.jpg")
#修改图像大小，以适应图像处理
image=im.resize((450,400))
image.save("C:/Users/···/2.jpg")
#分离颜色通道，产生三个 Image对象
r,g,b = image.split()
#重新组合颜色通道，返回先的Image对象
image_merge=Image.merge('RGB',(b,g,r))
image_merge.show()
#保存图像至桌面
image_merge.save("C:/Users/···/3.jpg")
```

两张图片的合并操作也并不复杂，但是要求两张图片的模式、图像大小必须要保持一致，否则不能合并。因此，对于那些模式、大小不同的图片要进行预处理。  
下面我们将蝴蝶图与向日葵图进行合并，向日葵原图如下：  
```python
im_1 = Image.open("C:/Users/···/2.jpg")
im_2= Image.open("C:/Users/···/向日葵.jpg")
#因为两种图片的图片格式一致，所以仅需要处理图片的大小，让它们保持一致
#让 im_2 的图像尺寸与 im_1 一致,注意此处新生成了 Image 对象
image = im_2.resize(im_1.size)
#接下来，对图像进行颜色分离操作
r1, g1 ,b1 = im_1.split()
r2, g2 , b2 = image.split()
# 合并图像
im_3 = Image.merge('RGB',[r2,g1,b2])
im_3.show()
im_3.save("C:/Users/···/合成.jpg")
```

## blend() 混合图片
Image 类也提供了 blend() 方法来混合 RGBA 模式的图片（PNG 格式），函数的语法格式如下：  
`Image.blend(image1,image2, alpha)`

参数说明如下：
- image1，image2：表示两个 Image 对象。
- alpha：表示透明度，取值范围为 0 到 1，当取值为 0 时，输出图像相当于 image1 的拷贝，而取值为 1 时，则是 image2 的拷贝，只有当取值为 0.5 时，才为两个图像的中合。因此改值的大小决定了两个图像的混合程度。

与 RGB 模式相比，RGBA 在 RGB 的基础上增加了透明度，通过 Alpha 取值来决定两个图像的混合程度。示例如下：
```python
im1 = Image.open("C:/Users/···/c-net.png")
image = Image.open("C:/Users/···/心形函数图像.png")
im2=image.resize(im1.size)
def blend_im(im1,im2):
     #设置 alpha 为 0.5
    Image.blend(im1,im2,0.5).save("C:/Users/···/C语言中文网.png")
#调用函数
blend_im(im1,im2)  
```
# Pillow图像裁剪、复制、粘贴操作
图像的剪裁、复制、粘贴是图像处理过程中经常使用的基本操作，Pillow Image 类提供了简单、易用的 API 接口，能够帮助您快速实现这些简单的图像处理操作。  
## 图像裁剪操作
Image 类提供的 crop() 函数允许我们以矩形区域的方式对原图像进行裁剪，函数的语法格式如下：
`crop(box=None)`
- box：表示裁剪区域，默认为 None，表示拷贝原图像。  
注意：box 是一个有四个数字的元组参数 (x_左上,y_左下,x1_右上,y1_右下)，分别表示被裁剪矩形区域的左上角 x、y 坐标和右下角 x，y 坐标。默认 (0,0) 表示坐标原点，宽度的方向为 x 轴，高度的方向为 y 轴，每个像素点代表一个单位。

crop() 函数的会返回一个 Image 对象，使用示例如下：  
```python
im = Image.open("C:/Users/···/C语言中文网.png")
box =(0,0,200,100)      # 在图片左上角裁200长，100宽的图
im_crop = im.crop(box)
im_crop.show()
```
## 图像拷贝和粘贴
Image 类提供了 copy() 和 paste() 方法来实现图像的复制和粘贴。  
其中复制操作比较简单，下面主要介绍 paste() 粘贴方法，语法格式如下所示：  
`paste(image, box=None, mask=None)`  

该函数的作用是将一张图片粘贴至另一张图片中。注意，粘贴后的图片模式将自动保持一致，不需要进行额外的转换。参数说明如下：  
- image：指被粘贴的图片；
- box：指定图片被粘贴的位置或者区域，其参数值是长度为 2 或者 4 的元组序列，长度为 2 时，表示具体的某一点 (x,y)；长度为 4 则表示图片粘贴的区域，此时区域的大小必须要和被粘贴的图像大小保持一致。
- mask：可选参数，为图片添加蒙版效果。

下面复制一张原图像的副本，对副本进行裁剪、粘贴操作，代码如下所示：  
```python
im = Image.open("C:/Users/···/C语言中文网.png")
#复制一张图片副本
im_copy=im.copy()
#对副本进行裁剪
im_crop = im_copy.crop((0,0,200,100))
#创建一个新的图像作为蒙版，L模式，单颜色值
image_new = Image.new('L', (200, 100), 200)
#将裁剪后的副本粘贴至副本图像上，并添加蒙版
im_copy.paste(im_crop,(100,100,300,200),mask=image_new)
#显示粘贴后的图像
im_copy.show()
```
# Pillow图像几何变换
## transpose()翻转操作
该函数可以实现图像的垂直、水平翻转，语法格式如下：  
`Image.transpose(method)`  
method 参数决定了图片要如何翻转，参数值如下：
- Image.FLIP_LEFT_RIGHT：左右水平翻转；
- Image.FLIP_TOP_BOTTOM：上下垂直翻转；
- Image.ROTATE_90：图像旋转 90 度；
- Image.ROTATE_180：图像旋转 180 度；
- Image.ROTATE_270：图像旋转 270 度；
- Image.TRANSPOSE：图像转置；
- Image.TRANSVERSE：图像横向翻转。

该函数可以实现图像的垂直、水平翻转，语法格式如下：
```python
Image.transpose(method)
method 参数决定了图片要如何翻转，参数值如下：
Image.FLIP_LEFT_RIGHT：左右水平翻转；
Image.FLIP_TOP_BOTTOM：上下垂直翻转；
Image.ROTATE_90：图像旋转 90 度；
Image.ROTATE_180：图像旋转 180 度；
Image.ROTATE_270：图像旋转 270 度；
Image.TRANSPOSE：图像转置；
Image.TRANSVERSE：图像横向翻转。
```
## rotate() 任意角度旋转
当我们想把图像旋转任意角度时，可以使用 rotate() 函数，语法格式如下：  
`Image.rotate(angle, resample=PIL.Image.NEAREST, expand=None, center=None, translate=None, fillcolor=None)`  
参数说明如下：   
- angle：表示任意旋转的角度；
- resample：重采样滤波器，默认为 PIL.Image.NEAREST 最近邻插值方法；
- expand：可选参数，表示是否对图像进行扩展，如果参数值为 True 则扩大输出图像，如果为False 或者省略，则表示按原图像大小输出；
- center：可选参数，指定旋转中心，参数值是长度为 2 的元组，默认以图像中心进行旋转；
- translate：参数值为二元组，表示对旋转后的图像进行平移，以左上角为原点；
- fillcolor：可选参数，填充颜色，图像旋转后，对图像之外的区域进行填充。

使用示例如下：  
```python
im = Image.open("C:/Users/···/c-net.png")
#translate的参数值可以为负数，并将旋转图之外的区域填充为绿色
#返回同一个新的Image对象
im_out=im.rotate(45,translate=(0,-25),fillcolor="green")
im_out.show()
im_out.save("C:/Users/···/旋转图像.png")
```
## transform() 图像变换
该函数能够对图像进行变换操作，通过指定的变换方式，产生一张规定大小的新图像，语法格式如下：  
`Image.transform(size, method, data=None, resample=0) `  
参数说明：  
- size：指定新图片的大小；
- method：指定图片的变化方式，比如 Image.EXTENT 表示矩形变换；
- data：该参数用来给变换方式提供所需数据；
- resample：图像重采样滤波器，默认参数值为 PIL.Image.NEAREST。

使用示例如下：
```python
from PIL import Image
im = Image.open("C:/Users/···/c-net.png")
#设置图像大小250*250，并根据data的数据截取原图像的区域，生成新的图像
im_out=im.transform((250,250),Image.EXTENT,data=[0,0,30 + im.width//4,im.height//3])
im_out.show()
im_out.save("C:/Users/···/变换.png")
```
# Pillow图像降噪处理
由于成像设备、传输媒介等因素的影响，图像总会或多或少的存在一些不必要的干扰信息，我们将这些干扰信息统称为“噪声”，比如数字图像中常见的“椒盐噪声”，指的是图像会随机出现的一些白、黑色的像素点。图像噪声既影响了图像的质量，又妨碍人们的视觉观赏。因此，噪声处理是图像处理过程中必不可少的环节之一，我们把处理图像噪声的过程称为“图像降噪”。

随着数字图像技术的不断发展，图像降噪方法也日趋成熟，通过某些算法来构造滤波器是图像降噪的主要方式。滤波器能够有效抑制噪声的产生，并且不影响被处理图像的形状、大小以及原有的拓扑结构。

Pillow 通过 ImageFilter 类达到图像降噪的目的，该类中集成了不同种类的滤波器，通过调用它们从而实现图像的平滑、锐化、边界增强等图像降噪操作。常见的降噪滤波器如下表所示：

|名称|说明|
|:--:|:--|
|ImageFilter.BLUR|模糊滤波，即均值滤波|
|ImageFilter.CONTOUR|轮廓滤波，寻找图像轮廓信息|
|ImageFilter.DETAIL|细节滤波，使得图像显示更加精细|
|ImageFilter.FIND_EDGES|寻找边界滤波（找寻图像的边界信息）|
|ImageFilter.EMBOSS|浮雕滤波，以浮雕图的形式显示图像|
|ImageFilter.EDGE_ENHANCE|边界增强滤波|
|ImageFilter.EDGE_ENHANCE_MORE|深度边缘增强滤波|
|ImageFilter.SMOOTH|平滑滤波|
|ImageFilter.SMOOTH_MORE|深度平滑滤波|
|ImageFilter.SHARPEN|锐化滤波|
|ImageFilter.GaussianBlur()|高斯模糊|
|ImageFilter.UnsharpMask()|反锐化掩码滤波|
|ImageFilter.Kernel()|卷积核滤波|
|ImageFilter.MinFilter(size)|最小值滤波器，从 size 参数指定的区域中选择最小像素值，然后将其存储至输出图像中。|
|ImageFilter.MedianFilter(size)|中值滤波器，从 size 参数指定的区域中选择中值像素值，然后将其存储至输出图像中。|
|ImageFilter.MaxFilter(size)|最大值滤波器|
|ImageFilter.ModeFilter()|模式滤波|

从上述表格中选取几个方法进行示例演示，下面是等待处理的原始图像：
## 模糊处理
```python 
# 导入Image类和ImageFilter类
from PIL import Image,ImageFilter
im = Image.open("C:/Users/···/国宝.jpg")
#图像模糊处理
im_blur=im.filter(ImageFilter.BLUR)
im_blur.show()
im_blur.save("C:/Users/···/模糊.png")
```
## 轮廓图
```python
from PIL import Image,ImageFilter
im = Image.open("C:/Users/···/国宝.jpg")
#生成轮廓图
im2=im.filter(ImageFilter.CONTOUR)
im2.show()
im2.save("C:/Users/···/轮廓图.png")
```
## 边缘检测 
```python
from PIL import Image,ImageFilter
im = Image.open("C:/Users/···/国宝.jpg")
#边缘检测
im3=im.filter(ImageFilter.FIND_EDGES)
im3.show()
im3.save("C:/Users/···/边缘检测.png")
```
## 浮雕图
```python
from PIL import Image,ImageFilter
im = Image.open("C:/Users/···/国宝.jpg")
#浮雕图
im4=im.filter(ImageFilter.EMBOSS)
im4.show()
im4.save("C:/Users/···/浮雕图.png")
```
## 平滑图像
```python
#生成平滑图像
from PIL import Image,ImageFilter
im = Image.open("C:/Users/···/国宝.jpg")
#平滑图smooth
im5=im.filter(ImageFilter.SMOOTH)
im5.show()
im5.save("C:/Users/···/平滑图.png")
```

# Pillow图像颜色处理
Pillow 提供了颜色处理模块 ImageColor，该模块支持不同格式的颜色，比如 RGB 格式的颜色三元组、十六进制的颜色名称（#ff0000）以及颜色英文单词（"red"）。同时，它还可以将 CSS风格的颜色转换为 RGB 格式。
## 颜色命名
ImageColor 支持多种颜色模式的的命名（即使用固定的格式对颜值进行表示），比如我们熟知的 RGB 色彩模式，除此之外，还有 HSL （色调-饱和度-明度）、HSB （又称 HSV，色调-饱和度-亮度）色彩模式。下面对 HSL 做简单介绍：  
- H：即 Hue 色调，取值范围 0 -360，其中 0 表示“red”，120 表示 “green”，240 表示“blue”；
- S：即 Saturation 饱和度，代表色彩的纯度，取值 0~100%，其中 0 代表灰色（gry），100% 表示色光最饱和；
- L：即 Lightness 明度，取值为 0~100%，其中 0 表示“black”黑色，50% 表示正常颜色，100% 则表示白色。

下面使用 HSL 色彩模式表示红色，格式如下：  
`HSL(0,100%,50%)`  
此时的颜色为“纯红色”，等同于 RGB (255,0,0)。如果想了解有关 HSL/HSB 的更多知识，点击链接前往。  

ImageColor 模块比较简单，只提供了两个常用方法，分别是 getrgb() 和 getcolor() 函数。  
## getrgb()方法
顾名思义，该函数用来得到颜色的 RGB 值，语法格式如下：  
`PIL.ImageColor.getrgb(color)`  
使用示例如下：  
```python
from PIL import Image,ImageColor
# getrgb()方法
color1=ImageColor.getrgb("blue")
print(color1)
color2=ImageColor.getrgb('#DCDCDC')
print(color2)
#使用HSL模式红色
color3=ImageColor.getrgb('HSL(0,100%,50%)')
print(color3)
```
输出结果如下：
```
(0, 0, 255)
(220, 220, 220)
(255, 0, 0)
```
通过 new() 方法可以新建图像，此时也可以使用 ImageColor.getrgb()，如下所示：
```python
#使用new()绘制新的图像
im= Image.new("RGB", (200, 200), ImageColor.getrgb("#EEB4B4"))
im.save("C:/Users/···/xin.jpg")
```
## getcolor()
该方法与 getrgb() 类似，同样用来获取颜色值，不过它多了一个mode参数，因此该函数可以获取指定色彩模式的颜色值。语法格式如下：  
`PIL.ImageColor.getcolor(color, mode)`  
参数说明如下：  
- color：一个颜色名称，字符串格式，可以是颜色的英文单词，或者十六进制颜色名。如果是不支持的颜色，会报 ValueError 错误；
- mode：指定色彩模式，如果是不支持的模式，会报 KeyError 错误。

使用示例如下：  
```python
color4=ImageColor.getcolor('#EEA9B8','L')
print(color4)
color5=ImageColor.getcolor('yellow','RGBA')
print(color5)
```
输出结果：
```
191
(255, 255, 0, 255)
```
# Pillow为图片添加水印
为图片添加水印能够在一定程度上避免其他人滥用您的图片，这是保护图片版权的一种有效方式。因此，当您在微博、或者博客等一些公众平台分享图片的时候，建议您为自己的图片添加一个水印，来证明这张图片属于您。

我们知道，水印是附着在原图片上一段文字信息，因此添加水印的过程中会涉及两个问题：
- 第一、如何使文字信息附着在图片上；
- 第二、如何绘制文字信息。

只要解决了这两个问题就可以成功添加水印。`Pillow` 提供的`ImageDraw`和`ImageFont`模块成功解决了上述问题。

## ImageDraw
PIL.ImageDraw 模块提供了一系列的绘图方法，通过该模块可以创建一个新的图形，或者在现有的图像上再绘制一个图形，从而起到对原图注释和修饰的作用。

下面创建一个 ImageDraw 对象，并对该对象的使用方法做简单介绍：  
`draw = ImageDraw.Draw(im)`  
上述方法会返回一个 ImageDraw 对象，参数 im 表示 Image 对象。这里我们可以把 Image 对象理解成画布，通过调用 ImageDraw 对象的一些方法，实现了在画布上绘制出新的图形目的。ImageDraw 对象的常用方法如下表所示：
|方法|说明|
|:--:|:--|
|text|在图像上绘制文字|
|line|绘制直线、线段|
|eclipse|绘制椭圆形|
|rectangle|绘制矩形|
|polygon|绘制多边形|
> 表格中第一个方法 text() 需要与 ImageFont 模块一起使用，在下面会做详细介绍。

绘制矩形图的语法格式如下：  
`draw.rectangle(xy, fill=None, outline=None)`  
参数说明如下：  
- xy：元组参数值，以图像的左上角为坐标原点，表示矩形图的位置、图形大小的坐标序列，形如 ((x1,y1,x2,y2))；
- fill：矩形图的背景填充色；
- outline：矩形图的边框线条颜色。

下面看一组简单的示例：  
```python
from PIL import Image,ImageDraw
#创建 Image 对象，当做背景图
im = Image.new('RGB',(200,200),color='gray')
#创建 ImageDraw 对象
draw = ImageDraw.Draw(im)
#以左上角为原点，绘制矩形。元组坐标序列表示矩形的位置、大小；fill设置填充色为红色，outline设置边框线为黑色
draw.rectangle((50,100,100,150),fill=(255,0,0),outline=(0,0,0))
#查看原图片
im.show()
#保存图片
im.save("C:/Users/···/添加矩形图.png")
```

## ImageFont
PIL.ImagreFont 模块通过加载不同格式的字体文件，从而在图像上绘制出不同类型的文字，比如 TrueType 和 OpenType 类型的字体。

创建字体对象的语法格式如下：    
`font = ImageFont.truetype(font='字体文件路径', size=字体大小)`  
如果想要在图片上添加文本，还需要使用 ImageDraw.text() 方法，语法格式如下：  
`d.text((x,y), "text", font, fill)`  
参数说明如下：  
- (x,y)：图像左上角为坐标原点，(x,y) 表示添加文本的起始坐标位置；
- text：字符串格式，要添加的文本内容；
- font：ImageFont 对象；
- fill：文本填充颜色。

下面看一组使用示例，如下所示：
```python
from PIL import Image,ImageFont,ImageDraw
#打开图片，返回 Image对象
im = Image.open("C:/Users/···/c-net.png")
#创建画布对象
draw = ImageDraw.Draw(im)
#加载计算机本地字体文件
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',size=36)
#在原图像上添加文本
draw.text(xy=(80,50),text='C语言中文网',fill=(255,0,0),font=font)
im.show()
im.save("C:/Users/···/c.png")
```

## 添加图片水印
通过上述知识的学习，我们对ImageDraw和ImageFont模块有了大体的认识，并且也解决了如何给图片添加水印的两个关键问题。以下示例展示了为图片添加水印的详细过程，代码如下所示：
```python
from PIL import Image,ImageFont,ImageDraw
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',size=30)
def creating_watermark(im,text,font=font):
    #给水印添加透明度，因此需要转换图片的格式
    im_rgba=im.convert('RGBA')
    im_text_canvas=Image.new('RGBA',im_rgba.size,(255,255,255,0))
    print(im_rgba.size[0])
    draw = ImageDraw.Draw(im_text_canvas)
    #设置文本文字大小
    text_x_width,text_y_height = draw.textsize(text,font=font)
    print(text_x_width,text_y_height)
    text_xy = (im_rgba.size[0] - text_x_width, im_rgba.size[1] - text_y_height)
    print(text_xy)
    #设置文本颜色（绿色）和透明度（半透明）
    draw.text(text_xy,text,font=font,fill=(255,255,255,128))
    #将原图片与文字复合
    im_text=Image.alpha_composite(im_rgba,im_text_canvas)
    return  im_text
image = Image.open("C:/Users/···/c-net.png")
image.show()
image_water = creating_watermark(image,'@c语言中文网')
image_water.show()
image_water.save("C:/Users/···/c语言中文网.png")
```

# Pillow和ndarray数组
NumPy 是 Python 科学计算的基础数据包，它被大量的应用于机器学习领域，比如图像识别、自然语言处理、数据挖掘等。

ndarray 是 NumPy 中的数组类型，也称为 ndarray 数组，该数组可以与 Pillow 的 PIL.Image 对象实现相互转化。
## ndarray数组创建图像
下面通过 ndarray 数组构建一个 Image 对象，并将图像显示出来。示例如下：
```python
#导入相关的包
from PIL import Image
#使用numpy之前需要提前安装
import numpy as np
#创建 300*400的图像，3个颜色通道
array = np.zeros([300,400,3],dtype=np.uint8)
#rgb色彩模式
array[:,:200]=[255,0,0]
array[:,200:]=[255,255,0]
img = Image.fromarray(array)
img.show()
img.save("C:/Users/···/数组生成图像.png")
```
## 图像转化为ndarray数组
下面将图像以 ndarray 数组的形式进行输出，示例如下：
```python
from PIL import Image
import numpy as np
img = Image.open("C:/Users/···/大熊猫.png")
img.show()
#Image图像转换为ndarray数组
img_2 = np.array(img)
print(img_2)
#ndarray转换为Image图像
arr_img = Image.fromarray(img_2)
#显示图片
arr_img.show()
#保存图片
arr_img.save("C:/Users/···/arr_img.png")
```

# Pillow生成GIF动态图
GIF（Graphics Interchange Format，图形交换格式）是一种“位图”图像格式，它以.gif作为图像的扩展名。GIF 图片非常适合在互联网中使用，这是因为它采用了图像预压缩技术，该技术的应用，在一定程度上减少了图像传播、加载所消耗的时间。

与其他格式的图片相比，GIF 还有一项非常重要的应用，那就是生成动态图。我们知道，Pillow 能够处理多种图像格式，包括 GIF 格式，它可以将静态格式图片（png、jpg）合成为 GIF 动态图。 

> 注意：Pillow 总是以灰度模式（L）或调色板模式（P）来读取 GIF 文件。

下面看一组示例：如何使用 Pillow 生成 GiF 动态图。
```python
import os
import random
from PIL import Image
def png_to_gif(png_path,gif_name):
    """png合成gif图像"""
    frames = []
    # 返回文件夹内的所有静态图的列表
    png_files = os.listdir(png_path)
    # 打印返回的列表
    print(png_files)
    # 读取文件内的静态图
    for frame_id in range(1,len(png_files)+1):
        frame = Image.open(os.path.join(png_path,'image%d.png'%frame_id))
        frames.append(frame)
    # 以第一张图片作为开始，将后续5张图片合并成 gif 动态图
    # 参数说明：
    # save_all 保存图像;transparency 设置透明背景色;duration 单位毫秒，动画持续时间， 
    # loop=0 无限循环;disposal=2 恢复原背景颜色。参数详细说明，请参阅官方文档，网址见文章末尾处。
    frames[0].save(gif_name,save_all=True,append_images=frames[1:],transparency=0,duration=2000,loop=0,disposal=2)
#调用函数，传入对应的参数
png_to_gif("C:/Users/···/image",'C:/Users/···/t.gif')
```

# [实例](../example/pillow_ex.py)
实现一个关于图片的批量操作程序，要求完成以下功能：

1. 提示用户输入一个文件夹路径，表示存储图片的文件夹。  
2. 遍历文件夹中的所有图片文件（假设文件夹中只包含图片文件），并进行如下操作：  
    1. 将图片格式转换为.jpg格式。
    2. 修改图片的像素为512x512。


```python
import argparse
from PIL import Image

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='图片处理程序')
parser.add_argument('-f', '--format', help='将图片格式修改为指定格式')
parser.add_argument('-r', '--resize', help='将图片分辨率修改为指定大小')
parser.add_argument('input', help='输入文件路径')
parser.add_argument('output', nargs='?', help='输出文件路径')

# 解析命令行参数
args = parser.parse_args()

# 执行相应操作
try:
    img = Image.open(args.input)

    if args.format:
        # 修改图片格式
        output_format = args.format.lower()
        if args.output:
            output_file = args.output
        else:
            output_file = f"{args.input}.{output_format}"

        img.save(output_file, output_format)
        print(f"已成功将图片格式修改为.{output_format}，保存在：{output_file}")

    elif args.resize:
        # 修改分辨率
        width, height = map(int, args.resize.split('*'))
        output_file = args.output or f"{args.input}_resized.jpg"

        img_resized = img.resize((width, height))
        img_resized.save(output_file, "JPEG")
        print(f"已成功将图片分辨率修改为{width}x{height}，保存在：{output_file}")

    else:
        print("请提供有效的选项")
except FileNotFoundError:
    print("输入的文件路径不存在：", args.input)
except Exception as e:
    print("发生错误：", str(e))
```
在这个升级后的程序中，我们使用了argparse模块创建了一个命令行参数解析器，并定义了-f和-r两个选项以及相应的参数。通过使用argparse.ArgumentParser类创建解析器，并使用add_argument方法定义选项和参数的规则，使程序更具扩展性和可维护性。

现在，你可以通过指定命令行参数来执行不同的操作，如：
```python
python pillow_ex.py -f jpg input.png
python pillow_ex.py -r 512*512 input.jpg
```