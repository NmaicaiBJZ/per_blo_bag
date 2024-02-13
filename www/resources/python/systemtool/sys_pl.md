# sys模块介绍
## 简介

“sys”即“system”，“系统”之意。该模块提供了一些接口，用于访问 Python 解释器自身使用和维护的变量，同时模块中还提供了一部分函数，可以与解释器进行比较深度的交互。
## sys.argv
“argv”即“argument value”的简写，是一个列表对象，其中存储的是在命令行调用 Python 脚本时提供的“命令行参数”。

这个列表中的第一个参数是被调用的脚本名称，也就是说，调用 Python 解释器的“命令”（python）本身并没有被加入这个列表当中。这个地方要注意一下，因为这一点跟 C 程序的行为有所不同，C 程序读取命令行参数是从头开始的。

举例来说，在当前目录下新建一个 Python 文件sys_argv_example.py，其内容为：
```python
import sys
 print("The list of command line arguments:\n", sys.argv)
```
运行脚本：
```python
 $ python sys_argv_example.py arg1 arg2 arg3
 The list of command line arguments:
  ['example.py', 'arg1', 'arg2', 'arg3']
```
## sys.platform
windows上显示：
```python
 >>> import sys
 >>> sys.platform
 'win32'
 ```
 ## sys.byteorder
“byteorder”即“字节序”，指的是在计算机内部存储数据时，数据的低位字节存储在存储空间中的高位还是低位。

“小端存储”时，数据的低位也存储在存储空间的低位地址中，此时sys.byteorder的值为“little”。如果不注意，在按地址顺序打印内容的时候，可能会把小端存储的内容打错。当前大部分机器都是使用的小端存储。

而另外还存在一种存储顺序是“大端存储”，即数据的高位字节存储在存储空间的低位地址上，此时sys.byteorder的值为“big”。
## sys.executable
该属性是一个字符串，在正常情况下，其值是当前运行的 Python 解释器对应的可执行程序所在的绝对路径。
```python
>>> sys.executable
'C:\\Users\\wag23\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
```
## sys.modules
该属性是一个字典，包含的是各种已加载的模块的模块名到模块具体位置的映射。

通过手动修改这个字典，可以重新加载某些模块；但要注意，切记不要大意删除了一些基本的项，否则可能会导致 Python 整个儿无法运行。

关于其具体的值，由于内容过多，就不在此给出示例了，读者可以自行查看。
## sys.builtin_module_names
该属性是一个字符串元组，其中的元素均为当前所使用的的 Python 解释器内置的模块名称。

注意区别sys.modules和sys.builtin_module_names——前者的关键字（keys）列出的是导入的模块名，而后者则是解释器内置的模块名。

其值示例如下：
## sys.path
该属性是一个由字符串组成的列表，其中各个元素表示的是 Python **搜索模块的路径**；在程序启动期间被初始化。

其中第一个元素（也就是path[0]）的值是最初调用 Python 解释器的脚本所在的绝对路径；如果是在交互式环境下查看sys.path的值，就会得到一个空字符串。

命令行运行脚本（脚本代码见示例 sys_path_example.py）：

## sys.stdin
即 Python 的标准输入通道。通过改变这个属性为其他的类文件（file-like）对象，可以实现输入的重定向，也就是说可以用其他内容替换标准输入的内容。

所谓“标准输入”，实际上就是通过键盘输入的字符。

由于input()使用的就是标准输入流，因此通过修改sys.stdin的值，我们使用老朋友input()函数，也可以实现对文件内容的读取，程序运行效果如下：

## sys.err
与前面两个属性类似，只不过该属性标识的是标准错误，通常也是定向到屏幕的，可以粗糙地认为是一个输出错误信息的特殊的标准输出流。由于性质类似，因此不做演示。

此外，sys模块中还存在几个“私有”属性：sys.__stdin__，sys.__stdout__，sys.__stderr__。这几个属性中保存的就是最初定向的“标准输入”、“标准输出”和“标准错误”流。在适当的时侯，我们可以借助这三个属性将sys.stdin、sys.stdout和sys.err恢复为初始值。

## sys.getrecursionlimit() 和 sys.setrecursionlimit()
sys.getrecursionlimit()和sys.setrecursionlimit()是成对的。前者可以获取 Python 的最大递归数目，后者则可以设置最大递归数目。
## sys.getrefcount()
其返回值是 Python 中某个对象被引用的次数。
## 这个函数的作用与 C 语言中的sizeof运算符类似，返回的是作用对象所占用的字节数。

比如我们就可以看看一个整型对象1在内存中的大小：
```python
>>> sys.getsizeof(1)
28
```
##  sys.int_info 和 sys.float_info
这两个属性分别给出了 Python 中两个重要的数据类型的相关信息。

其中sys.int_info的值为：
```python
>>> sys.int_info
sys.int_info(bits_per_digit=30, sizeof_digit=4)
```
在文档中的解释为：

属性解释bits_per_digitnumber of bits held in each digit. Python integers are stored internally in base 2**int_info.bits_per_digitsizeof_digitsize in bytes of the C type used to represent a digit

指的是 Python 以 2 的`sys.int_info.bits_per_digit`次方为基来表示整数，也就是说它是“2 的`sys.int_info.bits_per_digit`次方进制”的数。这样的数每一个为都用 C 类中的 4 个字节来存储。

换句话说，每“进 1 位”（即整数值增加2 的`sys.int_info.bits_per_digit`次方），就需要多分配 4 个字节用以保存某个整数。

因此在`sys.getsizeof()`的示例中，我们可以看到2^30-1和2^30之间，虽然本身只差了 1，但是所占的字节后者却比前者多了 4。

而sys.float_info的值则是：
```python
>>> sys.float_info
sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)
```
## sys.ps1与sys.ps2
每次打开 Python 的交互式界面，我们都会看到一个提示符`>>>`。

这两个属性中，`sys.ps1`代表的是一级提示符，也就是进入 Python 交互界面之后就会出现的那一个`>>>`；而第二个`sys.ps2`则是二级提示符，是在同一级内容没有输入完，换行之后新行行首的提示符`...`。当然，两个属性都是字符串。

