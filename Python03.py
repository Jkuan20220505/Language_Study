# 第 5 章 一等函数
# 5.1　把函数视作对象
# 输出n!
def factorial(n): 
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n-1)
print(factorial(4))

# 通过别的名称使用函数，再把函数作为参数传递
# map() 会根据提供的函数对指定序列做映射。map(function, iterable, ...)
# 第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
fn = factorial
print(fn(4))
print(list(map(fn,range(5)))) # [1, 1, 2, 6, 24]
# 有了一等函数，就可以使用函数式风格编程。函数式编程的特点之一是使用高阶函数

# 5.2　高阶函数
# 接受函数为参数，或者把函数作为结果返回的函数是高阶函数。map(function, iterable, ...)函数就是一例
# 函数式语言通常会提供 map、filter 和 reduce 三个高阶函数
# map 和 filter 返回生成器（一种迭代器），因此现在它们的直接替代品是生成器表达式
list(map(factorial, filter(lambda n: n % 2, range(6))))  # filter和lambda结合使用，使用 map 和 filter 计算直到 5! 的奇数阶乘列表。
[factorial(n) for n in range(6) if n % 2] # 使用列表推导做相同的工作，换掉 map 和 filter，并避免了使用 lambda 表达式。
# 使用 reduce 和 sum 计算 0~99 之和
from functools import reduce 
from operator import add

from pyparsing import Word 
print(reduce(add, range(100)))  #reduce(function, iterable[, initial])
print(sum(range(100)))

# 5.3　匿名函数
# lambda 关键字在 Python 表达式内创建匿名函数。lambda 函数的定义体只能使用纯表达式。
# 换句话说，lambda 函数的定义体中不能赋值，也不能使用 while 和 try 等 Python 语句。
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana'] 
sorted(fruits, key=lambda word: word[::-1]) #　使用 lambda 表达式反转拼写，然后依此给单词列表排序

# 5.4　可调用对象
# Python 数据模型文档列出了 7 种可调用对象: 用户定义的函数、内置函数、内置方法、方法、类、类的实例、生成器函数
#     用户定义的函数: 使用 def 语句或 lambda 表达式创建。
#     内置函数: 如 len 或 time.strftime
#     内置方法: 如 dict.get
#     方法: 在类的定义体中定义的函数
#     类:  调用类时会运行类的 __new__ 方法创建一个实例，然后运行 __init__ 方法，初始化实例，最后把实例返回给调用方。
# 因为 Python 没有 new 运算符，所以调用类相当于调用函数。
#     类的实例: 如果类定义了 __call__ 方法，那么它的实例可以作为函数调用
#     生成器函数:  使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象。

# 5.5　用户定义的可调用类型
import random
class BingoCage:
    def __init__(self, items):
        self._items = list(items) 
        random.shuffle(self._items) 
    def pick(self): 
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage') 
    def __call__(self): 
        return self.pick()

bingo = BingoCage(range(5)) #实例化对象
print(bingo._items) # [0, 2, 3, 1, 4]
bingo.pick()
print(bingo._items) # [0, 2, 3, 1]
bingo() #如果没有def __call__(self): 会报错，
print(bingo._items) # [0, 2, 3]     bingo()效果同bingo.pick()

# 5.7　从定位参数到仅限关键字参数
# Python提供了极为灵活的参数处理机制，而且Python3进一步提供了仅限关键字参数。
# 调用函数时使用 * 和 ** 展开可迭代对象，映射到单个参数。
def tag(name, *content, cls=None, **attrs):
#   生成一个或多个HTML标签
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

print(tag('br'))
print(tag('p', 'hello')) #第一个参数后面的任意个参数会被 *content 捕获，存入一个元组。
print(tag('p', 'hello', 'world')) 
#\n操作，输出： <p>hello</p>
#              <p>world</p>

print(tag('p', 'hello', id=33)) #tag 函数签名中没有明确指定名称的关键字参数会被 **attrs 捕获，存入一个字典。
# <p id="33">hello</p>

print(tag('p', 'hello', 'world', cls='sidebar')) # cls 参数只能作为关键字参数传入。
# <p class="sidebar">hello</p>
# <p class="sidebar">world</p>

print(tag(content='testing', name="img")) # 调用 tag 函数时，即便第一个定位参数也能作为关键字参数传入。
# <img content="testing" />

my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'} 
print(tag(**my_tag)) # 在 my_tag 前面加上 **，字典中的所有元素作为单个参数传入，同名键会绑定到对应的具名参数上，余下的则被 **attrs 捕获。
# <img class="framed" src="sunset.jpg" title="Sunset Boulevard" />

# 使用 reduce 函数和一个匿名函数计算阶乘
from functools import reduce
def fact1(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

# operator 模块为多个算术运算符提供了对应的函数
# 使用 reduce 和 operator.mul 函数计算阶乘
from functools import reduce
from operator import *
def fact2(n):
    return reduce(mul, range(1, n+1))

# itemgetter 的常见用途：根据元组的某个字段给元组列表排序
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):# 
    print(city)

cc_name = itemgetter(1, 0)  #输出序号为1和0的值
for city in metro_data:
    print(cc_name(city))

# attrgetter 与 itemgetter 作用类似，它创建的函数根据名称提取对象的属性。如果把多个属性名传给attrgetter，
# 它也会返回提取的值构成的元组。此外，如果参数名中包含 .（点号），attrgetter 会深入嵌套对象，获取指定的属性。
from collections import namedtuple
LatLong = namedtuple('LatLong','lat long')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop,(lat, long) in metro_data]
print(metro_areas[2]) # Metropolis(name='Mexico City', cc='MX', pop=20.142, coord=LatLong(lat=19.433333, long=-99.133333))
print(metro_areas[2].coord.lat) # 19.433333

from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat') #name_lat是函数名
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))