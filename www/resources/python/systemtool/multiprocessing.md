# multiprocessing 多进程
Python中的多进程是通过multiprocessing包来实现的，和多线程的threading.Thread差不多，  
它可以利用multiprocessing.Process对象来创建一个进程对象。

示例一：
```py
from multiprocessing import  Process
def fun1(name):
    print('测试%s多进程' %name)
if __name__ == '__main__':
    process_list = []
    for i in range(5):  #开启5个子进程执行fun1函数
        p = Process(target=fun1,args=('Python',)) #实例化进程对象
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()
    print('结束测试')
```
结果：
```py
测试Python多进程
测试Python多进程
测试Python多进程
测试Python多进程
测试Python多进程
结束测试
```


上面的代码开启了5个子进程去执行函数  
进程是python中最小的资源分配单元，也就是进程中间的数据，内存是不共享的，每启动一个进程，都要独立分配资源和拷贝访问的数据，所以进程的启动和销毁的代价是比较大了，所以在实际中使用多进程，要根据服务器的配置来设定。

示例二.通过继承的方法来实现
```py
from multiprocessing import  Process
class MyProcess(Process): #继承Process类
    def __init__(self,name):
        super(MyProcess,self).__init__()
        self.name = name
    def run(self):
        print('测试%s多进程' % self.name)
if __name__ == '__main__':
    process_list = []
    for i in range(5):  #开启5个子进程执行fun1函数
        p = MyProcess('Python') #实例化进程对象
        p.start()
        process_list.append(p)
    for i in process_list:
        p.join()
    print('结束测试')
```
效果和示例一一摸一样

## Process类的方法
### 构造方法：
`Process([group [, target [, name [, args [, kwargs]]]]])`

- group: 线程组 
- target: 要执行的方法
- name: 进程名
- args/kwargs: 要传入方法的参数

### 实例方法：
- `is_alive()`：返回进程是否在运行,bool类型。
- `join([timeout])`：阻塞当前上下文环境的进程程，直到调用此方法的进程终止或到达指定的timeout（可选参数）。
- `start()`：进程准备就绪，等待CPU调度
- `run()`：strat()调用run方法，如果实例进程时未制定传入target，这star执行t默认run()方法。
- `terminate()`：不管任务是否完成，立即停止工作进程

属性：
　　daemon：和线程的setDeamon功能一样
　　name：进程名字
　　pid：进程号

## 进程间的通讯
https://zhuanlan.zhihu.com/p/64702600