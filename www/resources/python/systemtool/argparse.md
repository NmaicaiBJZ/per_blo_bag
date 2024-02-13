# argparse -- 命令行选项、参数和子命令解析器
python版本：3.10.11  
argsparse是python的命令行解析的标准模块，内置于python，不需要安装。这个库可以让我们直接在命令行中就可以向程序中传入参数并让程序运行。
## 创建解释器
使用 argparse 的第一步是创建一个 ArgumentParser 对象：  
```python
>>> parser = argparse.ArgumentParser(description='···帮助指南···')
```
## 添加参数
给一个 `ArgumentParser` 添加程序参数信息是通过调用 `add_argument()` 方法完成的。通常，这些调用指定 `ArgumentParser` 如何获取命令行字符串并将其转换为对象。这些信息在 `parse_args()` 调用时被存储和使用。  
示例：
```python
>>> parser.add_argument('参数', metavar='N', type=int, nargs='+',help='··对参数的解释··')
>>> parser.add_argument('--sum', dest='accumulate', action='store_const',
...                     const=sum, default=max,
...                     help='对参数进行求和,无次选项则对参数取最大值')
```
然后，调用 `parse_args()` 将返回一个具有 `参数` 和 `accumulate` 两个属性的对象属性的对象。`参数` 属性将是一个包含一个或多个整数的列表，这是通过`nargs`与`type`指定的;而 `accumulate` 属性当命令行中指定了 `--sum` 参数时将是 `sum()` 函数，否则则是 `max()` 函数。
## 解析参数
`ArgumentParser` 通过 `parse_args()` 方法解析参数。它将检查命令行，把每个参数转换为适当的类型然后调用相应的操作。在大多数情况下，这意味着一个简单的 `Namespace` 对象将从命令行解析出的属性构建：
```python
>>> parser.parse_args(['--sum', '7', '-1', '42'])
# Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42])
```
在脚本中，通常 `parse_args()` 会被不带参数调用，而 `ArgumentParser` 将自动从 `sys.argv` 中确定命令行参数。
# ArgumentParser 对象
创建新的`ArgumentParser`对象，所有的参数都应当作为关键字参数传入，以下为详细描述：

|参数|说明|
|:--|:--|
|prog|程序的名称 (默认值: `os.path.basename(sys.argv[0])`)|
|usage|描述程序用途的字符串（默认值：从添加到解析器的参数生成）|
|description|对这个程序进行描述|
|epilog|额外的描述内容|
|parents|实现模块化和重用性|
|formatter_class|用于自定义帮助文档输出格式的类|
|prefix_chars|可选参数的前缀字符集合（默认值： '-'）|
|fromfile_prefix_chars|当需要从文件中读取其他参数时，用于标识文件名的前缀字符集合（默认值： None）|
|argument_default|参数的全局默认值（默认值： None）|
|conflict_handler|解决冲突选项的策略（通常是不必要的）|
|add_help|为解析器添加一个 -h/--help 选项（默认值： True）|
|allow_abbrev|如果缩写是无歧义的，则允许缩写长选项 （默认值：True）|
|exit_on_error|决定当错误发生时是否让 ArgumentParser 附带错误信息退出。 (默认值: True)|
## prog
默认情况下，`ArgumentParser` 对象使用 `sys.argv[0]` 来确定如何在帮助消息中显示程序名称。这一默认值几乎总是可取的，因为它将使帮助消息与从命令行调用此程序的方式相匹配。
> 注意： 无论是从 `sys.argv[0]` 或是从 `prog=` 参数确定的程序名称，都可以在帮助消息里通过 `%(prog)s` 格式说明符来引用。
```python 
>>> parser = argparse.ArgumentParser(prog='myprogram')
>>> parser.add_argument('--foo', help='foo of the %(prog)s program')
>>> parser.print_help()
usage: myprogram [-h] [--foo FOO]

options:
 -h, --help  show this help message and exit
 --foo FOO   foo of the myprogram program
```
## usage
默认情况下，`ArgumentParser` 根据它包含的参数来构建用法消息。

可以通过 `usage=` 关键字参数覆盖默认消息：
## description
这个参数简要描述这个程序做什么以及怎么做。 在帮助消息中，这个描述会显示在命令行用法字符串和各种参数的帮助消息之间:
## parents
parents 参数允许将一个或多个 `ArgumentParser` 对象作为参数传递给当前解析器，从而将它们的选项和参数添加到当前解析器中。这可以帮助你实现模块化和重用性，将一些通用的选项和参数定义在一个父解析器中，并在需要时添加到子解析器中。
```python
import argparse
# 创建父解析器
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--verbose', help='增加详细输出', action='store_true')
# 创建子解析器，并继承父解析器的选项和参数
parser = argparse.ArgumentParser(parents=[parent_parser])
parser.add_argument('input', help='输入文件路径')
args = parser.parse_args()
print(args.input)
print(args.verbose)
```
## formatter_class
`ArgumentParser` 对象允许通过指定备用格式化类来自定义帮助格式。目前，有四种这样的类。
- class argparse.RawDescriptionHelpFormatter
- class argparse.RawTextHelpFormatter
- class argparse.ArgumentDefaultsHelpFormatter
- class argparse.MetavarTypeHelpFormatter

```python
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     description='''this description
...         was indented weird
...             but that is okay''',
...     epilog='''
...             likewise for this epilog whose whitespace will
...         be cleaned up and whose words will be wrapped
...         across a couple lines''')
>>> parser.print_help()
usage: PROG [-h]

this description was indented weird but that is okay

options:
 -h, --help  show this help message and exit

likewise for this epilog whose whitespace will be cleaned up and whose words
will be wrapped across a couple lines
```
传 `RawDescriptionHelpFormatter` 给 `formatter_class=` 表示 `description` 和 `epilog` 已经被正确的格式化了，不能在命令行中被自动换行:
```python
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.RawDescriptionHelpFormatter,
...     description=textwrap.dedent('''\
...         Please do not mess up this text!
...         --------------------------------
...             I have indented it
...             exactly the way
...             I want it
...         '''))
>>> parser.print_help()
usage: PROG [-h]

Please do not mess up this text!
--------------------------------
   I have indented it
   exactly the way
   I want it

options:
 -h, --help  show this help message and exit
```
`RawTextHelpFormatter` 保留所有种类文字的空格，包括参数的描述。然而，多重的新行会被替换成一行。如果你想保留多重的空白行，可以在新行之间加空格。

`ArgumentDefaultsHelpFormatter` 自动添加默认的值的信息到每一个帮助信息的参数中:
```python
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
>>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
>>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
>>> parser.print_help()
usage: PROG [-h] [--foo FOO] [bar ...]

positional arguments:
 bar         BAR! (default: [1, 2, 3])

options:
 -h, --help  show this help message and exit
 --foo FOO   FOO! (default: 42)
```

 `MetavarTypeHelpFormatter` 为它的值在每一个参数中使用 type 的参数名当作它的显示名（而不是使用通常的格式 dest ）:

```python
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.MetavarTypeHelpFormatter)
>>> parser.add_argument('--foo', type=int)
>>> parser.add_argument('bar', type=float)
>>> parser.print_help()
usage: PROG [-h] [--foo int] float

positional arguments:
  float

options:
  -h, --help  show this help message and exit
  --foo int
```
## prefix_chars
许多命令行会使用 `-` 当作前缀，比如 `-f/--foo`。如果解析器需要支持不同的或者额外的字符，比如像 `+f` 或者 `/foo` 的选项，可以在参数解析构建器中使用 `prefix_chars=` 参数。
```python
>>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
>>> parser.add_argument('+f')
>>> parser.add_argument('++bar')
>>> parser.parse_args('+f X ++bar Y'.split())
Namespace(bar='Y', f='X')
```
prefix_chars= 参数默认使用 `'-'`。 提供一组不包括 `-` 的字符将导致 `-f/--foo` 选项不被允许。
## fromfile_prefix_chars
在某些时候，例如在处理一个特别长的参数列表的时候，把参数列表存入一个文件中而不是在命令行中打印出来会更有意义。 如果提供 `fromfile_prefix_chars=` 参数给 `ArgumentParser` 构造器，则任何以指定字符打头的参数都将被当作文件来处理，并将被它们包含的参数所替代。 举例来说:
```python
import argparse
parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('--input', help='输入文件路径')

args = parser.parse_args(['@params.txt'])
print(args.input)
```
fromfile_prefix_chars= 参数默认为 None，意味着参数不会被当作文件对待。
## argument_default
`argument_default` 参数用于设置解析器的默认参数值。如果没有明确指定参数的值，解析器将使用此默认值。这个参数可以帮助你在定义参数时为其提供默认值，简化参数的输入，同时允许用户在需要时覆盖默认值。
## conflict_handler
`conflict_handler` 参数用于处理选项和参数之间的冲突。如果多个选项或参数具有相同的名称，会导致冲突。`conflict_handler` 参数用于处理选项和参数之间的冲突。如果多个选项或参数具有相同的名称，会导致冲突。
```python
parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-a', help='选项A')
parser.add_argument('--a', help='选项B')

args = parser.parse_args(['-a', 'value_a', '--a', 'value_b'])
print(args.a)
```
# add_argument() 方法
|参数|说明|
|:--|:--|
|name or flags|一个命名或者一个选项字符串的列表，例如 foo 或 -f, --foo。|
|action|当参数在命令行中出现时使用的动作基本类型。|
|nargs|命令行参数应当消耗的数目。|
|const|被一些 action 和 nargs 选择所需求的常数。|
|default|当参数未在命令行中出现并且也不存在于命名空间对象时所产生的值。|
|typ|命令行参数应当被转换成的类型。|
|choices|限制参数值的有效选项|
|required|此命令行选项是否可省略 （仅选项可用）。|
|help|一个此选项作用的简单描述。|
|metavar|在使用方法消息中使用的参数值示例。|
|dest|被添加到 parse_args() 所返回对象上的属性名。|
## name or flags
add_argument() 方法必须知道它是否是一个选项，例如 -f 或 --foo，或是一个位置参数，例如一组文件名。
```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo')
>>> parser.add_argument('bar')
```
## action
ArgumentParser 对象将命令行参数与动作相关联。这些动作可以做与它们相关联的命令行参数的任何事，尽管大多数动作只是简单的向 parse_args() 返回的对象上添加属性。action 命名参数指定了这个命令行参数应当如何处理。action参数可采取以下取值：
- '`store`'（默认值）：将参数值存储起来。当指定了这个操作时，argparse 会将命令行参数的值存储到指定的变量中供您后续使用。
```python
parser.add_argument('--name', action='store', help='输入您的名字')
# 执行python script.py --name John后
# args.name 的值将是 'John'
```
- '`store_const`'：将参数的值存储为一个常量。通常与 `const` 参数一起使用，`const` 参数用于指定常量的值。
```python
parser.add_argument('--mode', action='store_const', const='fast', help='设置模式为快速模式')
# python script.py --mode
# 则 args.mode 的值将是 'fast'。
```
- '`store_true`' / '`store_false`'：将参数的值存储为 True 或 False。通常用于处理布尔型参数。
```python
parser.add_argument('--verbose', action='store_true', help='显示详细信息')
# python script.py --verbose
# 则 args.verbose 的值将是 True
```
- '`append`'：将参数的值存储为列表，并将多个参数值追加到列表中。
```python
parser.add_argument('--files', action='append', help='指定要处理的文件')
# python script.py --files file1.txt --files file2.txt
# 则 args.files 的值将是 ['file1.txt', 'file2.txt']。
```
- '`append_const`'：将参数的值追加到一个常量列表中。
```python
parser.add_argument('--modes', action='append_const', const='fast', help='添加快速模式')
# python script.py --modes --modes
# 则 args.modes 的值将是 ['fast', 'fast']。
```
- '`count`'：统计参数出现的次数。当指定了这个操作时，argparse 会记录参数在命令行中出现的次数，并将结果存储到指定的变量中。
```python
parser.add_argument('--verbose', action='count', help='增加详细信息的输出级别')
# python script.py --verbose --verbose --verbose
# 则 args.verbose 的值将是 3
```
- '`help`'：显示帮助信息，并退出程序。
- 自定义函数：您可以指定一个自定义函数作为 action 的值，该函数将在遇到参数时被调用。这允许您在解析命令行参数时执行自定义的操作。
```python
def custom_action(value):
    # 自定义操作
    print(f'执行自定义操作，参数值为：{value}')

parser.add_argument('--custom', action=custom_action, help='执行自定义操作')
# python script.py --custom value，
# 将调用 custom_action 函数，并将参数值 'value' 传递给该函数。
```
## nargs
ArgumentParser 对象通常关联一个单独的命令行参数到一个单独的被执行的动作。 nargs 命名参数关联不同数目的命令行参数到单一动作。
- `None`（默认值）：参数只接受单个值。这是最常见的情况。
- N （一个整数）。命令行中的 `N` 个参数会被聚集到一个列表中。
- '`?`':参数接受零个或一个值。如果在命令行中未提供该参数，则该参数的值为默认值（`default`）；如果提供了该参数，没有提供参数值，则默认为`const`的值。
```python
>>> parser.add_argument('--foo', nargs='?', const='c', default='d')
>>> parser.add_argument('--foo', nargs='?', const='c', default='d')
>>> parser.add_argument('bar', nargs='?', default='d')
>>> parser.parse_args(['XX', '--foo', 'YY'])
Namespace(bar='XX', foo='YY')
>>> parser.parse_args(['XX', '--foo'])
Namespace(bar='XX', foo='c')
>>> parser.parse_args([])
Namespace(bar='d', foo='d')
```
- '`*`'：参数接受零个或多个值。所有提供的值将被收集到一个列表中。
- '`+`'：参数接受一个或多个值。与 '`*`' 类似，但至少需要提供一个值。
## const
`const` 参数用于保存不从命令行中读取但被各种 ArgumentParser 动作需求的常数值。最常用的两例为：
- 通过 `action='store_const'` 或 `action='append_const` 调用时。这些动作将 `const` 值添加到 `parse_args()` 返回的对象的属性中。前面有示例。
- 通过选项调用并且 `nargs='?'` 时。这会创建一个可以跟随零个或一个命令行参数的选项。当解析命令行时，如果选项后没有参数，则将用 `const` 代替。在前面也有示例。
## default
default，默认值为 `None`，指定了在命令行参数未出现时应当使用的值。
```python
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('foo', nargs='?', default=42)
>>> parser.parse_args(['a'])
Namespace(foo='a')
>>> parser.parse_args([])
Namespace(foo=42)
```
提供 `default=argparse.SUPPRESS` 导致命令行参数未出现时没有属性被添加:
```python
>>> par.add_argument('--foo')
>>> par.parse_args([])
Namespace(foo=None)
>>> parser.add_argument('--foo', default=argparse.SUPPRESS)
>>> parser.parse_args([])
Namespace()
```
## type
`type` 参数用于指定参数值应该被解析为哪种数据类型。它允许您定义参数的类型转换规则，以确保参数值的正确性。`type` 参数可以接受以下几种不同的取值：
- 内置类型：您可以使用 Python 的内置类型（如 int、float、str 等）作为 type 的值，将参数的值转换为相应的类型。
  - `int`、`float`、`str`、`bool`，将参数转换为指定类型。`bool`将空字符串转为 `False` 而将非空字符串转为 `True`。
  - `ascii`：将参数值解析为 ASCII 字符串类型。使用 ascii 类型将确保参数值只包含 ASCII 字符。如果提供的值包含非 ASCII 字符，则会引发 UnicodeEncodeError。
  - `ord`：将参数值解析为整数类型，该整数表示字符的 Unicode 码位。ord 函数将字符转换为对应的 Unicode 码位。
  - `open`：将参数值解析为文件对象。使用 open 类型可以直接将参数值解析为一个打开的文件对象，而不仅仅是文件名。
  - `argparse.FileType('w', encoding='latin-1')`：将参数值解析为文件对象，并指定文件打开模式和编码。
  - `pathlib.Path`：将参数值解析为 pathlib.Path 对象。使用 pathlib.Path 类型可以方便地处理文件路径和目录路径。

- 自定义函数：您可以指定一个自定义函数作为 type 的值，该函数将在解析参数时被调用，并负责将参数值转换为所需的类型。
```python
def positive_float(value):
  f = float(value)
  if f <= 0:
      raise argparse.ArgumentTypeError('值必须为正数')
  return f

parser.add_argument('--value', type=positive_float, help='输入一个正数')
args = parser.parse_args()
# positive_float，该函数将确保命令行中提供的值被解析为正数类型。
# 如果提供的值不是正数，则会引发 ArgumentTypeError，并显示错误消息。
```
## choices 
`choices`参数用于限制参数值的有效选项。它允许您指定参数可以接受的特定值的列表，从而确保只有在有效选项内选择值时才能成功解析参数。
```python
parser = argparse.ArgumentParser()
parser.add_argument('--color', choices=['red', 'green', 'blue'], help='选择一种颜色')

args = parser.parse_args()
print(args)
```
## required
通常，`argparse` 模块会认为 `-f` 和 `--bar` 等旗标是指明 **可选的** 参数，它们总是可以在命令行中被忽略。 要让一个选项成为 必需的，则可以将 `True` 作为 `required=`的关键字。
```python
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', required=True)
>>> parser.parse_args([])
usage: [-h] --foo FOO
: error: the following arguments are required: --foo
# 必须对--foo进行指明
```
## help
`help` 值是一个包含参数简短描述的字符串。 当用户请求帮助时（一般是通过在命令行中使用 `-h` 或 `--help` 的方式），这些 `help` 描述将随每个参数一同显示:
`help` 字符串可包括各种格式描述符以避免重复使用程序名称或参数 default 等文本。 有效的描述符包括程序名称 `%(prog)s` 和传给 `add_argument()` 的大部分关键字参数，例如 %(default)s, %(type)s 等等:
```python
>>> parser = argparse.ArgumentParser(prog='frobble')
>>> parser.add_argument('bar', nargs='?', type=int, default=42,
...                     help='the bar to %(prog)s (default: %(default)s)')
>>> parser.print_help()
usage: frobble [-h] [bar]

positional arguments:
 bar     the bar to frobble (default: 42)

options:
 -h, --help  show this help message and exit
```
## metavar
成帮助消息时，它需要用某种方式来引用每个预期的参数。
```python
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', metavar='YYY')
>>> parser.add_argument('bar', metavar='XXX')
>>> parser.print_help()
usage:  [-h] [--foo YYY] XXX

positional arguments:
 XXX

options:
 -h, --help  show this help message and exit
 --foo YYY
```
## dest
指定参数值在解析结果中的目标属性名称。它决定了解析后的参数值将存储在哪个属性中。  
默认情况下，dest 参数的值与参数的长格式（即以两个连字符开头的参数，如 --verbose）相同，去掉连字符并将其转换为小写。但是，您可以通过指定 dest 参数来自定义目标属性的名称。
```python
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', dest='is_verbose', action='store_true', help='显示详细信息') # 如果没有dest，该属性名为verbose;当有dest后，属性名为is_verbose

args = parser.parse_args()
print(args.is_verbose)
```
# parse_args() 方法
- `args` - 要解析的字符串列表。 默认值是从 sys.argv 获取。
- `namespace` - 用于获取属性的对象。 默认值是一个新的空 Namespace 对象。
## 选项值语法
parse_args() 方法支持多种指定选项值的方式（如果它接受选项的话）。 在最简单的情况下，选项和它的值是作为两个单独参数传入的:
```python
···
>>> parser.parse_args(['-x', 'X'])
Namespace(foo=None, x='X')
>>> parser.parse_args(['--foo', 'FOO'])
Namespace(foo='FOO', x=None)
```
对于长选项（名称长度超过一个字符的选项），选项和值也可以作为单个命令行参数传入，使用 = 分隔它们即可:
```python
>>> parser.parse_args(['--foo=FOO'])
Namespace(foo='FOO', x=None)
```
对于短选项（长度只有一个字符的选项），选项和它的值可以拼接在一起:
```python
>>> parser.parse_args(['-xX'])
Namespace(foo=None, x='X')
```
有些短选项可以使用单个 - 前缀来进行合并，如果仅有最后一个选项（或没有任何选项）需要值的话:
```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-x', action='store_true')
>>> parser.add_argument('-y', action='store_true')
>>> parser.add_argument('-z')
>>> parser.parse_args(['-xyzZ'])
Namespace(x=True, y=True, z='Z')
```
## 无效参数
示例：
```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo', type=int)
>>> parser.add_argument('bar', nargs='?')

>>> # invalid type
>>> parser.parse_args(['--foo', 'spam'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: argument --foo: invalid int value: 'spam'

>>> # invalid option
>>> parser.parse_args(['--bar'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: no such option: --bar

>>> # wrong number of arguments
>>> parser.parse_args(['spam', 'badger'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: extra arguments found: badger
```
## 包含 - 的参数
示例：
```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-x')
>>> parser.add_argument('foo', nargs='?')

>>> # no negative number options, so -1 is a positional argument
>>> parser.parse_args(['-x', '-1'])
Namespace(foo=None, x='-1')

>>> # no negative number options, so -1 and -5 are positional arguments
>>> parser.parse_args(['-x', '-1', '-5'])
Namespace(foo='-5', x='-1')

>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-1', dest='one')
>>> parser.add_argument('foo', nargs='?')

>>> # negative number options present, so -1 is an option
>>> parser.parse_args(['-1', 'X'])
Namespace(foo=None, one='X')

>>> # negative number options present, so -2 is an option
>>> parser.parse_args(['-2'])
usage: PROG [-h] [-1 ONE] [foo]
PROG: error: no such option: -2

>>> # negative number options present, so both -1s are options
>>> parser.parse_args(['-1', '-1'])
usage: PROG [-h] [-1 ONE] [foo]
PROG: error: argument -1: expected one argument
```
如果你有必须以 - 打头的位置参数并且看起来不像负数，你可以插入伪参数 '--' 以告诉 parse_args() 在那之后的内容是一个位置参数
```python
>>> parser.parse_args(['--', '-f'])
Namespace(foo='-f', one=None)
 ```
# 参考
[官方文档-argparse简单介绍](https://docs.python.org/zh-cn/3/howto/argparse.html)
[官方文档-argparse详细介绍](https://docs.python.org/zh-cn/3/library/argparse.html#module-argparse)