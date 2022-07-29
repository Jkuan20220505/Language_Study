# 第 1 章 Python数据模型
# 1.1　一摞Python风格的纸牌
import codecs
import collections
#  collections.namedtuple 用以构建只有少数属性但是没有方法的对象
Card = collections.namedtuple('Card', ['rank', 'suit'])   # 创建Card对象
beer_card = Card('7', 'diamonds')
print(beer_card.suit)


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]


deck = FrenchDeck()
print(deck.__len__())
print(len(deck))  # 定义了新类，方法重写

# 抽取第一张或最后一张,由__getitem__ 方法提供的
print(deck[0], deck[-1])

# Python 已经内置了从一个序列中随机选出一个元素的函数 random.choice,不需要去写
from random import choice
print(choice(deck))

# 查看一摞牌最上面 3 张
print(deck[:3])
# 只看牌面是 A 的牌的操作，先抽出索引是 12 的那张牌，然后每隔 13 张牌拿 1 张
print(deck[12::13])

# 实现了 __getitem__ 方法，这一摞牌就变成可迭代的了
# for card in deck:
#     print(card)
# for card in reversed(deck): # 反向迭代
#     print(card)

# 迭代通常是隐式的，譬如说一个集合类型没有实现 __contains__ 方法，那么 in运算符 就会按顺序做一次迭代搜索。
print(Card(rank='7', suit='clubs') in deck)  # 返回True

# 排序
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card1):
    rank_value = FrenchDeck.ranks.index(card1.rank)  # index() 方法检测字符串中是否包含子字符串 str
    return rank_value * len(suit_values) + suit_values[card1.suit]


for card in sorted(deck, key=spades_high):  #
    print(card)

# 特殊方法的存在是为了被 Python 解释器调用的，你自己并不需要调用它们。也就是说没有 my_object.__len__() 这种写法，而应该使用 len(my_object)。
# 在执行len(my_object) 的时候，如果 my_object 是一个自定义类的对象，那么 Python 会自己去调用其中由你实现的 __len__ 方法。

# 1.2　如何使用特殊方法
# 1.2.1　模拟数值类型
from math import hypot


class Vector:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def __repr__(self): # 重新输出
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self): 
        return hypot(self.x, self.y)  # sqrt(x*x + y*y) #向量的模

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(3,4)
v2 = Vector(5,6)
v3 = Vector(7,8)
print(v1.__add__(v2))
print(abs(v1))  # 向量的模
print(v2+v3)  # 向量加法
print(v1*3)  # 向量的标量乘法
print(bool(v1))
print(v1.__bool__())

# 1.2.2　字符串表示形式
# bool(x) 的背后是调用 x.__bool__() 的结果；如果不存在 __bool__ 方法，那么 bool(x) 会尝试调用 x.__len__()。

# 1.2.3　算术运算符
# 中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值

# 1.2.4　自定义的布尔值
# bool(x) 的背后是调用 x.__bool__() 的结果；如果不存在 __bool__ 方法，那么 bool(x) 会尝试调用 x.__len__()

# 1.3　特殊方法一览
# 表1-1：跟运算符无关的特殊方法:
    # 字符串/字节序列/表示形式: __repr__、__str__、__format__、__bytes__
    # 数值转换: __abs__、__bool__、__complex__、__int__、__float__、__hash__、__index__
    # 集合模拟: __len__、__getitem__、__setitem__、__delitem__、__contains__
    # 迭代枚举： __iter__、__reversed__、__next__
    # 可调用模拟： __call__
    # 上下文管理： __enter__、__exit__
    # 实例创建和销毁： __new__、__init__、__del__
    # 属性管理： __getattr__、__getattribute__、__setattr__、__delattr__、__dir__
    # 属性描述符： __get__、__set__、__delete__
    # 跟类相关的服务: __prepare__、__instancecheck__、__subclasscheck__
# 表1-2：跟运算符相关的特殊方法：
    # 一元运算符： __neg__ -、__pos__ +、__abs__ abs()
    # 众多比较运算符： __lt__ <、__le__ <=、__eq__ ==、__ne__ !=、__gt__ >、__ge__ >=
    # 算术运算符： __add__ +、__sub__ -、__mul__ *、__truediv__ /、__floordiv__ //、__mod__ %、__divmod__ divmod()、
#                __pow__ ** 或 pow()、__round__ round()
    # 反向算术运算符： __radd__、__rsub__、__rmul__、__rtruediv__、__rfloordiv__、__rmod__、__rdivmod__、__rpow__
    # 增量赋值算术运算符： __iadd__、__isub__、__imul__、__itruediv__、__ifloordiv__、__imod__、__ipow__
    # 位运算符： __invert__ ~、__lshift__ <<、__rshift__ >>、__and__ &、__or__ |、__xor__ ^
    # 反向位运算符： __rlshift__、__rrshift__、__rand__、__rxor__、__ror__
    # 增量赋值位运算符： __ilshift__、__irshift__、__iand__、__ixor__、__ior__

# 第 2 章 序列构成的数组
# 2.1　内置序列类型概览
# Python 标准库用 C 实现了丰富的序列类型，列举如下。 
# 容器序列：
#     list、tuple 和 collections.deque 这些序列能存放不同类型的数据。 
# 扁平序列： 
#     str、bytes、bytearray、memoryview 和 array.array，这类序列只能容纳一种类型。 
# 容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列里存放的是值而不是引用。
# 换句话说，扁平序列其实是一段连续的内存空间。由此可见扁平序列其实更加紧凑，但是它里面只能存放诸如字符、字节和数值这种基础类型。
# 序列类型还能按照能否被修改来分类。 
# 可变序列（MutableSequence）：list、bytearray、array.array、collections.deque 和 memoryview。 
# 不可变序列（Sequence）：tuple、str 和 bytes。


print('--------------------------------------------------------------')
'''
list 可以用的deque都可以用：
    1 list.append(obj)：在列表末尾添加新的对象
    2 list.count (obj)：统计某个元素在列表中出现的次数
    3 list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
    4 list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
    5 list.insert(index, obj)：将对象插入列表
        list2=['this','is','a','list']
        print(list2.index('is'))
        list2.insert(2,'insert at 2') # 在2位置插入'insert at 2'
        print(list2)
    6 list.pop([index=-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
    7 list.remove(obj)：移除列表中某个值的第一个匹配项
    8 list.reverse()：反向列表中元素
    9 list.sort(cmp=None, key=None, reverse=False)：对原列表进行排序

deque 可以用list不可以用的有：
    1 appendleft(x)：头部添加元素
    2 extendleft(iterable)：头部添加多个元素
    3 popleft()：头部返回并删除
    deque中append，extend，pop其实是对右端（尾部）的操作，省去没写
    4 rotate(n=1)：旋转
    5 maxlen：最大空间，如果是无边界的，返回None

collections 是Python内建的一个集合模块，提供了许多有用的集合类。
    1、namedtuple是一个函数, 它用来创建一个自定义的tuple对象,并且规定了 tuple元素的个数, 
       并可以用属性而不是索引来引用tuple的某个元素,Point = namedtuple('Point', ['x', 'y'])
    2、deque是为了高效的实现插入和删除操作的双向列表，适用于队列和栈。使用 deque(maxlen=N) 构造函数会新建一个固定大小的队列。
    如果你不设置队列的大小,那么就会得到一个无限大小队列。当新的元素加入并且这个队列已满的时候， 最老的元素会自动被移除掉。
        from collections import deque
        q = deque(['a', 'b', 'c'])
        q.append('y')
    3、OrderedDict可以保持字典中Key的顺序，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序 
        from collections import OrderedDict
    4、Counter是一个简单的计数器，例如，统计字符出现的个数。
        from collections import Counter
        c = Counter()
        for h in '21212132131298475984758712368271':
            c[h] = c[h]+1
        print(c)
'''

# 2.2　列表推导和生成器表达式
# 2.2.1　列表推导和可读性
# 注意：ord() 将字符转换为10进制的数。
#      例     >>>ord('a')
#             97
#      append() 末尾添加新的对象
symbols = '$¢£¥€¤'
codes = []
for symbol in symbols:
    codes.append(ord(symbol))
# 等价于
codes = [ord(symbol) for symbol in symbols]

beyond_ascii_1 = [ord(symbol) for symbol in symbols if ord(symbol) > 127]
# 等价于
beyond_ascii_2 = list(filter(lambda c: c > 127, map(ord, symbols)))
# map(函数，序列)函数 将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回。
# filter(函数，序列)函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。 
# lambda作为一个表达式，定义了一个匿名函数。上例中代码c为函数入口参数，c > 127 为函数体。
# 两者效果一样，[162, 163, 165, 8364, 164]

# 列表推导的作用只有一个：生成列表。
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)

# 内存里不会留下一个有 6 个组合的列表,生成器表达式就可以帮忙省掉运行 for 循环的开销
# 一个 % 运算符就把 passport 元组里的元素对应到了print函数的格式字符串空档中
for tshirt in ('%s %s' % (color, size) for color in colors for size in sizes):
    print(tshirt)   #输出形式：black S

# 2.2.4　生成器表达式
tuple(ord(symbol) for symbol in symbols)  # 元组
# list和tuple的区别,在于list可以在运行时修改内容和大小,tuple在首次创建和赋值后, 不可以再次修改内部的内容
# tuple还用于没有字段名的记录
# 数组 Python本身没有数组的说法， array 的构造方法需要两个参数，因此括号是必需的。
# array 构造方法的第一个参数指定了数组中数字的存储方式。 
import array
arr = array.array('I', (ord(symbol) for symbol in symbols))  
print(arr[2],"===============")


# 2.3　元组不仅仅是不可变的列表
# 2.3.1　元组和记录
# 元组就被当作记录加以利用
# city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)  # 把元组里面的值分别赋值
tokyo = ('Tokyo', 2003, 32450, 0.66, 8014)  # 拆包
city, year, pop, chg, area = tokyo
print(city)

# 一个元组列表，元组的形式为 (country_code, passport_number)
traveler_ids = [('USA', '31195855','ij'), ('BRA', 'CE342567','jj'), ('ESP', 'XDA205856','ll')]
# passport 变量被绑定到每个元组上
for passport in sorted(traveler_ids): 
    print('%s: %s==%s' % passport,"????????")   # 输出BRA: CE342567
    # 一个 % 运算符就把 passport 元组里的元素对应到了print函数的格式字符串空档中
# for循环可以分别提取元组里的元素，也叫作拆包（unpacking）。因为元组中第二个元素对我们没有什么用，
# 所以它赋值给“_”占位符。for country, number in traveler_ids:也可以分别获得值
for country, _, h in traveler_ids:
    print(country,h+"===========")

# 2.3.2　元组拆包
# 用*来处理剩下的元素，在平行赋值中，* 前缀只能用在一个变量名前面，但是这个变量可以出现在赋值表达式的任意位置
a, b, *res = range(7)
print(a,b,res)  # 输出：0 1 [2, 3, 4, 5, 6]，剩下元素用列表封装

# divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b),9//3=3 但9/3=3.0
print(divmod(20, 7),"divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)")

# os.path.split() 函数就会返回以路径和最后一个文件名组成的元组 (path, last_part)
import os
path, filename = os.path.split('/home/luciano/jslkjbg/ssh/idrsa.pub')
print(path,filename)  #输出：idrsa.pub

# 2.3.3　嵌套元组拆包
# 接受表达式的元组可以是嵌套式的，例如 (a, b, (c, d))
# 元组可以容纳多种类型的对象，拥有字符串不可变的特性
# 元组创建：
tuple1 = 1,2,3,'jk'
tuple2 = (1,3,5,'jkl')
tuple3 = ("vgfb",)
str1 = ('jkj')
str2 = 'dffd'
print(type(tuple1),type(tuple2),type(tuple3),type(str1),type(str2))
# <class 'tuple'> <class 'tuple'> <class 'tuple'> <class 'str'> <class 'str'>

# 2.3.4　具名元组
from collections import namedtuple
# collections.namedtuple() 创建一个具名元组需要两个参数，一个是类名，另一个是类的各个字段的名字。
# 后者可以是由数个字符串组成的可迭代对象，或者是由空格分隔开的字段名组成的字符串。
City = namedtuple('City', 'name country population coordinates')  # 创建City类
# 存放在对应字段里的数据要以一串参数的形式传入到构造函数中（注意，元组的构造函数却只接受单一的可迭代对象）
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667)) # 实例化
# 你可以通
# 过字段名或者位置来获取一个字段的信息。
print(tokyo.coordinates[0],"或者",tokyo[0])

# _fields 属性是一个包含这个类所有字段名称的元组。
print(City._fields)  #输出：('name', 'country', 'population', 'coordinates')

LatLong = namedtuple('LatLong', 'lat long') #创建LatLong类
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)  #用_make()通过接受一个可迭代对象来生成这个类的一个实例
print(delhi._asdict()) # 键值对返回
print(delhi._asdict().get('name')) # 字典根据键输出对应的值
# items() 方法把字典中每对 key 和 value 组成一个元组，并把这些元组放在列表中返回。
for key, value in delhi._asdict().items():
    print(key + ':', value)

# 2.3.5　作为不可变列表的元组
# s.__add__(s2)              s + s2，拼接
# s.__iadd__(s2)             s += s2，就地拼接
# s.append(e)                在尾部添加一个新元素
# s.clear()                  删除所有元素
# s.__contains__(e)          s 是否包含 e
# s.copy()                   列表的浅复制
# s.count(e)                 e 在 s 中出现的次数
# s.__delitem__(p)           把位于 p 的元素删除
# s.extend(it)               把可迭代对象 it 追加给 s
# s.__getitem__(p)           s[p]，获取位置 p 的元素
# s.__getnewargs__()         在 pickle 中支持更加优化的序列化
# s.index(e)                 在 s 中找到元素 e 第一次出现的位置
# s.insert(p, e)             在位置 p 之前插入元素 e
# s.__iter__()               获取 s 的迭代器
# s.__len__()                len(s)，元素的数量
# s.__mul__(n)               s * n，n 个 s 的重复拼接
# s.__imul__(n)              s *= n，就地重复拼接
# s.__rmul__(n)              n * s，反向拼接 *
# s.pop([p])                 删除最后或者是（可选的）位于 p 的元素，并返回它的值
# s.remove(e)                删除 s 中的第一次出现的 e
# s.reverse()                就地把 s 的元素倒序排列
# s.__reversed__()           返回 s 的倒序迭代器
# s.__setitem__(p, e)        s[p] = e，把元素 e 放在位置 p，替代已经在那个位置的元素
# s.sort([key], [reverse])   就地对 s 中的元素进行排序，可选的参数有键（key）和是否倒序（reverse）
