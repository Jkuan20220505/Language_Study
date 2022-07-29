# x = [1,2,3,4]
# y = 'abcd'
# mateix  = [(i,j) for i in x if i>2 for j in y if ord(j) < 98]
# print(mateix)

# traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
# # passport 变量被绑定到每个元组上
# for passport in sorted(traveler_ids): 
#     print('%s: %s' % passport) 

# print(9/3) # 输出3.0
# print(9//3) # 输出3

# x = 2
# y = 4
# print(x.__add__(y))  # 2+4=6
# ======================以上是对昨天的复习==========================

# 2.4　切片
# 2.4.1　为什么切片和区间会忽略最后一个元素
# 利用任意一个下标来把序列分割成不重叠的两部分
l = [10, 20, 30, 40, 50, 60]
print(l[:2])  # [10, 20]   从序号0开始往后到序号2（不包括2）
print(l[3:])  # [40, 50, 60] 从序号3开始往后

# 2.4.2　对对象进行切片
# 用 s[a:b:c] 的形式对s在a和b之间以c为间隔取值。c的值还可以为负，负值意味着反向取值。
# a:b:c 这种用法只能作为索引或者下标用在 [] 中来返回一个切片对象：slice(a, b, c)。
s = 'bicycle'
print(s[::3])  # bye
print(s[::-2]) # eccb

# 2.4.3　多维切片和省略
# [] 运算符里还可以使用以逗号分开的多个索引或者是切片，外部库 NumPy 里就用到了这个特性，
# 二维的 numpy.ndarray 就可以用 a[i, j] 这种形式来获取( Python 会调用 a.__getitem__((i, j)) )，
# 亦或是用 a[m:n, k:l]的方式来得到二维切片。
# NumPy 中，... 用作多维数组切片的快捷方式。如果 x 是四维数组，那么 x[i, ...] 就是 x[i, :, :, :] 的缩写。

# 2.4.4　给切片赋值
l = list(range(10))
l[2:3] = [20,50] # tuple不支持对它的元素赋值
print(l) # [0, 1, 20, 50, 3, 4, 5, 6, 7, 8, 9]
del l[5:7]
print(l)  # [0, 1, 20, 50, 3, 6, 7, 8, 9] 删除从序号5(包括5)到序号7(不包括7)
l[4::2] = [11, 22, 33] 
print(l)  # [0, 1, 20, 50, 11, 6, 22, 8, 33] 从序号4开始，每间隔2就分别替代，要对应得上
l[2:5] = [100]  #如果赋值的对象是一个切片，那么赋值语句的右侧必须是个可迭代对象。 l[2:5] = 100就不行
print(l)  # [0, 1, 100, 6, 22, 8, 33]

# 2.5　对序列使用+和*
print(5*'abcd') #'abcdabcdabcdabcdabcd'
print([1,2]+[4,5,6]) #[1, 2, 4, 5, 6]  

l = [1, 2, 3]
print(id(l)) # 1777410238848
l *= 2
print(id(l),l) # 1777410238848 [1, 2, 3, 1, 2, 3]

# 2.7 list.sort方法和内置函数sorted
# list.sort 方法会就地排序列表，也就是说不会把原列表复制一份。
# 内置函数sorted，它会新建一个列表作为返回值。
# 两者有关键字：reverse,key
fruits = ['grape', 'raspberry', 'apple', 'banana']
print(sorted(fruits,reverse=True)) #按照字母降序排序，reverse=False就是升序
print(sorted(fruits,key=len)) #key=len进行基于字符串长度的排序

fruits.sort() #对原列表就地排序，返回值 None 会被控制台忽略。
print(fruits) #此时fruits本身被排序。

# 2.8　用bisect来管理已排序的序列
# insort(seq, item) 把变量 item 插入(前插)到序列 seq 中，并能保持 seq 的升序顺序。
import bisect
import random
SIZE=7
random.seed(1729) # 随机生成数
my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2) # randrange(start, stop, width) 函数在生成随机整数时不包括结束参数。
    bisect.insort(my_list, new_item)  
    print('%2d ->' % new_item, my_list)

# 2.9　当列表不是首选时
# 2.9.1　数组
# 只包含数字的列表，那么 array.array 比 list 更高效

# 2.9.3 NumPy和SciPy
# 凭借着 NumPy 和 SciPy 提供的高阶数组和矩阵操作，
# NumPy 实现了多维同质数组（homogeneous array）和矩阵，这些数据结构不但能处理数字，还能存放其他由用户定义的记录。
# SciPy 是基于 NumPy 的另一个库，它提供了很多跟科学计算有关的算法，专为线性代数、数值积分和统计学而设计。
# 对 numpy.ndarray 的行和列进行基本操作
import numpy
A = numpy.arange(12)
print(A.shape) # (12,) 看看数组的维度
A.shape = 3, 4 # 生成3行4列矩阵
print(A)
print(A[2]) # 打印出第 2 行
print(A[2][2]) 
print(A[:,1]) #把第 1 列打印出来。
print(A.transpose())  # 把行和列交换，就得到了一个新数组

# 2.9.4　双向队列和其他形式的队列
from collections import deque  # 使用双向队列
dq = deque(range(10), maxlen=10)
# 队列的移位操作接受一个参数 n，当 n > 0 时，队列的最右边的 n 个元素会被移动到队列的左边。
# 当 n < 0 时，最左边的 n 个元素会被移动到右边。
dq.rotate(3)
print(dq) # deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
dq.rotate(-4)
print(dq) # deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
# 当试图对一个已满（len(d) == d.maxlen）的队列做头部添加操作的时候，它尾部的元素会被删除掉。元素 0 被删除了。
dq.appendleft(-1) # 左边添加
print(dq) # deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
dq.extend([11, 22, 33])  # 相继添加，会挤掉[-1,1,2]
# extendleft(iter) 方法会把迭代器里的元素逐个添加到双向队列的左边，因此迭代器里的元素会逆序出现在队列里。
dq.extendleft([10, 20, 30, 40])
print(dq) # deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
# 除了 deque 之外，还有些其他的 Python 标准库也有对队列的实现。
# queue
# multiprocessing
# asyncio
# heapq

# 第 3 章 字典和集合
# 3.1　泛映射类型
# 字典提供了很多种构造方法,此外，字典推导也可以
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('one', 1),('two', 2),  ('three', 3)])
e = dict({'one': 1, 'two': 2,'three': 3})
# 3.2　字典推导
DIAL_CODES = [ 
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan'),
]
country_code = {country: code for code, country in DIAL_CODES}
print(country_code)
print({code: country.upper() for country, code in country_code.items() if code < 66})

# 字典
dict = {'a':12,'d':34}
dict.__delitem__('d')
# dict.clear()
print(dict.get('a'))
print(dict.values())