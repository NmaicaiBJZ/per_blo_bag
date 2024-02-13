# 正则表达式
匹配单个字符:

|字符|功能|
|:--|:--|
|`.`|匹配任意字符，除了换行符 `\n` ，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。|
|`[...]`|用来表示一组字符,单独列出：[amk] 匹配 'a'，'m'或'k'|
|`[^...]`|不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。|
|`\w`|匹配字母数字及下划线|
|`\W`|匹配非字母数字及下划线|
|`\s`|匹配任意空白字符，等价于 [ \t\n\r\f]。|
|`\S`|匹配任意非空字符|
|`\d`|匹配任意数字，等价于 [0-9].|
|`\D`|匹配任意非数字|
|`\A`|匹配字符串开始|
|`\Z`|匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。|
|`\z`|匹配字符串结束|
|`\G`|匹配最后匹配完成的位置。|
|`\b`|匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹|配 "verb" 中的 'er'。
|`\B`|匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。|
|`\n`, `\t`, 等.|匹配一个换行符。匹配一个制表符。等|

匹配多个字符：
|字符|功能|
|:--|:--|
|`*`|匹配*前一个字符*出现 **0次** 或者 **无限次**|
|`+`|匹配*前一个字符*出现 **1次** 或者 **无限次**|
|`?`|匹配*前一个字符*出现 **1次** 或者 **0次**,也可用做非贪婪方式|
|`{m}`|匹配*前一个字符*出现 **m次**|
|`{m,}`|匹配 m 个前面表达式。
|`{m,n}`|匹配*前一个字符*出现 **m次到n次**|

分组
|字符|功能|
|:--|:--|
|`a\|b`|匹配a或b|
|`(ab)`|将括号中的字符作为一个**分组**,group可以单独拿出来|
|`\1...\9`|匹配第n个分组的内容。|
|`\10`|匹配第n个分组的内容，如果它经匹配。否则指的是八进制字符码的表达式。|
|`(?P<name>)`|为分组起别名 别名 name|
|`(?P=name)`|引用分组 name 别名,进行匹配|

eg.
```py
import re
re.match(r'<(\w*)>.*</\1>',<h1>haha</h1>)   # 其中 (\w*) 作为一个分组被匹配，而 \1 会使用 第一组(\w*) 一样的表达式被匹配 匹配到 h1

re.match(r'<(?P<P2>\w*.)>.*</(?P=P2)>',<h1>hhhaaa</h1>) # 为(\w*)起别名P2
```
 
`^`	匹配字符串的开头  
`$`	匹配字符串的末尾。

# re 模块

## match方法
`re.match` 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match() 就返回 none。

`re.match(pattern, string, flags=0)`

- pattern	匹配的正则表达式
- string	要匹配的字符串。
- flags	标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。

匹配成功 re.match 方法返回一个匹配的对象，否则返回 None。

获取匹配表达式
|匹配对象方法|描述|
|:--|:--|
|group(num=0)|匹配的整个表达式的字符串，group() 可以一次输入多个组号，<br>在这种情况下它将返回一个包含那些组所对应值的元组。|
|groups()|返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。|

eg.

`re.match( r'(.*) are (.*?) .*',"Cats are smarter than dogs", re.M|re.I).group(2)`

## search方法

`re.search` 扫描整个字符串并返回第一个成功的匹配。

`re.search(pattern, string, flags=0)`

- pattern	匹配的正则表达式
- string	要匹配的字符串。
- flags	标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。

eg.

`re.search( r'(.*) are (.*?) .*', "Cats are smarter than dogs";, re.M|re.I).group(2)`

## re.match与re.search的区别

re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。

eg.
```py
import re
 
line = "Cats are smarter than dogs";
 
matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
   print "match --> matchObj.group() : ", matchObj.group()
else:
   print "No match!!"
 
matchObj = re.search( r'dogs', line, re.M|re.I)
if matchObj:
   print "search --> searchObj.group() : ", matchObj.group()
else:
   print "No match!!"

# 结果
# No match!!
# search --> searchObj.group() :  dogs
```

## sub()方法
`re.sub` 用于替换字符串中的匹配项。

`re.sub(pattern, repl, string, count=0, flags=0)`

- pattern : 正则中的模式字符串。
- repl : 替换的字符串，也可为一个函数。
- string : 要被查找替换的原始字符串。
- count : 模式匹配后替换的最大次数，默认 0 表示替换所有的匹配。
```py
import re
phone = "2004-959-559 # 这是一个国外电话号码"
 
# 删除字符串中的 Python注释 
num = re.sub(r'#.*$', "", phone)
print "电话号码是: ", num
 
# 删除非数字(-)的字符串 
num = re.sub(r'\D', "", phone)
print "电话号码是 : ", num
```

对于参数 `repl` 可以传入一个函数
```py
import re
 
# 将匹配的数字乘以 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)
 
s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))
```

## re.compile 函数

compile 函数用于编译正则表达式，生成一个正则表达式（ `Pattern` ）对象，供 `match()` 和 `search()` 这两个函数使用。

`re.compile(pattern[, flags])`

- `pattern` : 一个字符串形式的正则表达式

- `flags` : 可选，表示匹配模式，比如忽略大小写，多行模式等，具体参数为：

    - `re.I` 忽略大小写
    - `re.L` 表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
    - `re.M` 多行模式
    - `re.S` 即为 . 并且包括换行符在内的任意字符（. 不包括换行符）
    - `re.U` 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库
    - `re.X` 为了增加可读性，忽略空格和 # 后面的注释

在上面，当匹配成功时返回一个 `Match` 对象，其中：

- `group([group1, …])` 方法用于获得一个或多个分组匹配的字符串，当要获得整个匹配的子串时，可直接使用 `group()` 或 `group(0)`；
- `start([group])` 方法用于获取分组匹配的子串在整个字符串中的起始位置（子串第一个字符的索引），参数默认值为 0；
- `end([group])` 方法用于获取分组匹配的子串在整个字符串中的结束位置（子串最后一个字符的索引+1），参数默认值为 0；
- `span([group])` 方法返回 (start(group), end(group))。

eg.
```py
>>> import re
>>> pattern = re.compile(r'\d+')                    # 用于匹配至少一个数字
>>> m = pattern.match('one12twothree34four')        # 查找头部，没有匹配
>>> print m
None
>>> m = pattern.match('one12twothree34four', 2, 10) # 从'e'的位置开始匹配，没有匹配
>>> print m
None
>>> m = pattern.match('one12twothree34four', 3, 10) # 从'1'的位置开始匹配，正好匹配
>>> print m                                         # 返回一个 Match 对象
<_sre.SRE_Match object at 0x10a42aac0>
>>> m.group(0)
'12'
>>> m.start(0)
3
>>> m.end(0)  
5
>>> m.span(0) 
(3, 5)
```

### findall方法

在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果有多个匹配模式，则返回元组列表，如果没有找到匹配的，则返回空列表。

`findall(string[, pos[, endpos]])`

- string : 待匹配的字符串。
- pos : 可选参数，指定字符串的起始位置，默认为 0。
- endpos : 可选参数，指定字符串的结束位置，默认为字符串的长度。

```py
import re
 
pattern = re.compile(r'\d+')   # 查找数字
result1 = pattern.findall('runoob 123 google 456')
result2 = pattern.findall('run88oob123google456', 0, 10)
 
print(result1)
print(result2)

# 结果
# ['123', '456']
# ['88', '12']
``` 

同样  
`re.finditer(pattern, string, flags=0)`与findall 类似

eg.  
`re.finditer(r"\d+","12a32bc43jf3")`会返回一个匹配到的列表

## re.split
split 方法按照能够匹配的子串将字符串分割后返回列表

`re.split(pattern, string[, maxsplit=0, flags=0])`

- maxsplit	分隔次数，maxsplit=1 分隔一次，默认为 0，不限制次数。
- flags	标志位，用于控制正则表达式的匹配方式

```py
>>>import re
>>> re.split('\W+', 'runoob, runoob, runoob.')
['runoob', 'runoob', 'runoob', '']
>>> re.split('(\W+)', ' runoob, runoob, runoob.') 
['', ' ', 'runoob', ', ', 'runoob', ', ', 'runoob', '.', '']
>>> re.split('\W+', ' runoob, runoob, runoob.', 1) 
['', 'runoob, runoob, runoob.']
 
>>> re.split('a*', 'hello world')   # 对于一个找不到匹配的字符串而言，split 不会对其作出分割
['hello world']
```

## 贪婪与非贪婪

示例：

```py
import re
text = "/res/ww/markd_fafd.md"

# 正则表达式匹配包含 "markd_" 的字符串，并分组前后内容
pattern = re.compile(r'(.*)markd_(.*)')
match = pattern.match(text)
```

正则表达式中 `.*` 是贪婪匹配，它会尽可能多地匹配字符，可能导致匹配到字符串的末尾。

为了防止这种情况，可以使用非贪婪匹配，即 `.*?`，以便在第一次遇到 "markd_" 时停止匹配。