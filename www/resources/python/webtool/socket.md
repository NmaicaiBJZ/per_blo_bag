# socket
Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口。  
在设计模式中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。  
所以，我们无需深入理解tcp/udp协议，socket已经为我们封装好了，我们只需要遵循socket的规定去编程，写出的程序自然就是遵循tcp/udp标准的。

套接字的工作流程

<img src="../../imagebag/socket_jichu.png" height="500px" />

## socket()函数

`socket.socket([family[, type[, proto]]])`

参数：

- `family`
    - `AF_UNIX`: UNIX网域协议
    - `AF_INET`: IPv4网域协议，如TCP与UDP
- `type` ：套接字类型
    - `SOCK_STREAM` :（使用在TCP中）
    - `SOCK_DGRAM` :（使用在UDP中）
    - `SOCK_RAW` :（使用在IP中）
    - `SOCK_SEQPACKET` :（列表连接模式）。
- `protocol` ：只使用在family等于AF_INET或type等于SOCK_RAW的时候。  
    `protocol` 是一个常数，用于辨识所使用的协议 种类。默认值是0，表示适用于所有socket类型。

## socket 对象方法
- `accept()`：接收一个新连接，并且返回两个数值（conn、address）。conn是一个新的socket对象，用于在该连接上传输数据；address是此socket使用的地址。

- `bind(address)`：将socket连接到address地址，地址的格式为(hostname, port)。

- `close()`：关闭此socket。

- `connect(address)`：连接到一个远程的socket，其地址为address。

- `makefile([mode [, bufsize]])` ：创建一个与socket有关的文件对象，参数mode和bufsize与内置函数open()相同。

- `getpeername()`：返回socket所连接的地址，地址的格式为(ipaddr, port)。

- `getsockname()`：返回socket本身的地址，地址的格式为(ipaddr, port)。

- `listen(backlog)`：打开连接监听，参数backlog为最大可等候的连接数目。

- `recv(bufsize [, flags])` ：从socket接收数据，返回值是字符串数据。参数bufszie表示最大的可接收数据量；参数flags用来指定数据的相关信息，默认值为0。

- `recvfrom(bufsize [, flags])` ：从socket接收数据。返回值是成对的(string, address)，其中，string代表接收的字符串数据，address则是socket传输数据的地址。参数bufszie表示最大的可接收数据量；参数flags用来指定数据的相关信息，默认值为0。

- `send(string [, flags])`：将数据以字符串类型传输到socket。参数flags与recv()方法相同。

- `sendto(string [, flags], address)`：将数据传输到远程的socket。参数flags与recv()方法相同，参数address是该socket的地址。

- `shutdown(how)`：关闭联机的一端或两端。若how等于0，则关闭接收端；若how等于1，则关闭传输端；若how等于2，则同时关闭接收端与传输端。

##  setSocketOpt 详细
### 功能描述：

获取或者设置与某个 `套接字` 关联的选项。选项可能存在于多层协议中，它们总会出现在最上面的套接字层。当操作套接字选项时，选项位于的层和选项的名称必须给出。为了操作套接字层的选项，应该将层的值指定为 `SOL_SOCKET` 。  

为了操作其它层的选项，控制选项的合适协议号必须给出。例如，为了表示一个选项由TCP协议解析，层应该设定为协议号TCP。

### 用法：

`setsockopt(level,optname,value)`

### 参数：  
- `level` 定义了哪个选项将被使用。通常情况下是 `SOL_SOCKET` ，意思是正在使用的socket选项。它还可以通过设置一个特殊协议号码来设置协议选项，然而对于一个给定的操作系统，大多数协议选项都是明确的，所以为了简便，它们很少用于为移动设备设计的应用程序。
- optname：optname参数提供使用的特殊选项。关于可用选项的设置，会因为操作系统的不同而有少许不同。

### 参数详细说明：
level指定控制套接字的层次.可以取三种值:

1. SOL_SOCKET:通用套接字选项.
2. IPPROTO_IP:IP选项.
3. IPPROTO_TCP:TCP选项.　

套接字 `SOL_SOCKET`

|选项名称|说明|数据类型|
|:--|:--|:--|
|SO_BROADCAST|允许广播地址发送和接收信息包。只<br>对UDP有效。如何发送和接收广播信<br>息包|int|
|SO_DEBUG|允许调试|int|
|SO_DONTROUTE|禁止通过路由器和网关往外发送信息<br>包。这主要是为了安全而用在以太网<br>上UDP通信的一种方法。不管目的地<br>址使用什么IP地址，都可以防止数据<br>离开本地网络|int|
|SO_ERROR|获得套接字错误|int|
|SO_KEEPALIVE|可以使TCP通信的信息包保持连续<br>性。这些信息包可以在没有信息传输<br>的时候，使通信的双方确定连接是保<br>持的|int|
|SO_LINGER|延迟关闭连接|struct linger|
|SO_OOBINLINE|可以把收到的不正常数据看成是正常<br>的数据，也就是说会通过一个标准的<br>对recvO的调用来接收这些数|int|
|SO_RCVBUF|接收缓冲区大小|int|
|SO_SNDBUF|发送缓冲区大小|int|
|SO_RCVLOWAT|接收缓冲区下限|int|
|SO_SNDLOWAT|发送缓冲区下限|int|
|SO_RCVTIMEO|接收超时|struct timeval|
|SO_SNDTIMEO|发送超时|struct timeval|
|SO_REUSEADDR|当socket关闭后，本地端用于该socket<br>的端口号立刻就可以被重用。通常来<br>说，只有经过系统定义一段时间后，<br>才能被重用。|int|
|SO_TYPE|获得套接字类型|int|
|SO_BSDCOMPAT|与BSD系统兼容|int|
|SO_DONTLINGER|调用closesocket后不强制关闭|bool|
|SO_BINDTODEVICE|可以使socket只在某个特殊的网络接<br>口(网卡)有效。也许不能是移动便<br>携设备<br>|一个字符串给出设备的名称或<br>者一个空字符串返回默认值|

套接字 `IPPROTO_IP`

|选项名称|说明|数据类型|
|:--|:--|:--|
|IP_HDRINCL|在数据包中包含IP首部|int|
|IP_OPTINOS|IP首部选项|int|
|IP_TOS|服务类型||
|IP_TTL|生存时间|int|

套接字 `IPPRO_TCP`

|选项名称|说明|数据类型|
|:--|:--|:--|
|TCP_MAXSEG|TCP最大数据段的大小|int|
|TCP_NODELAY|不使用Nagle算法|int|

`SO_RCVBUF` 和 `SO_SNDBUF` 每个套接口都有一个发送缓冲区和一个接收缓冲区，使用这两个套接口选项可以改变缺省缓冲区大小。

### 具体写法
`S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) `

这里value设置为1，表示将 `SO_REUSEADDR` 标记为 `TRUE` ，  
操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。

### 返回说明：  
- 成功执行时，返回0。失败返回-1，errno被设为以下的某个值  
- EBADF：sock不是有效的文件描述词
- EFAULT：optval指向的内存并非有效的进程空间
- EINVAL：在调用setsockopt()时，optlen无效
- ENOPROTOOPT：指定的协议层不能识别选项
- ENOTSOCK：sock描述的不是套接字

