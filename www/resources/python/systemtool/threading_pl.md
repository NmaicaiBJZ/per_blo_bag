# Python 多线程
多线程类似于同时执行多个不同程序，多线程运行有如下优点：

使用线程可以把占据长时间的程序中的任务放到后台去处理。  
用户界面可以更加吸引人，这样比如用户点击了一个按钮去触发某些事件的处理，可以弹出一个进度条来显示处理的进度  
程序的运行速度可能加快  
在一些等待的任务实现上如用户输入、文件读写和网络收发数据等，线程就比较有用了。在这种情况下我们可以释放一些珍贵的资源如内存占用等等。  
线程在执行过程中与进程还是有区别的。每个独立的进程有一个程序运行的入口、顺序执行序列和程序的出口。但是线程不能够独立执行，必须依存在应用程序中，由应用程序提供多个线程执行控制。  

每个线程都有他自己的一组CPU寄存器，称为线程的上下文，该上下文反映了线程上次运行该线程的CPU寄存器的状态。

指令指针和堆栈指针寄存器是线程上下文中两个最重要的寄存器，线程总是在进程得到上下文中运行的，这些地址都用于标志拥有线程的进程地址空间中的内存。

线程可以被抢占（中断）。  
在其他线程正在运行时，线程可以暂时搁置（也称为睡眠） -- 这就是线程的退让。  
## 全局解释器锁（GIL）
Python的多线程，只有用于I/O密集型程序时效率才会有明显的提高。

原因如下：

Python代码的执行是由Python虚拟机进行控制。它在主循环中同时只能有一个控制线程在执行，意思就是Python解释器中可以运行多个线程，但是在执行的只有一个线程，其他的处于等待状态。

这些线程执行是有全局解释器锁（GIL）控制，它来保证同时只有一个线程在运行。在多线程运行环境中，Python虚拟机执行方式如下：

1. 设置GIL
2. 切换进线程
3. 执行下面操作之一
4. 运行指定数量的字节码指令
5. 线程主动让出控制权
6. 切换出线程（线程处于睡眠状态）
7. 解锁GIL
8. 进入1步骤
> 注意：Python运行计算密集型的多线程程序时，更倾向于让线程在整个时间片内始终占据GIL，而I/O秘籍型的多线程程序在I/O被调用前会释放GIL，以允许其他线程在I/O执行的时候运行。
## 线程模块
Python通过两个标准库thread和threading提供对线程的支持。thread提供了低级别的、原始的线程以及一个简单的锁。

threading 模块提供的其他方法：

- threading.currentThread(): 返回当前的线程变量。   
- threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。  
- threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。  

除了使用方法外，threading 模块的Thread 类是主要的执行对象。Thread类提供了以下方法:  

- run(): 用以表示线程活动的方法。
- start():启动线程活动。
- join([time]): 等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
- isAlive(): 返回线程是否活动的。
- getName(): 返回线程名。
- setName(): 设置线程名。

可调用对象（函数，类的实例方法）使用多线程:
![步骤](../../imagebag/threading.webp)
## 使用Threading模块创建线程
创建Thread实例，传递给他一个函数：
```python
from threading import Thread
from time import sleep, ctime
def func(name, sec):
    print('---开始---', name, '时间', ctime())
    sleep(sec)
    print('***结束***', name, '时间', ctime())

# 创建 Thread 实例
t1 = Thread(target=func, args=('第一个线程', 1))
t2 = Thread(target=func, args=('第二个线程', 2))

# 启动线程运行
t1.start()
t2.start()

# 等待所有线程执行完毕
t1.join()  # join() 等待线程终止，要不然一直挂起，意思就是等待t1线程执行完后在才能往下执行
t2.join()
```
start() 是方法用来启动线程的执行。

join() 方法是一种自旋锁，它用来等待线程终止。也可以提供超时的时间，当线程运行达到超时时间后结束线程，如join(500)，500毫秒后结束线程运行。  
> 注意：如果当你的主线程还有其他事情要做，而不是等待这些线程完成，就可以不调用join()。join()方法只有在你需要等待线程完成然后在做其他事情的时候才是有用的。

派生Thread 的子类，传递给他一个可调用对象:
```python
from threading import Thread
from time import sleep, ctime
# 创建 Thread 的子类
class MyThread(Thread):
    def __init__(self, func, args):
        '''
        :param func: 可调用的对象
        :param args: 可调用对象的参数
        '''
        Thread.__init__(self)   # 不要忘记调用Thread的初始化方法
        self.func = func
        self.args = args
        # self.result = None
    def run(self):
        self.func(*self.args)

    # def getResult(self):      # 如果希望func有返回参数，可使用
    #     return self.result

def func(name, sec):
    print('---开始---', name, '时间', ctime())
    sleep(sec)
    print('***结束***', name, '时间', ctime())
    # return sec                # 返回结果

def main():         
    # 创建 Thread 实例
    t1 = MyThread(func, (1, 1))     # 创建程序时调用__init__初始化方法
    t2 = MyThread(func, (2, 2))
    # 启动线程运行
    t1.start()      # 会运行run方法
    t2.start()
    # 等待所有线程执行完毕
    t1.join()
    t2.join()

    # print(t1.getResult())     # 打印需要返回值

if __name__ == '__main__':
    main()
```


## Lock 同步锁 (原语锁)
示例：加锁 与 解锁
```python
import threading

# 创建一个锁对象
lock = threading.Lock()
# 获得锁，加锁
lock.acquire()

....

# 释放锁，解锁
lock.release()
```
当我们通过 lock.acquire() 获得锁后线程程将一直执行不会中断，直到该线程 lock.release( )释放锁后线程才有可能被释放(注意：锁被释放后线程不一定会释放)。

示例：锁的运用
```python
import time
import threading

# 生成一个锁对象
lock = threading.Lock()
def func():
    global num  # 全局变量
    # lock.acquire()  # 获得锁，加锁
    num1 = num
    time.sleep(0.1)
    num = num1 - 1
    # lock.release()  # 释放锁，解锁
    time.sleep(2)
num = 100
l = []
for i in range(100):  # 开启100个线程
    t = threading.Thread(target=func, args=())
    t.start()
    l.append(t)
# 等待线程运行结束
for i in l:
    i.join()

print(num)
```
> 注意：上面代码先将lock.acquire()和lock.release()行注释掉表示不使用锁，取消lock.acquire()和lock.release()行的注释表示使用锁。

Lock 与GIL(全局解释器锁）存在区别。

我们需要知道 Lock 锁的目的，它是为了保护共享的数据，同时刻只能有一个线程来修改共享的数据，而保护不同的数据需要使用不同的锁。

GIL用于限制一个进程中同一时刻只有一个线程被CPU调度，GIL的级别比Lock高，GIL是解释器级别。

GIL与Lock同时存在，程序执行如下：
1. 同时存在两个线程：线程A，线程B
2. 线程A 抢占到GIL，进入CPU执行，并加了Lock，但为执行完毕，线程被释放
3. 线程B 抢占到GIL，进入CPU执行，执行时发现数据被线程A Lock，于是线程B被阻塞
4. 线程B的GIL被夺走，有可能线程A拿到GIL，执行完操作、解锁，并释放GIL
5. 线程B再次拿到GIL，才可以正常执行

多线程最怕的是遇到死锁，两个或两个以上的线程在执行时，因争夺资源被相互锁住而相互等待。  
示例：互锁造成死锁
```python
import threading
# 生成一个锁对象
lock1 = threading.Lock()
lock2 = threading.Lock()
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self) -> None:
        self.fun_A()
        self.fun_B()
    def fun_A(self):
        lock1.acquire()
        print('A_1 加锁', end='\t')
        lock2.acquire()
        print('A-2 加锁', end='\t')
        time.sleep(0.1)
        lock2.release()
        print('A-2 释放', end='\t')
        lock1.release()
        print('A-1 释放')
    def fun_B(self):
        lock2.acquire()
        print('B-1 加锁', end='\t')
        lock1.acquire()
        print('B-2 加锁', end='\t')
        time.sleep(0.1)
        lock1.release()
        print('B-1 释放', end='\t')
        lock2.release()
        print('B-2 释放')

if __name__ == '__main__':
# 需要四个以上线程，才会出现死锁现象
    t1 = MyThread()
    t2 = MyThread()
    t1.start()
    t2.start()
```
如上，如果两个锁同时被多个线程运行，就有可能出现死锁，如果没出现死锁，就多运行几遍就会出现死锁现象。上面程序死锁为偶现性，这种bug也是最难找的。
##  重入锁(递归锁) threading.RLock()
为了支持同一个线程中多次请求同一资源，Python 提供了可重入锁(RLock)。这个RLock内部维护着一个锁(Lock)和一个计数器(counter)变量，counter 记录了acquire 的次数，从而使得资源可以被多次acquire。直到一个线程所有 acquire都被release(计数器counter变为0)，其他的线程才能获得资源。
```python
import time
import threading
# 生成一个递归对象
Rlock = threading.RLock()
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self) -> None:
        self.fun_A()
        self.fun_B()
    def fun_A(self):
        Rlock.acquire()
        print('A加锁1', end='\t')
        Rlock.acquire()
        print('A加锁2', end='\t')
        time.sleep(0.2)
        Rlock.release()
        print('A释放1', end='\t')
        Rlock.release()
        print('A释放2')
    def fun_B(self):
        Rlock.acquire()
        print('B加锁1', end='\t')
        Rlock.acquire()
        print('B加锁2', end='\t')
        time.sleep(3)
        Rlock.release()
        print('B释放1', end='\t')
        Rlock.release()
        print('B释放2')

if __name__ == '__main__':
    t1 = MyThread()
    t2 = MyThread()
    t1.start()
    t2.start()
```
注意观察程序的运行，当运行到程序B时，即使B休眠了3秒也不会切换线程。

使用重入锁时，counter 没有变为0(所有的acquire没有被释放掉)，即使遇到长时间的io操作也不会切换线程。
## 信号量(Semaphore)
信号量是一个内部数据，它有一个内置的计数器，它标明当前的共享资源可以有多少线程同时读取。

示例：定义一个只能同时执行5个线程的信号量。  
`semaphore = threading.Semaphore(5)  # 创建信号量对象，5个线程并发`

当线程需要读取关联信号量的共享资源时，需调用acquire()，这时信号量的计数器会-1。  
`semaphore.acquire() # 获取共享资源，信号量计数器-1`

在线程不需要共享资源时，需释放信号release()，这时信号量的计数器会+1，在信号量等待队列中排在最前面的线程会拿到共享资源的权限。。
`semaphore.release()  # 释放共享资源，信号量计数器+1`

信号量控制规则：当计数器大于0时，那么可以为线程分配资源权限；当计数器小于0时，未获得权限的线程会被挂起，直到其他线程释放资源。

示例1: 信号量运行3个线程并行
```python
import time
import threading
import random
# 创建信号量对象，信号量设置为3，需要有3个线程才启动
semaphore = threading.Semaphore(3)
def func():
    if semaphore.acquire():  # 获取信号 -1
        print(threading.currentThread().getName() + '获得信号量')
        time.sleep(random.randint(1, 5))
        semaphore.release()  # 释放信号 +1

for i in range(10):
    t1 = threading.Thread(target=func)
    t1.start()
```
注意观察程序运行，开始只有3个线程获得了资源的权限，后面当释放几个资源时就有几个获得资源权限

示例2：运用信号量进行线程同步
```python
import threading
import time
import random
# 同步两个不同线程，信号量被初始化0
semaphore = threading.Semaphore(0)
def consumer():
    print("-----等待producer运行------")
    semaphore.acquire()  # 获取资源，信号量为0被挂起，等待信号量释放
    print("----consumer 结束----- 编号: %s" % item )
def producer():
    global item  # 全局变量
    time.sleep(3)
    item = random.randint(0, 100)  # 随机编号
    print("producer运行编号: %s" % item)
    semaphore.release()

if __name__ == "__main__":
    for i in range(0, 4):
        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print("程序终止")
```
信号量被初始化为0，目的是同步两个或多个线程。线程必须并行运行，所以需要信号量同步。这种运用场景有时会用到，比较难理解，多运行示例仔细观察打印结果。

拓展：

信号量的一个特殊用法是互斥量。互斥量是初始值为1的信号量，可以实现数据、资源的互斥访问。

信号量在在多线程的编程语言中应用很广，他也有可能造成死锁的情况。例如，有一个线程t1，先等待信号量s1，然后等待信号量s2，而线程t2会先等待信号量s2，然后再等待信号量s1，这样就会发生死锁，导致t1等待s2，但是t2在等待s1。
## Condition 条件变量
Condition 条件变量通常与一个锁相关联。需要在多个Condition 条件中共享一个锁时，可以传递一个Lock/RLock实例给构造方法，否则他将自己产生一个RLock实例。

定义条件变量锁实例  
`condition = threading.Condition()`  

比较难理解，先看看Condition()下的方法。
- acquire() 获得锁(线程锁)
- release() 释放锁
- wait(timeout) 挂起线程timeout秒(为None时时间无限)，直到收到notify通知或者超时才会被唤醒继续运行。必须在获得Lock下运行。
- notify(n=1) 通知挂起的线程开始运行，默认通知正在等待该condition的线程，可同时唤醒n个。必须在获得Lock下运行。
- notifyAll() 通知所有被挂起的线程开始运行。必须在获得Lock下运行。

示例1：生产与消费，线程produce生产产品当产品生产成功后通知线程B使用产品，线程consume使用完产品后通知线程produce继续生产产品。
```python
import threading
import time
# 商品
product = None
# 条件变量对象
con = threading.Condition()
# 生产方法
def produce():
    global product  # 全局变量产品
    if con.acquire():
        while True:
            print('---执行，produce--')
            if product is None:
                product = '袜子'
                print('---生产产品:%s---' % product)
                # 通知消费者，商品已经生产
                con.notify()  # 唤醒消费线程
            # 等待通知
            con.wait()
            time.sleep(2)

# 消费方法
def consume():
    global product
    if con.acquire():
        while True:
            print('***执行，consume***')
            if product is not None:
                print('***卖出产品:%s***' % product)
                product = None
                # 通知生产者，商品已经没了
                con.notify()
            # 等待通知
            con.wait()
            time.sleep(2)

if __name__=='__main__':
    t1 = threading.Thread(target=consume)
    t1.start()
    t2 = threading.Thread(target=produce)
    t2.start()
```
示例2：生产商品数量达到一定条件后被消费
```python
import threading
import time
num = 0
condition = threading.Condition()

class Producer(threading.Thread):
    """ 生产者 ，生产商品，5个后等待消费"""
    def run(self):
        global num
        # 获取锁
        condition.acquire()
        while True:
            num += 1
            print('生产了1个，现在有{0}个'.format(num))
            time.sleep(1)
            if num >= 5:
                print('已达到5个，停止生产')
                # 唤醒消费者费线程
                condition.notify()
                # 等待-释放锁 或者 被唤醒-获取锁
                condition.wait()

class Customer(threading.Thread):
    """ 消费者 抢购商品，每人初始10元，商品单价1元"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 每人初始10块钱
        self.money = 10
    def run(self):
        global num
        while self.money > 0:
            condition.acquire()
            if num <= 0:
                print('没货了，{0}通知生产者'.format(threading.current_thread().name))
                condition.notify()
                condition.wait()
            self.money -= 1
            num -= 1
            print('{0}消费了1个, 剩余{1}个'.format(threading.current_thread().name, num))
            condition.release()
            time.sleep(1)
        print('{0}没钱了-停止消费'.format(threading.current_thread().name))

if __name__ == '__main__':
    p = Producer(daemon=True)
    c1 = Customer(name='Customer-1')
    c2 = Customer(name='Customer-2')
    p.start()
    c1.start()
    c2.start()
```
两个示例差不多，只是实现方式不同，注意观察输出，理解程序运行规则。

release() 和 wait() 都有释放锁的作用，不同在于wait() 后，该子线程就在那里挂起等待，要继续执行，就需要接收到 notify() 或者 notifyAll() 来唤醒线程，而 release() 该线程还能继续执行。
## Event 事件锁对象
用于线程间通信，即程序中的其一个线程需要通过判断某个线程的状态来确定自己下一步的操作，就用到了event()对象。event()对象有个状态值，他的默认值为 Flase，即遇到 event() 对象就阻塞线程的执行。

定义Event 事件锁实例  
`event = threading.Event()`

Event对象的方法
- wait(timeout=None) 挂起线程timeout秒(None时间无限)，直到超时或收到event()信号开关为True时才唤醒程序。
- set() Even状态值设为True
- clear() Even状态值设为 False
- isSet() 返回Even对象的状态值。

示例: func等待connect启动服务
```python
import threading
event = threading.Event()
def func():
    print('等待服务响应...')
    event.wait()  # 等待事件发生
    print('连接到服务')
def connect():
    print('成功启动服务')
    event.set()
t1 = threading.Thread(target=func, args=())
t2 = threading.Thread(target=connect, args=())
t1.start()
t2.start()
```
观察结果会发现，t1线程运行的func函数需要等到connect函数运行event.set()后才继续执行之后的操作。
## Barrie 障碍锁
也可以叫屏障或者栅栏，可以想象成路障、道闸。当线程达到设定的数值时放开道闸允许继续运行。

创建Barrier障碍锁  
`barrier=threading.Barrier(parties, action=None, timeout=None)` 

参数：
- parties 参与线程的数量
- action 全部线程被释放时可被其中一条线程调用的可调用对象
- timeout 调用wait方法时未指定时超时的默认值

Barrier实例的方法
- wait(timeout=None) 等待通过栅栏，返回值是一个0到parties-1之间的整数， 每个线程返- 回不同。如果wait方法设置了超时，并超时发送，栅栏将处于broken状态。
- reset() 重置障碍，返回默认的 False 状态，即重新开始阻塞线程。
- abort() 将障碍置为断开状态，这将导致已调用wait()和之后调用wait()引发BrokenBarrierError异常。

Barrier实例的属性
- partier 通过障碍的线程数
- n_waiting 当前在屏障中等待的线程数
- broken 布尔值，表明barrier是否broken。

示例:
```python
import threading
def work(barrier):
    print("n_waiting = {}".format(barrier.n_waiting))  # 等待的线程数
    bid = barrier.wait()  # 参与者的id，返回0到线程数减1的数值
    print("障碍后运行 {}".format(bid))  # 障碍之后
barrier = threading.Barrier(3)  # 3个参与者，每3个开闸放行
for x in range(6):  # 这里启动线程只能是3的倍数,你可以试5
    threading.Thread(target=work, args=(barrier,)).start()
```
注意：当我们设置Barrier的放行的线程数时，我们启动的线程只能是他的倍数，不然会有线程一直陷入等待中。

怎么解决这个问题，我们需要在wait加入timeout参数，如下示例。

示例2: 解决线程不是Barrier的倍数问题
```python
import threading
def work(barrier):
    bid = None
    print("n_waiting = {}".format(barrier.n_waiting))  # 等待的线程数
    try:
        # 设置超时时间，线程达不到数量会抛出异常
        bid = barrier.wait(1)  # 设置线程超时时间
        print("障碍后运行 {}".format(bid))  # 障碍之后
    except threading.BrokenBarrierError:  # 接收超时的异常
        barrier.abort()  # 取消屏障
        print("打破障碍运行 {}".format(threading.current_thread()))
barrier = threading.Barrier(3)  # 3个参与者，每3个开闸放行
for x in range(5):  # 5个线程，剩余2个会抛出超时异常
    threading.Event().wait(0.1)
    threading.Thread(target=work, args=(barrier,)).start()
```
## threading 使用 Queue 保持线程同步
Python的Queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

FIFO队列，先进先出
```python
q = queue.Queue(10)  # FIFO 队列，最多放入10个项目
q.put(123) # 队列中存入项目123
```

LIFO队列，后进先出，如同栈
```python
q = queue.LifoQueue()   # LIFO 队列，项目数无限 
q.put(123) # 队列中存入项目123
```

Priority队列，对着中的数据始终保持排序，优先检索最低值。 通常使用 (优先序号, 数据)形式存储数据。不带需要默认对其值进行排序。  
注意：Priority队列因为是顺序的，存储的数据必须是要能排序，即相同类型数据
```python
q = queue.PriorityQueue(10) # Priority 队列，最多放入10个项目
q.put((1,'a')) # 队列中存入项目(1,'a')
```
注意: 创建队列时会指定队列中最多存储项目的个数，就是设定一个非常大的值也比无限制好。

Queue模块中的常用方法:
- Queue.qsize() 返回队列的大小
- Queue.empty() 如果队列为空，返回True,反之False
- Queue.full() 如果队列满了，返回True,反之False
- Queue.full 与 maxsize 大小对应
- Queue.get([block[, timeout]])从队列中删除并返回一个item。  
    block=True, timeout=None 在必要时阻塞，直到有可用数据为止，timeout 为阻止的时间，超时抛出Empty异常。  
    block=False 立即获取队列中的可用数据，否则抛出Empty异常。
- Queue.get_nowait() 立即获取队列中的数据，同get(False)。
- Queue.put(item, block=True, timeout=None) 写入队列  
    block=True, timeout=None 在必要时阻塞，直到有空位可用，timeout 为阻止的时间，超时抛出Full异常。  
    block=False 立即将item放入队列，队列已满引发Full异常。
- Queue.put_nowait(item) 立即放入队列，同put(item,False)
- Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
- Queue.join() 立即获取队列中的数据，同get(False)。
> 注意：join() 与 task_done() 是套组合拳，有使用 join() 必须在任务结束后执行 task_done() 通知队列。

示例：生产 消费模式

```python
import threading, time
import queue
# 最多存入10个
q = queue.PriorityQueue(10)
def producer(name):
    ''' 生产者 '''
    count = 1
    while True:
        # 　生产袜子
        q.put("袜子 %s" % count)  # 将生产的袜子方法队列
        print(name, "---生产了袜子", count)
        count += 1
        time.sleep(0.2)
def consumer(name):
    ''' 消费者 '''
    while True:
        print("%s ***卖掉了[%s]" % (name, q.get()))  # 消费生产的袜子
        time.sleep(1)
        q.task_done()  # 告知这个任务执行完了

# 生产线程
z = threading.Thread(target=producer, args=("张三",))
# 消费线程
l = threading.Thread(target=consumer, args=("李四",))
w = threading.Thread(target=consumer, args=("王五",))
# 执行线程
z.start()
l.start()
w.start()
```